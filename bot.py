import telebot
import random
from dotenv import load_dotenv
import os
import model_classification

load_dotenv()
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)
print('Bot ready to use!')


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Предоставить запись")
    bot.send_message(message.chat.id,
                     '\n🤖 Добро пожаловать! 🤖'
                     '\n'
                     '\n🔍🎙️ Данный бот может определить русскоязычную речь на факт четкости её произношения. 🎙️🔍'
                     '\n'
                     '\n📌 Выберете <b>«Предоставить запись»</b> в меню бота. 📌',
                     reply_markup=markup, parse_mode="html")


def data_loader():
    @bot.message_handler(content_types=['voice'])
    def treatment(record):
        model_processing(bot.get_file(record.voice.file_id), record.chat.id)

    @bot.message_handler(content_types=['audio'])
    def treatment(record):
        model_processing(bot.get_file(record.audio.file_id), record.chat.id)

    @bot.message_handler(content_types=['text', 'photo', 'animation', 'game', 'story', 'video', 'document'])
    def error(message):
        bot.send_message(message.chat.id, 'Ошибка! Предоставьте аудио в формате'
                                          '\n<b>голосового сообщения</b> или <b>аудиофайла</b>.', parse_mode="html")


@bot.message_handler(regexp='предоставить запись')
def next_record(message):
    bot.send_message(message.chat.id, 'Предоставьте следующим сообщением запись.')
    data_loader()


def model_processing(file_info, chat_id):
    path = f'data/users/{chat_id}'
    os.makedirs(path, exist_ok=True)
    with open(path + f'/{chat_id}.wav', 'wb') as f:
        f.write(bot.download_file(file_info.file_path))

    prediction_values = model_classification.start(path + f'/{chat_id}.wav').ravel().tolist()
    discrepancy = prediction_values[1] - prediction_values[0]
    print(discrepancy)

    if (discrepancy < 0.393) and (discrepancy > -0.4):
        bot.send_message(chat_id, 'Аудиозапись содержит нормальную русскую речь.')
    elif discrepancy > 0.393:
        bot.send_message(chat_id, 'Аудиофайл содержит ненормальную русскую речь.')
    elif discrepancy < -0.4:
        bot.send_message(chat_id, 'Не удалось проанализировать предоставленный файл.')

    data_loader()


bot.infinity_polling()