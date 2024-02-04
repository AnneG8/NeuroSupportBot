# Neuro Support Bot

Боты Телеграм и ВКонтакте, отвечающие на стандартные сообщения пользователей. Реализовано с помощью DialogFlow.

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Подготовка [DialogFlow](https://dialogflow.cloud.google.com/)

1. [Создать проект](https://cloud.google.com/dialogflow/es/docs/quick/setup) в DialogFlow.
2. [Создать агента](https://cloud.google.com/dialogflow/es/docs/quick/build-agent).
3. Создать свои [намерения](https://dialogflow.cloud.google.com/#/agent/newagent-qseq/intents) и/или обновить существующие.
4. [Включить API](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) DialogFlow на вашем Google-аккаунте.
5. Установите и инициализируйте [Google Cloud CLI](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk). 
6. [Аутентифицируйте](https://cloud.google.com/dialogflow/es/docs/quick/setup#user) учетную запись. Во время аутентификации создастся файл `credentials.json`, сохраните путь к нему в переменную окружения `GOOGLE_APPLICATION_CREDENTIALS`.

### Переменные окружения

Для работы проекта, в корень необходимо положить файл `.env` со следующими полями:

Переменные, необходимые для работы Телеграм-бота:
- `TG_BOT_TOKEN` - токен Вашего Телеграм-бота. [Как создать бота и получить токен](https://core.telegram.org/bots#how-do-i-create-a-bot).
- `VK_BOT_TOKEN` - токен Вашего бота группы во ВКонтакте. Получить можно в разделе `Работа с API`.
- `DIALOGFLOW_PROJECT_ID` - id Вашего проекта, указан в поле `GOOGLE PROJECT` Вашего агента. [Посмотреть список агентов](https://dialogflow.cloud.google.com/#/agents).
- `GOOGLE_APPLICATION_CREDENTIALS` - путь к файлу `credentials.json`, созданному во время аутентификации (см. пункт 6 в разделе `Подготовка DialogFlow`).

### Запуск

1. Запустите Вашего Телеграм-бота командой
```bash
$ python3 tg_bot.py
```

2. Запустите Вашего бота во ВКонтакте командой
```bash
$ python3 vk_bot.py
```

Ботов можно запускать независимо друг от друга.

Также можно добавить намерения с помощью json-файла. Создайте json-файл формата:
```
{
    "Устройство на работу": {
        "questions": [
            "Фраза_1",
             ... ,
            "Фраза_N"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    {...},
     ... ,
    {...}
}
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для [dvmn.org](https://dvmn.org/).
