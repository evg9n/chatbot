from telebot.handler_backends import State, StatesGroup


class StateChatSupport(StatesGroup):
    user = State()
    support = State()
