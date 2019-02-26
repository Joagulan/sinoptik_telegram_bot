from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import json
from pymongo import MongoClient

client = MongoClient()
db = client.database_bot
collection = db.collection_bot
docs = db.docs

updater = Updater(token='559103957:AAHiFO-IE4w87hTE4IHV9wMr8fWSOaJwcS0')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)




reply_keyboard = [['Age', 'Favourite colour'],
                  ['Number of siblings', 'Something else...'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def start(bot, update):
    """start button"""
    update.message.reply_text("choose something", reply_markup=markup)












start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.start_polling()