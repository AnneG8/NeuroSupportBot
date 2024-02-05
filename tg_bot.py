from environs import Env
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)

from admin_alert import start_admin_alert
from dialogflow import detect_intent_text


env = Env()
env.read_env()
project_id = env.str('DIALOGFLOW_PROJECT_ID')


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Здравствуйте!')


def echo(update: Update, context: CallbackContext):
    update.message.reply_text(detect_intent_text(
        project_id,
        update.message.chat_id,
        update.message.text,
        'ru-Ru'
    ))


def main():
    tg_bot_token = env('ADMIN_TG_BOT_TOKEN')
    admin_chat_id = env('ADMIN_TG_CHAT_ID')
    if tg_bot_token and admin_chat_id:
        start_admin_alert(__name__, tg_bot_token, admin_chat_id)

    updater = Updater(env.str('TG_BOT_TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
