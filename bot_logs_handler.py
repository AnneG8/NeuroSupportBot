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
