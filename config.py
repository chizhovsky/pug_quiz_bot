import os

from dotenv import load_dotenv
from emoji import emojize

load_dotenv()

token = os.getenv("BOT_TOKEN")
admin_chat_id = os.getenv("ADMIN_ID")
emoji_one = emojize(":one:", language="alias")
emoji_two = emojize(":two:", language="alias")
emoji_three = emojize(":three:", language="alias")
emoji_four = emojize(":four:", language="alias")
emoji_five = emojize(":five:", language="alias")
emoji_six = emojize(":six:", language="alias")
