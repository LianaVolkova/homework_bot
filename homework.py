import logging
import os
import sys
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)
handler.setFormatter(formatter)


def send_message(bot, message):
    """Отправляет сообщение в Телеграм."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        raise error('Ошибка при отправке сообщения: {error}')
    else:
        logger.info('Сообщение отправлено')


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}

    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception as error:
        raise error('Ошибка при запросе к API: {error}')

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        raise TypeError(f'Проблемы соединения с сервером'
                        f'ошибка {response.status_code}')


def check_response(response):
    """Проверяет ответ API на корректность."""
    if not isinstance(response, dict):
        raise TypeError('Ответ API не является словарем')

    try:
        homeworks = response['homeworks']
    except KeyError:
        raise KeyError('Ожидаемые ключи отсутствуют')

    try:
        homeworks[0]
    except IndexError:
        raise IndexError('Домашняя работа отсутствует')
    else:
        if not isinstance(homeworks, list):
            raise TypeError('Cписок домашних работ отсутствует')
        else:
            return homeworks


def parse_status(homework):
    """Узнает статус проверки домашней работы."""
    homework_name = homework.get('homework_name')

    if not homework_name:
        raise KeyError('Домашняя работа отсутствует')

    homework_status = homework.get('status')
    if not homework_status:
        raise KeyError('Статус проверки работы отсутствует')

    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    logging.basicConfig(
        level=logging.INFO,
        filename='global.log'
    )

    if not check_tokens():
        logger.critical('Отсутствуют необходимые переменные окружения')
        raise SystemExit('Отсутствуют необходимые переменные окружения')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    last_status = None

    while True:
        try:
            response = get_api_answer(current_timestamp)
            message = check_response(response)
            status = parse_status(message)

            if status != last_status:
                last_status = status
                send_message(bot, status)
            else:
                logger.debug('Статус проверки домашней работы не изменился')

            current_timestamp = response.get('current_date')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            send_message(bot, message)

        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
