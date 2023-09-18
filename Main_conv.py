import telebot
from currency_converter import CurrencyConverter
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()
key_tg = os.getenv('YOUR_TOKEN')
bot = telebot.TeleBot(token=key_tg)

currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def con_start_com(message):
    bot.send_message(message.chat.id, f'Hello <b>{message.chat.first_name}</b>!\n\n'
                                      f'This bot can help you with the currency conversion\n'
                                      f'Add value', parse_mode='html')
    bot.register_next_step_handler(message, money)


def money(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Add correct num')
        bot.register_next_step_handler(message, money)
        return

    if amount > 0:
        murkup = types.InlineKeyboardMarkup(row_width=2)
        bt1 = types.InlineKeyboardButton('USD ➜ EUR', callback_data='usd/eur')
        bt2 = types.InlineKeyboardButton('EUR ➜ USD', callback_data='eur/usd')
        bt6 = types.InlineKeyboardButton('Other', callback_data='other')
        murkup.add(bt1, bt2, bt6)

        bot.send_message(message.chat.id, 'Choose currency', reply_markup=murkup)
    else:
        bot.send_message(message.chat.id, 'Add num witch have value > 0')
        bot.register_next_step_handler(message, money)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.data != 'other':
        val = call.data.upper().split('/')
        res = currency.convert(amount, val[0], val[1])
        bot.send_message(call.message.chat.id, f'Result: {round(res, 2)} \n\n'
                                               f'If you want make other currency - add new sum')
        bot.register_next_step_handler(call.message, money)
    else:
        bot.send_message(call.message.chat.id, 'Add your personal values use "/":')
        bot.register_next_step_handler(call.message, per_cur)


def per_cur(message):
    try:
        val = message.text.upper().split('/')
        res = currency.convert(amount, val[0], val[1])
        bot.send_message(message.chat.id, f'Result: {round(res, 2)} \n\n'
                                          f'If you want make other currency - add new sum')
        bot.register_next_step_handler(message, money)
    except Exception:
        bot.send_message(message.chat.id, 'Add correct num with the "/"')
        bot.register_next_step_handler(message, per_cur)


bot.polling(none_stop=True)