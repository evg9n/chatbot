from loader import bot
from telebot.custom_filters import StateFilter
from telebot.types import BotCommand
import handlers
import threading
from utils.helper import control_thread

DEFAULT_COMMANDS = (
    ('start', "Перезапустить бота"),
    # ('info', "Руководство использования"),
)


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )

    t = threading.Thread(target=control_thread)
    t.start()

    bot.infinity_polling()
