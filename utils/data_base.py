from json import load, dump
from os import path
from telebot.types import Message
from typing import Union, Optional


active_support = dict()
queues = list()


def set_users(message: Message, write_message_id: bool = False) -> None:
    """
    Запись пользователя в json
    :param write_message_id: True - если нужно записать message_id
    """
    file_path = path.join('data', 'users.json')
    users = get_users()
    if str(message.from_user.id) not in users.keys() and not message.from_user.is_bot:
        users[message.from_user.id] = dict(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code,
            is_premium=message.from_user.is_premium,
            chat_id=message.chat.id
        )
        if write_message_id:
            users[message.from_user.id]['message_id'] = message.id

        with open(file_path, 'w', encoding='utf-8') as file:
            dump(users, file, ensure_ascii=False, indent=4)

    elif write_message_id:
        users[str(message.from_user.id)]['message_id'] = message.id
        users[str(message.from_user.id)]['message_id2'] = message.message_id
        with open(file_path, 'w', encoding='utf-8') as file:
            dump(users, file, ensure_ascii=False, indent=4)


def get_users(user_id=None) -> dict:
    """
    Получение словаря с пользователями
    :param user_id: Принимает user_id пользователя которого нужно вернуть, по умолчанию None
    :return: Словарь с польльзователями при user_id is None, иначе словарь с конкретным пользователем
    """
    file_path = path.join('data', 'users.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            result = load(file)
    except FileNotFoundError:
        return dict()

    if user_id is None:
        return result
    else:
        return result.get(str(user_id))


def set_queue(user_id: str, delete: bool = False) -> None:
    """
    Вносит изменения в очередь
    :param user_id: id пользователя который встает/выходит в очередь
    :param delete: Флаг удаление
    """

    if user_id not in queues:
        queues.append(user_id)
    elif delete:
        queues.remove(user_id)


def get_queue(user_id: Optional[str] = None) -> Union[list, bool]:
    """
    Возвращает очередь
    :param user_id: id пользователя
    :return: При user_id is None возвращает list очереди, иначе делает проверку на наличие в очереди
    указанного пользователя True or False
    """
    if user_id is None:
        return queues
    else:
        return user_id in queues


def set_active_support(id_support: str, user_id: str, delete: bool = False) -> None:
    """
    Вносит изменение в словарь соединений между пользователем и поддержкой
    :param id_support: id поддержки
    :param user_id: id пользователя
    :param delete: Флаг удлаения
    """
    if delete:
        active_support.pop(id_support)
        active_support.pop(user_id)
    else:
        active_support[id_support] = user_id
        active_support[user_id] = id_support


def get_active_support(number_id=None):
    """
    Получает словарь соединений между пользователем и поддержкой либо значение по ключу number_id
    :param number_id: Ключ
    """
    if number_id is None:
        return active_support
    else:
        return active_support.get(str(number_id))


if __name__ == "__main__":
    ...
