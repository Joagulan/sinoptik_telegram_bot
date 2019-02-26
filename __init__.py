from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler,
                          RegexHandler, run_async)
from telegram import (ReplyKeyboardMarkup)
from datetime import datetime, timedelta


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


cancel_button = '🚫 Отмена'

cancel_reply_markup = ReplyKeyboardMarkup(build_menu([cancel_button], n_cols=2),
                                          resize_keyboard=True)


def start(bot, update):
    buttons = ['Указать город', 'Узнать погоду']
    main_reply_markup = ReplyKeyboardMarkup(build_menu(buttons, n_cols=2), resize_keyboard=True)
    update.message.reply_text('Выберите нужный вам пункт:',
                              reply_markup=main_reply_markup)
    return -1


def city_name(bot, update):
    update.message.reply_text("Пожалуйста, укажите Ваш город:",
                              reply_markup=cancel_reply_markup)
    return "city_add_mongo"


def city_add_mongo(bot, update):
    user_id = update.message.chat_id
    user_city_name = update.message.text
    # добавление города пользоватетелю с user_id с MongoDB
    update.message.reply_text('Город <b>{}</b> успешно добавлен пользователю с <b>id {}</b>.'
                              .format(user_city_name, user_id),
                              parse_mode="HTML")
    start(bot, update)
    return -1


@run_async
def check_weather(bot, job):
    # проверить погоду и тем, кто заказывал вывод - вывести
    pass


city_handler = ConversationHandler(
    entry_points=[RegexHandler('^.*Указать город$', city_name)],

    states={
        "city_add_mongo": [RegexHandler(cancel_button, start),
                           MessageHandler(Filters.text, city_add_mongo)]
    },

    fallbacks=[RegexHandler(cancel_button, start)]
)


def main():
    updater = Updater("559103957:AAHiFO-IE4w87hTE4IHV9wMr8fWSOaJwcS0")

    dp = updater.dispatcher

    dp.add_handler(city_handler)
    dp.add_handler(MessageHandler(Filters.text, start))
    dp.add_handler(CommandHandler('start', start))

    jq = updater.job_queue
    jq.run_repeating(check_weather, interval=timedelta(minutes=10), first=timedelta(minutes=3))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()