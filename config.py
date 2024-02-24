import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("BOT_TOKEN")
admin_chat_id = os.getenv("ADMIN_ID")
db_settings = {
    "host": os.getenv("DB_HOST"),
    "name": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT"),
}
questions_count = 6
