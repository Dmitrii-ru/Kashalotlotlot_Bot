import os
import requests
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

# temp_file
TEMP_FILE_PATH  =  'media'

def media_file_path(file_name):
    if not os.path.exists(TEMP_FILE_PATH):
        os.makedirs(TEMP_FILE_PATH)
    file_path = os.path.join(TEMP_FILE_PATH, file_name)
    return file_path

def media_file_path_delete(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)






load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

redis_host='localhost'
redis_port=6379
redis_db=6
redis_live_time = 3