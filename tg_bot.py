import functools
import logging

from environs import Env
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)

from bot_logs_handler import BotLogsHandler
from dialogflow import detect_intent_text


logger = logging.getLogger('tg_bot')


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Здравствуйте!')


def project_reply(project_id, update: Update, context: CallbackContext):
    __, answer = detect_intent_text(
        project_id,
        f'vk-{update.message.chat_id}',
        update.message.text,
        'ru-Ru'
    )
    update.message.reply_text(answer)


def main():
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    env = Env()
    env.read_env()

    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    reply = functools.partial(project_reply, project_id)

    tg_bot_token = env('ADMIN_TG_BOT_TOKEN', None)
    admin_chat_id = env('ADMIN_TG_CHAT_ID', None)
    if tg_bot_token and admin_chat_id:
        logger.addHandler(BotLogsHandler(tg_bot_token, admin_chat_id))
        logger.warning('Bot started')

    updater = Updater(env.str('TG_BOT_TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
