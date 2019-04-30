# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
import requests

TRANSLATER_TOKEN = 'trnsl.1.1.20190401T124723Z.02dcee8d12c23e8c.863fd38574c842f9bcc68b57b036dabbaa2e7b55'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
reply_keyboard = [['английский->русский'], ['русский->английский']]
menu = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

sessionStorage = {}


def start(bot, updater):
    sessionStorage[updater.message.chat_id] = 'ru-en'
    updater.message.reply_text(
        "Я бот-переводчик. Выберите с какого языка переводить.(по умолчанию с русского на Английский)",
        reply_markup=menu)


def translater(bot, updater):
    if updater.message.text == 'английский->русский':
        sessionStorage[updater.message.chat_id] = 'en-ru'
        updater.message.reply_text('Теперь я буду переводить с английского на русский')
    elif updater.message.text == 'русский->английский':
        sessionStorage[updater.message.chat_id] = 'ru-en'
        updater.message.reply_text('Теперь я буду переводить с русского на английский')
    else:
        accompanying_text = "Переведено сервисом «Яндекс.Переводчик» http://translate.yandex.ru/."
        translator_uri = "https://translate.yandex.net/api/v1.5/tr.json/translate"
        response = requests.get(
            translator_uri,
            params={
                "key": TRANSLATER_TOKEN,
                # Направление перевода: с русского на английский.
                "lang": sessionStorage[updater.message.chat_id],
                # То, что нужно перевести.
                "text": updater.message.text
            })
        updater.message.reply_text("\n\n".join([response.json()["text"][0], accompanying_text]))


def main():
    # Создаём объект updater. Вместо слова "TOKEN" надо разместить
    # полученный от @BotFather токен
    updater = Updater(token='810937855:AAF8rSV6IbTPtYqG9vfWdlMQkoR2OaG-fi0')

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, translater)

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
