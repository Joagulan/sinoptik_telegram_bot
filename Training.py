#!/usr/bin/python3
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import json
from pymongo import MongoClient
from yura import not_main

client = MongoClient()
db = client.database_bot
collection = db.collection_bot
docs = db.collection.docs

updater = Updater(token='559103957:AAHiFO-IE4w87hTE4IHV9wMr8fWSOaJwcS0')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hi!')


def add_city(bot, update, args):
    city = {'city': ' '.join(args)}
    city['weather'] = '+3'
    docs.insert_one(city)
    for i in docs.find():
        bot.send_message(chat_id=update.message.chat_id, text=f'{i["city"]} успешно добавлен.')


def call_weather(bot, update):
    for i in docs.find():
        bot.send_message(chat_id=update.message.chat_id, text=f'Температура в городе {i["city"]} - {i["weather"]} градуса.')




start_handler = CommandHandler('start', start, pass_user_data=True)
dispatcher.add_handler(start_handler)

city = CommandHandler('city', add_city, pass_args=True)
dispatcher.add_handler(city)

weather = CommandHandler('weather', call_weather)
dispatcher.add_handler(weather)

updater.start_polling()