from utils.data_base import get_active_support, set_queue, set_active_support, get_users, get_queue
from loader import bot, environ
from random import choice
from keyboard.reply.support import yes_or_no, detele_keyboard
from utils.helper import get_list_support
from datetime import datetime


list_thread = list()


def check_support(user_id) -> None:
    """
    Проверяет свободных социалистов, в случает нахождения отправляет ему запрос,
    иначе пользователя ставит в очередь
    :param user_id: id пользователя
    """
    list_support = get_list_support()
    active_support = get_active_support()

    free_support = [support for support in list_support if (support not in active_support)]

    if not free_support:
        set_queue(str(user_id))
    else:
        if str(user_id) in get_queue():
            set_queue(str(user_id), delete=True)
        support_id = choice(free_support)
        set_active_support(id_support=support_id, user_id=str(user_id))

        users = get_users(user_id=user_id)
        username = users.get('username')
        if username is None:

            if users.get('last_name') is None:

                if users.get('first_name') is None:
                    username = 'Имя Неизвестно'
                else:
                    username = users.get('first_name')
            else:
                username = users.get('last_name')

        text = f'У {username} вопросы, принимаешь диалог?'
        bot.send_message(chat_id=support_id, text=text, reply_markup=yes_or_no())


def finish_chat(user_id, support_id) -> None:
    """
    Завершение чата для обеих сторон
    :param user_id: id пользователя
    :param support_id: id поддержки
    """
    queue = get_queue()
    if user_id in queue:
        set_queue(user_id=user_id, delete=True)
        bot.send_message(chat_id=user_id, text='Чат завершен', reply_markup=detele_keyboard())
    else:
        set_active_support(user_id=user_id, id_support=support_id, delete=True)
        list_users = get_users()
        chat_id_user = list_users.get(user_id).get('chat_id')
        chat_id_support = list_users.get(support_id).get('chat_id')
        bot.set_state(chat_id=chat_id_user, user_id=int(user_id), state=None)
        bot.set_state(chat_id=chat_id_support, user_id=int(support_id), state=None)
        bot.send_message(chat_id=user_id, text='Чат завершен', reply_markup=detele_keyboard())
        bot.send_message(chat_id=support_id, text='Чат завершен', reply_markup=detele_keyboard())

        if queue:
            count = len(queue)
            text_to_support = f"В очереди еще {count} человека"
            bot.send_message(chat_id=support_id, text=text_to_support)
            check_support(queue[0])


def check_expectation(user_id) -> None:
    """
    Проверка ожидания ответа
    :param user_id: id пользователя
    :return:
    """
    from time import sleep
    sleep(int(environ.get('WAITING_TIME_MINUTES')) * 60)
    if str(user_id) not in list_thread:
        return
    list_thread.remove(str(user_id))
    user_id = str(user_id)
    support_id = get_active_support(number_id=user_id)
    queue = get_queue()
    if support_id is None:
        if str(user_id) in queue:
            set_queue(user_id=str(user_id), delete=True)
            text_to_user = "К сожалению сейчас все специалисты заняты и не могут ответить😔" \
                           f"\nВы можете получить консультацию по номерам {environ.get('NUMBERS_PHONE')}"
            bot.send_message(chat_id=user_id, text=text_to_user)
    elif support_id is not None:
        list_users = get_users()
        chat_id_support = list_users.get(support_id).get('chat_id')
        if bot.get_state(user_id=support_id, chat_id=chat_id_support) is not None:
            return

        set_active_support(user_id=user_id, id_support=support_id, delete=True)
        chat_id_user = list_users.get(user_id).get('chat_id')
        bot.set_state(chat_id=chat_id_user, user_id=int(user_id), state=None)
        bot.set_state(chat_id=chat_id_support, user_id=int(support_id), state=None)
        bot.send_message(chat_id=support_id, text='Чат завершен по окончанию времени ожидания',
                         reply_markup=detele_keyboard())
        text_to_user = "К сожалению сейчас все специалисты заняты и не могут ответить😔" \
                       "\nВы можете получить консультацию по номерам +7 939 809-51-30 и +7 (800) 101-19-14"
        bot.send_message(chat_id=user_id, text=text_to_user, reply_markup=detele_keyboard())

        queue = get_queue()
        if queue:
            count = len(queue)
            text_to_support = f"В очереди еще {count} человека"
            bot.send_message(chat_id=support_id, text=text_to_support)
            check_support(queue[0])


def check_work_time() -> bool:
    """
    Проврка рабочего времени
    :return: bool
    """
    work_weekday = [weekday.strip() for weekday in  environ.get('WORK_WEEKDAY').split(',')]
    start_work_hour = int(environ.get('START_WORK_HOUR'))
    stop_work_hour = int(environ.get('STOP_WORK_HOUR'))
    now = datetime.now()
    now_weekday = now.date().weekday()
    now_hour = now.time().hour

    if str(now_weekday) in work_weekday and start_work_hour <= now_hour < stop_work_hour:
        return True
    else:
        return False
