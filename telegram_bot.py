# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
from time import gmtime, strftime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
reply_keyboard = [['/address', '/phone'],['/site', '/work_time', '/close']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

def echo(bot, update):
    # У объекта класса Updater есть поле message, являющееся
    # объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str), отсылающий ответ пользователю,
    # от которого получено сообщение.
    update.message.reply_text('Я получил сообщение ' + update.message.text[::-1])


def start(bot, update):
    update.message.reply_text("Я бот-справочник. Какая информация вам нужна?", reply_markup=markup)

def help(bot, update):
    update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


def address(bot, update):
    update.message.reply_text("Адрес: г. Москва, ул. Льва Толстого, 16")


def phone(bot, update):
    update.message.reply_text("Телефон: +7(495)776-3030")


def site(bot, update):
    update.message.reply_text("Сайт: http://www.yandex.ru/company")


def work_time(bot, update):
    update.message.reply_text("Время работы: пн-пт -- 9-00 - 19-00")

def close_keyboard(bot, update):
    update.message.reply_text("Ok", reply_markup=ReplyKeyboardRemove())

def time (bot, update):
    update.message.reply_text(strftime("%H:%M:%S", gmtime()))

def date (bot, update):
    update.message.reply_text(strftime("%Y-%m-%d", gmtime()))


def set_timer(bot, update, job_queue, chat_data, args):
    # создаём задачу task в очереди job_queue через 20 секунд
    # передаём ей идентификатор текущего чата
    # (будет доступен через job.context)
    try:
        delay = int(args[0])  # секунд
        job = job_queue.run_once(task, delay, context=update.message.chat_id)

        # Запоминаем в пользовательских данных созданную задачу.
        chat_data['job'] = job

        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text('Вернусь через '+str(delay)+' секунд!')
    except Exception as err:
        update.message.reply_text('Ошибка! Введите толко одно целое число!')

def task(bot, job):
    bot.send_message(job.context, text='Вернулся!')


def unset_timer(bot, update, chat_data):
    # Проверяем, что задача ставилась
    # (вот зачем нужно было ее записать в chat_data).
    if 'job' in chat_data:
        # планируем удаление задачи (выполнется, когда будет возможность)
        chat_data['job'].schedule_removal()
        # и очищаем пользовательские данные
        del chat_data['job']

    update.message.reply_text('Хорошо, вернулся сейчас!')

def main():
    # Создаём объект updater. Вместо слова "TOKEN" надо разместить
    # полученный от @BotFather токен
    updater = Updater(token='810937855:AAF8rSV6IbTPtYqG9vfWdlMQkoR2OaG-fi0')

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере эта функция
    # будет вызываться при получении сообщения с типом "текст",
    # т.е. текстовых сообщений.
    text_handler = MessageHandler(Filters.text, echo)

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("phone", phone))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("work_time", work_time))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("date", date))
    dp.add_handler(CommandHandler("set_timer", set_timer,
                                  pass_job_queue=True, pass_chat_data=True, pass_args=True))
    dp.add_handler(CommandHandler("unset_timer", unset_timer,
                                  pass_chat_data=True))

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
