from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def yes_or_no() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = [
        KeyboardButton('Принять'),
        KeyboardButton('Отклонить'),
    ]

    return markup.add(*buttons)


def finish() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = [
        KeyboardButton('Завершить')
    ]

    return markup.add(*buttons)


def detele_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
