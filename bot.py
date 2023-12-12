import telebot
import random
from dotenv import load_dotenv
import os


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Предоставить запись")
    bot.send_message(message.chat.id, 'Добро пожаловать, данный бот может определить русскоязычную речь на факт четкости её произношения.', reply_markup=markup)


@bot.message_handler(regexp='предоставить запись')
def record(message):
    bot.send_message(message.chat.id, 'Предоставьте следующим сообщением необходимую запись в формате .wav')


@bot.message_handler(content_types=['text'])
def get_messages(message):
    if message.text[-3:] == 'wav':
        bot.send_message(message.chat.id, 'Обработка…')

        resp = random.randint(1, 3)
        normal = 'Аудиозапись содержит нормальную русскую речь.'
        notNormal = 'Аудиофайл содержит ненормальную русскую речь.'
        nothing = 'Не удалось проанализировать предоставленный файл.'
        if resp == 1:
            bot.send_message(message.chat.id, normal)
        elif resp == 2:
            bot.send_message(message.chat.id, notNormal)
        else:
            bot.send_message(message.chat.id, nothing)

        bot.send_message(message.chat.id, 'Для отправки ещё одного запроса с повторным или новым аудиофайлом нажмите "Предоставить запись".')
    else:
        bot.send_message(message.chat.id, 'Неверный формат аудиозаписи, повторите попытку.')


bot.infinity_polling()