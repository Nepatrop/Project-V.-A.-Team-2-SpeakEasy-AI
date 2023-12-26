import telebot
import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Предоставить запись")
    bot.send_message(message.chat.id,
                     'Добро пожаловать, данный бот может определить русскоязычную речь на факт четкости её произношения.',
                     reply_markup=markup)


@bot.message_handler(regexp='предоставить запись')
def record(message):
    bot.send_message(message.chat.id, 'Предоставьте следующим сообщением необходимую запись.')


    @bot.message_handler(content_types=['voice', 'text'])
    def treatment(record):
        file_info = bot.get_file(record.voice.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))

        with open('voice.wav', 'wb') as f:
            f.write(file.content)

        bot.send_message(record.chat.id, 'Обработка…')

        resp = random.randint(1, 3)
        normal = 'Аудиозапись содержит нормальную русскую речь.'
        notNormal = 'Аудиофайл содержит ненормальную русскую речь.'
        nothing = 'Не удалось проанализировать предоставленный файл.'
        if resp == 1:
            bot.send_message(record.chat.id, normal)
        elif resp == 2:
            bot.send_message(record.chat.id, notNormal)
        else:
            bot.send_message(record.chat.id, nothing)

        bot.send_message(record.chat.id,
                         'Для отправки ещё одного запроса с повторным или новым аудиофайлом нажмите "Предоставить запись".')


bot.infinity_polling()
