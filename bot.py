import telebot
import requests
import random
from dotenv import load_dotenv
import os
import model_classification

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
def next_record(message):
    bot.send_message(message.chat.id, 'Предоставьте следующим сообщением запись.')

    @bot.message_handler(content_types=['voice'])
    def treatment(record):
        model_processing(bot.get_file(record.voice.file_id), record.chat.id)

    @bot.message_handler(content_types=['audio'])
    def treatment(record):
        model_processing(bot.get_file(record.audio.file_id), record.chat.id)


def model_processing(file_info, chat_id):
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))

    with open('data/voice.wav', 'wb') as f:
        f.write(file.content)

    bot.send_message(chat_id, 'Обработка…')

    result = model_classification.start()
    print(result)



    #if result[0] < result[1]:
    #    bot.send_message(chat_id, 'Аудиозапись содержит нормальную русскую речь.')
    #elif result[0] > result[1]:
    #    bot.send_message(chat_id, 'Аудиофайл содержит ненормальную русскую речь.')
    #else:
    #    bot.send_message(chat_id, 'Не удалось проанализировать предоставленный файл.')

    bot.send_message(chat_id,
                     'Для отправки ещё одного запроса с повторным или новым голосовым сообщением нажмите "Предоставить запись".')


bot.infinity_polling()