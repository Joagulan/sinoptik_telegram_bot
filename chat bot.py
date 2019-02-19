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


logger = logging.getLogger(__name__)

GENDER = range(1)



def start(update, context):
    """start button"""
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    update.message.reply_text('choose something', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


    return GENDER


def gender ():
    return None

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GENDER: [RegexHandler('^(1|2|3)$', gender)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(conv_handler)


updater.start_polling()