import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()


db_name = os.getenv('DB_NAME', default='postgres')
db_user = os.getenv('DB_USERNAME', default='postgres')
db_pass = os.getenv('DB_PASSWORD', default='postgres')
db_host = os.getenv('DB_HOST', default='localhost')
db_port = os.getenv('DB_PORT', default='5432')
PAYMENTS_TOKEN = os.getenv('PAYMENTS_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


storage = MemoryStorage()

bot = Bot(token=TELEGRAM_TOKEN)

dp = Dispatcher(bot, storage=storage)
