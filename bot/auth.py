import os
from dotenv import load_dotenv

load_dotenv()
OWNER_ID = int(os.getenv("OWNER_ID"))
AUTH_OFF = False

def is_owner(message) -> bool:
    return message.from_user.id == OWNER_ID

def owner_only(bot, message) -> bool:
    if not is_owner(message):
        bot.send_message(message.chat.id, "🚫 Access denied.")
        return AUTH_OFF
    return True