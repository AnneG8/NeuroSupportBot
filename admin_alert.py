import logging

import telegram


class BotLogsHandler(logging.Handler):
    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot = telegram.Bot(token=bot_token)
        self.chat_id = chat_id
    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id,
                              text=log_entry)


def start_admin_alert(bot_name, token, chat_id):
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(bot_name)

    logger.addHandler(BotLogsHandler(token, chat_id))
    logger.warning('Bot started')
