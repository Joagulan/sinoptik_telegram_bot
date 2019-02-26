#!/usr/bin/python3
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, RegexHandler, ConversationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import json
from pymongo import MongoClient
import datetime

client = MongoClient()
db = client.database_bot
collection = db.collection_bot
docs = db.collection.docs

updater = Updater(token='559103957:AAHiFO-IE4w87hTE4IHV9wMr8fWSOaJwcS0')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
job = updater.job_queue


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


back_button = 'Назад'

cancel_reply_markup = ReplyKeyboardMarkup(build_menu([back_button], n_cols=2),
                                          resize_keyboard=True)


def start(bot, update):
    """Start button"""

    reply_keyboard = ['Прислать погоду на сегодня', 'Прислать погоду на выбранную дату', 'Добавить/удалить город',
                      'Выбрать режим оповещаний']
    main_reply_markup = ReplyKeyboardMarkup(build_menu(reply_keyboard, n_cols=1),
                                            resize_keyboard=True)
    update.message.reply_text('Выберите нужный Вам пункт:',
                              reply_markup=main_reply_markup)

    return -1


def call_weather(bot, update):
    # Обращается к базе и выдает погоду на все требуемые города
    for i in docs.find():
        bot.send_message(chat_id=update.message.chat_id,
                         text=f'Температура в городе {i["city"]} - {i["weather"]} градуса.')

    start(bot, update)

    return -1


def chose_date_menu (bot, update):
    # Сделать 10 кнопок, которые будут меняться в зависимости от возножных 10 дат, на которые синоптик может дать погоду
    # Сделать прямой парсинг на выбранную дату. Или сделать регулярный парсинг погоды на все дни и кидать инфу с базы данных
    reply_keyboard = ['10 декабря', '11 декабря', '12 декабря', '13 декабря', '14 декабря', '15 декабря', '16 декабря',
                      '17 декабря', '18 декабря', '19 декабря']
    reply_markup = ReplyKeyboardMarkup(build_menu(reply_keyboard, n_cols=2, footer_buttons=[back_button]),
                                       resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Выберите дату', reply_markup=reply_markup)

    return 'dates_menu'


def wather_for_selected_weather(bot,update):
    # Спарсить напрямую погоду на выбранную дату и выдать в сообщении
    update.message.reply_text('Погода зачет')

    start(bot, update)

    return -1


def add_or_remove_city (bot, update):

    reply_keyboard = ['Добавить город', 'Удалить город', 'Ваш список городов']
    reply_markup = ReplyKeyboardMarkup(build_menu(reply_keyboard, n_cols=2, footer_buttons=[back_button]),
                                       resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Выберите нужный Вам пункт:', reply_markup=reply_markup)

    return 'city_menu'


def ask_city_to_add (bot, update):
    update.message.reply_text('Введите название города', reply_markup=cancel_reply_markup)
    # добавлять в базу данных id пользователя

    return 'add_city'


def add_city(bot, update):
    # Добавлять в базу id пользователя
    city = {'city': update.message.text}
    city['weather'] = '+3'

    docs.insert_one(city)
    update.message.reply_text(f'{city["city"]} успешно добавлен в базу данных.')

    start(bot, update)

    return -1


def ask_city_to_remove(bot, update):
    update.message.reply_text('Введите название города, которое хотите удалить.', reply_markup=cancel_reply_markup)

    return 'remove_city'


def remove_city(bot, update):
    # добавить функционал проверяющий наличие города в базе и в зависимости от этого отвечать
    update.message.reply_text(f'{update.message.text} успешно удален')

    start(bot, update)

    return -1


def list_of_cities(bot, update):
    # добавить функционал выводящий все города юзера с базы
    update.message.reply_text("Вот ваши города.")

    start(bot, update)

    return -1


def alerts(bot, update):
    # Добавить функционал если время еще никакое не введено или удалено, добавить кнопку "Выбрать время" и
    # убрать кнопку "Изменить время"
    reply_keyboard = ['Изменить время', 'Узнать текущий режим', 'Убрать оповещания']
    reply_markup = ReplyKeyboardMarkup(build_menu(reply_keyboard, n_cols=2, footer_buttons=[back_button]),
                                       resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Выберите нужный Вам пункт:', reply_markup=reply_markup)

    return 'alert_mode_menu'


def change_time (bot, update):
    update.message.reply_text('Введите желаемое время оповещания в формате ЧЧ:ММ', reply_markup=cancel_reply_markup)

    return 'changing_time'

def changing_time_for_alert(bot, update):
    # Добавить функционал изменения времени оповещания
    update.message.reply_text(f'Время оповещания изменено на {update.message.text}')

    start(bot, update)

    return -1

def current_mode(bot, update):
    # Вытащить с работы или с бд текущее время оповещания
    update.message.reply_text('Оповещания приходят в 12:00')

    start(bot, update)

    return -1


def delete_alert(bot, update):
    # выключить работу
    update.message.reply_text('Оповещание выключено')

    start(bot, update)

    return -1


def callback_minute(bot, job):
    bot.send_message(chat_id='406831253', text='beep')


menu_for_chose_dates = ConversationHandler(
    entry_points=[RegexHandler('Прислать погоду на выбранную дату', chose_date_menu)],
    states={
        'dates_menu': [RegexHandler(back_button, start),
                       RegexHandler('10 декабря', wather_for_selected_weather),
                       RegexHandler('11 декабря', wather_for_selected_weather),
                       RegexHandler('12 декабря', wather_for_selected_weather),
                       RegexHandler('13 декабря', wather_for_selected_weather),
                       RegexHandler('14 декабря', wather_for_selected_weather),# Даты будут браться или напрямую с синоптика
                       RegexHandler('15 декабря', wather_for_selected_weather),# или из БД
                       RegexHandler('16 декабря', wather_for_selected_weather),
                       RegexHandler('17 декабря', wather_for_selected_weather),
                       RegexHandler('18 декабря', wather_for_selected_weather),
                       RegexHandler('19 декабря', wather_for_selected_weather)]
    },
    fallbacks=[RegexHandler(back_button, start)]
)

add_remove_menu = ConversationHandler(
    entry_points=[RegexHandler('Добавить/удалить город', add_or_remove_city)],
    states={
        'city_menu': [RegexHandler(back_button, start),
                      RegexHandler('Добавить город', ask_city_to_add),
                      RegexHandler('Удалить город', ask_city_to_remove),
                      RegexHandler('Ваш список городов', list_of_cities)],
        'add_city': [RegexHandler(back_button, add_or_remove_city),
                     MessageHandler(Filters.all, add_city)],
        'remove_city': [RegexHandler(back_button, add_or_remove_city),
                        MessageHandler(Filters.all, remove_city)]

    },
    fallbacks=[RegexHandler(back_button, start)]
)

chose_alert_mode = ConversationHandler(
    entry_points= [RegexHandler('Выбрать режим оповещаний', alerts)],
    states={
        'alert_mode_menu': [RegexHandler(back_button, start),
                            RegexHandler('Изменить время', change_time),
                            RegexHandler('Узнать текущий режим', current_mode),# поменять на нормальные функции
                            RegexHandler('Убрать оповещания', delete_alert)],
        'changing_time': [RegexHandler(back_button, alerts),
                          MessageHandler(Filters.all, changing_time_for_alert)]
    },
    fallbacks=[RegexHandler(back_button, start)]
)

job_minute = job.run_daily(callback_minute, time=datetime.time(1,33,00)) # включить возможность изменить время от юзера


dispatcher.add_handler(CommandHandler('start', start, callback_minute, pass_job_queue=True))
dispatcher.add_handler(add_remove_menu)
dispatcher.add_handler(chose_alert_mode)
dispatcher.add_handler(RegexHandler('Прислать погоду на сегодня', call_weather))
dispatcher.add_handler(menu_for_chose_dates)

updater.start_polling()


