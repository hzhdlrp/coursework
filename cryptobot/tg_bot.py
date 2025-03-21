import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

TEST_PRIVATE_KEY = os.getenv('KEY')
TEST_ADDRESS = os.getenv('WALLET')
TOKEN = os.getenv('TOKEN')
SEPOLIA_RPC_URL = os.getenv('RPC_URL')
CONTRACT_ADDRESS = os.getenv('ADDRESS')

commands = ['записать в eth', 'прочитать из eth', 'записать в sol', 'прочитать из sol']

from eth import read_key, write_key, CONTRACT_ABI, web3, contract

bot = telebot.TeleBot(os.getenv('TOKEN'))

user_data = {}

def write_to_eth(number):
    logs = write_key(TEST_PRIVATE_KEY, number)
    return f"записано число {number}", logs

def read_from_eth():
    number = read_key(TEST_ADDRESS)
    return f"записано значение {number}"

def write_to_sol(number):
    return f"записано число {number}"

def read_from_sol():
    number = 5
    return f"записано значение {number}"

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Ethereum')
    btn2 = types.KeyboardButton('Solana')
    markup.add(btn1, btn2)
    return markup

def eth_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Записать в eth')
    btn2 = types.KeyboardButton('Прочитать из eth')
    back = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, back)
    return markup

# Меню для раздела 2
def sol_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Записать в sol')
    btn2 = types.KeyboardButton('Прочитать из sol')
    back = types.KeyboardButton('Назад')
    markup.add(btn1, btn2, back)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    print(chat_id)
    if message.text == 'Ethereum':
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=eth_menu())
    elif message.text == 'Solana':
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=sol_menu())
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=main_menu())
    if message.text == 'Записать в eth':
        user_data[chat_id] = 'eth'
        bot.send_message(chat_id, 'Введите число')
    elif message.text == 'Записать в sol':
        user_data[chat_id] = 'sol'
        bot.send_message(chat_id, 'Введите число')
    elif message.text == 'Прочитать из eth':
        bot.send_message(chat_id, read_from_eth())
    elif message.text == 'Прочитать из sol':
        bot.send_message(chat_id, read_from_sol())
    else:
        err_mess = "Это не число! Пожалуйста, введите число."
        if user_data.get(chat_id) == 'eth':
            try:
                bot.send_message(chat_id,'подождите, пожалуйста')
                number = int(message.text)
                text, logs = write_to_eth(number)
                for log in logs:
                    bot.send_message(chat_id, log)
                bot.send_message(chat_id, text)
                user_data[chat_id] = None
            except ValueError:
                bot.send_message(chat_id, err_mess)
        elif user_data.get(chat_id) == 'sol':
            try:
                bot.send_message(chat_id,'подождите, пожалуйста')
                number = int(message.text)
                bot.send_message(chat_id, write_to_sol(number))
                user_data[chat_id] = None
            except ValueError:
                bot.send_message(chat_id, err_mess)
        else:
            bot.send_message(chat_id, "Неизвестная команда")


bot.polling(none_stop=True)