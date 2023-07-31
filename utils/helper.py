from os import listdir
from os.path import join
from threading import Thread
from re import sub
from apscheduler.schedulers.blocking import BlockingScheduler

from loader import environ, bot
from utils.data_base import get_users


def get_list_support():
    return {user.strip() for user in environ.get('USERS_SUPPORT').split(',')}


def control_thread() -> None:
    """
    Контроль поток
    """
    shed = BlockingScheduler()

    if environ.get('LIST_DATETIME_MAILING') is None:
        return

    all_datetime = [date.strip() for date in environ.get('LIST_DATETIME_MAILING').split(',')]

    for date in all_datetime:
        # mailing(date_time=date, list_users=list_users)
        shed.add_job(send_mailing, 'date', run_date=date, args=(date, ))
    shed.start()


def send_mailing(date_time: str) -> None:
    """
    Рассылка
    """
    path = join('mailing', f"{sub(':', '', date_time)}.txt")
    list_users = list(get_users().keys())
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    if f"{sub(':', '', date_time)}.png" in listdir(join('mailing', 'photo')):

        for user in list_users:
            photo = open(join('mailing', 'photo', f"{sub(':', '', date_time)}.png"), 'rb')
            bot.send_photo(chat_id=user, photo=photo, caption=text)
            photo.close()
    else:
        for user in list_users:
            bot.send_message(chat_id=user, text=text)
