import os
from dotenv import load_dotenv
import telebot
from bot.handlers import register_handlers


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

def main():
    bot = telebot.TeleBot(TOKEN)
    register_handlers(bot)

    print("[✓] Бот запущен...")
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()