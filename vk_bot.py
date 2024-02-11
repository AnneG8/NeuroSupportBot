import logging

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.utils import get_random_id
from environs import Env

from bot_logs_handler import BotLogsHandler
from dialogflow import detect_intent_text


logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('vk_bot')


def send_answer(api, user_id, answer):
    api.messages.send(
        user_id=user_id,
        message=answer,
        random_id=get_random_id(),
    )


def main():
    env = Env()
    env.read_env()

    tg_bot_token = env('ADMIN_TG_BOT_TOKEN', None)
    admin_chat_id = env('ADMIN_TG_CHAT_ID', None)
    if tg_bot_token and admin_chat_id:
        logger.addHandler(BotLogsHandler(tg_bot_token, admin_chat_id))
        logger.warning('Bot started')

    vk_bot_token = env.str('VK_BOT_TOKEN')
    project_id = env.str('DIALOGFLOW_PROJECT_ID')

    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_id = event.user_id
                answer = detect_intent_text(
                    project_id,
                    f'vk-{user_id}',
                    event.text,
                    'ru-Ru'
                )
                if answer:
                    send_answer(vk, user_id, answer)


if __name__ == '__main__':
    main()
