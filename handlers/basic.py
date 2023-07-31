from os.path import join
from os import listdir
from keyboard.reply.support import finish
from loader import bot, environ
from telebot.types import Message
from utils.data_base import set_users
from utils.support import check_support, check_expectation, check_work_time, list_thread
from state.support import StateChatSupport
from utils.helper import get_list_support
from threading import Thread
from time import sleep


@bot.message_handler(commands=['start', ])
def start(message: Message):
    """
    Стартовый обработчик
    """
    set_users(message)

    if str(message.from_user.id) in get_list_support():
        text = "Здравствуй, человек, тебя назначил Сам👆😇 моим помощником чтобы ты общался с другими людьми😂" \
               "\nЯ дам тебе знать когда нужна будет твоя помощь😊"
        bot.send_message(chat_id=message.from_user.id, text=text)
    else:
        text = environ.get('START_TEXT')
        if environ.get('START_IMEG'):
            if environ.get('START_IMEG') in listdir(join('mailing', 'photo')):
                name = environ.get('START_IMEG')
                photo = open(join('mailing', 'photo', name), 'rb')
                bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=text)
            else:
                bot.send_message(chat_id=message.from_user.id, text=text)    
        else:
            bot.send_message(chat_id=message.from_user.id, text=text)


@bot.message_handler(commands=['info', ])
def info(message: Message):
    if str(message.from_user.id) in get_list_support():
        ...
    else:
        ...


@bot.message_handler(content_types=['text', 'sticker'])
def chat_support(message: Message):
    """
    Переводит на специалиста
    """

    if check_work_time():
        if str(message.from_user.id) in get_list_support():
            pass
        else:
            bot.set_state(user_id=message.from_user.id,
                          chat_id=message.chat.id,
                          state=StateChatSupport.user)
            check_support(str(message.from_user.id))
            text = 'Упс, я не был к этому готов 😅\nЗову человека\n🗣 Человееек, хелп миии'
            set_users(message=message, write_message_id=True)
            bot.send_message(chat_id=message.from_user.id, text=text)
            bot.send_message(chat_id=message.from_user.id, text='Ищу свободного человека🔎', reply_markup=finish())
            list_thread.append(str(message.from_user.id))
            t = Thread(target=check_expectation, args=(message.from_user.id,))
            t.start()
    else:
        work_weekday = [weekday.strip() for weekday in environ.get('WORK_WEEKDAY').split(',')]
        start_work_hour = int(environ.get('START_WORK_HOUR'))
        stop_work_hour = int(environ.get('STOP_WORK_HOUR'))
        list_weekdays = ['понедельник', "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
        work_weekday = [list_weekdays[int(number_weekday)] for number_weekday in work_weekday]
        text = "Вы написали в нерабочее время\n" \
               f"Мы работает в следующие дни недели: {', '.join(work_weekday)}\n" \
               f"С {start_work_hour}:00 до {stop_work_hour}:00"
        bot.send_message(chat_id=message.from_user.id, text=text)
