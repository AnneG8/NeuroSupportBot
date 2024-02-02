import logging

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)

from run import detect_intent_text


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

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
    updater = Updater(env.str('TG_BOT_TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
