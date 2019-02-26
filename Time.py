from telegram.ext import Updater
from telegram.ext import CommandHandler
import datetime
updater = Updater(token='559103957:AAHiFO-IE4w87hTE4IHV9wMr8fWSOaJwcS0')
dispatcher = updater.dispatcher
job = updater.job_queue


def callback_minute(bot, job):
    bot.send_message(chat_id='@Training_sinoptik_bot', text='beep')

job_minute = job.run_daily(callback_minute, time=datetime.time(1,13,00))

start = CommandHandler('start', callback_minute, pass_job_queue=True)
dispatcher.add_handler(start)

updater.start_polling()
# 406831253