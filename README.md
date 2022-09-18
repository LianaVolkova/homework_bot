# Телеграм-бот

## Описание
Бот взаимодействует с API сервиса Практикум.Домашка, отслеживает статус проверки домашней работы и при его изменении отправляет уведомление в Telegram. Также реализовано логирование, при котором в Telegram приходят сообщения о важных проблемах.

## Стек технологий
- Python 3.7
- python-telegram-bot

### Перед запуском проекта необходимо наличие двух токенов и id вашего аккаунта в Telegram:
 - Токен API Yandex.Praktikum - получить токен можно по этой [ссылке](https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a), если вы являетесь студентом одного из курсов в Yandex.Praktikum
 - Токен вашего Telegram-бота
    Как создать и получить токен, можно посмотреть [здесь](https://core.telegram.org/bots).
 - ID вашего аккаунта Telegram (для его получения можно воспользоваться одним из этих ботов: [@getmyid_bot](https://t.me/getmyid_bot) 
или [@userinfobot](https://telegram.me/userinfobot))

## Как запустить проект

Клонировать репозиторий:
```
git clone git@github.com:LianaVolkova/homework_bot.git
```
Перейдите в папку с проектом

Создать файл .env и прописать в нем переменные окружения

PRACTICUM_TOKEN = токен к API сервиса Яндекс.Домашка

TELEGRAM_TOKEN = токен Telegram бота

TELEGRAM_CHAT_ID = ID чата в Телеграме, куда будут приходить уведомления.

Установить и активировать виртуальное окружение:
```
python -m venv venv

source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt

``` 
pip install -r requirements.txt
```

### Документация
Краткая документация к API-сервису и примеры запросов доступны по [ссылке](https://code.s3.yandex.net/backend-developer/learning-materials/delugov/%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D1%83%D0%BC.%D0%94%D0%BE%D0%BC%D0%B0%D1%88%D0%BA%D0%B0%20%D0%A8%D0%BF%D0%B0%D1%80%D0%B3%D0%B0%D0%BB%D0%BA%D0%B0.pdf)

### Автор
Волкова Лиана
