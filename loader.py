from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from dotenv import load_dotenv
from os import environ


load_dotenv()

list_support = {user.strip() for user in environ.get('USERS_SUPPORT').split(',')}
storage = StateMemoryStorage()

bot = TeleBot(token=environ.get('TOKEN'), state_storage=storage)
