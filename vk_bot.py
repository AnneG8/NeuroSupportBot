import logging

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.utils import get_random_id
from environs import Env

from dialogflow import detect_intent_text


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def print_msg(event: Event):
    print('Новое сообщение:')
    if event.to_me:
        print('Для меня от: ', event.user_id)
    else:
        print('От меня для: ', event.user_id)
    print('Текст:', event.text)


def send_answer(api, user_id, message):
    api.messages.send(
        user_id=user_id,
        message=message,
        random_id=get_random_id(),
    )


def main():
    env = Env()
    env.read_env()
    vk_bot_token = env.str('VK_BOT_TOKEN')
    project_id = env.str('DIALOGFLOW_PROJECT_ID')

    vk_session = vk_api.VkApi(token=vk_bot_token)
    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print_msg(event)
            if event.to_me:
                user_id = event.user_id
                message = detect_intent_text(
                    project_id,
                    user_id,
                    event.text,
                    'ru-Ru'
                )
                send_answer(vk, user_id, message)





if __name__ == '__main__':
    main()
