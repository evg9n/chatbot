from keyboard.reply.support import finish, detele_keyboard
from loader import bot, environ
from telebot.types import Message
from utils.helper import get_list_support
from utils.data_base import get_active_support, set_active_support, get_users, get_queue
from state.support import StateChatSupport
from utils.support import finish_chat, check_support, list_thread


@bot.message_handler(state=StateChatSupport.support)
def support(message: Message):
    """
    Перенаправление сообщение поддержки на пользователя
    """
    support_id = str(message.from_user.id)
    user_id = get_active_support().get(support_id)
    if message.text == 'Завершить':
        finish_chat(user_id=user_id, support_id=support_id)
    else:
        text = message.text
        bot.send_message(chat_id=user_id, text=text)


@bot.message_handler(state=StateChatSupport.user)
def user(message: Message):
    """
    Перенаправления сообщения пользователя на поддержку
    """
    user_id = str(message.from_user.id)
    support_id = get_active_support().get(user_id)
    if message.text == 'Завершить':
        finish_chat(user_id=user_id, support_id=support_id)
    else:
        text = message.text
        bot.send_message(chat_id=support_id, text=text)


@bot.message_handler(func=lambda message: str(message.from_user.id) in get_list_support() and
                                          (message.text == "Принять" or message.text == 'Отклонить'))
def answer(message: Message):
    """
    Обработка поддержки о принятии чата с пользователем
    """
    active_support = get_active_support()
    support_id = str(message.from_user.id)
    user_id = active_support.get(support_id)
    users = get_users(user_id=user_id)
    username = users.get('username')

    if message.text == "Принять":
        if active_support.get(support_id):
            list_thread.remove(str(user_id))
            active_support[support_id] = user_id
            bot.set_state(user_id=message.from_user.id,
                          chat_id=message.chat.id,
                          state=StateChatSupport.support)

            if username is None:

                if users.get('last_name') is None:

                    if users.get('first_name') is None:
                        username = 'Имя Неизвестно'
                    else:
                        username = users.get('first_name')
                else:
                    username = users.get('last_name')

            bot.send_message(chat_id=message.from_user.id, text=f'Чат начат c {username}', reply_markup=finish())
            bot.send_message(chat_id=user_id,
                             text=f'Здравствуйте, меня зовут {environ.get(f"{message.from_user.id}")}'
                                  f'\nЧем могу помочь?')
        else:
            ...
    #         TODO Добавить
    elif message.text == "Отклонить":
        set_active_support(user_id=user_id, id_support=support_id, delete=True)
        list_users = get_users()
        chat_id_user = list_users.get(user_id).get('chat_id')
        bot.set_state(chat_id=chat_id_user, user_id=int(user_id), state=None)
        text_to_user = "К сожалению сейчас все специалисты заняты и не могут ответить😔" \
                       "\nВы можете получить консультацию по номерам +7 939 809-51-30 и +7 (800) 101-19-14"

        bot.send_message(chat_id=user_id, text=text_to_user, reply_markup=detele_keyboard())
        bot.send_message(chat_id=support_id, text='Чат отменен', reply_markup=detele_keyboard())

        queue = get_queue()
        if queue:
            count = len(queue)
            text_to_support = f"В очереди еще {count} человека"
            bot.send_message(chat_id=support_id, text=text_to_support)
            check_support(queue[0])


# @bot.message_handler(func=lambda message: str(message.from_user.id) in get_list_support())
# def fsdfsdf(message: Message):
#     bot.send_message(chat_id=message.from_user.id, text='fdsgfsdfsdf')
