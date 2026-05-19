from telebot import types
from bot.keyboards import main_menu, photo_menu,program_menu
from commands.photo_command import WebCamCommand, ScreenshotCommand
from commands.program_command import OpenProgramCommand, CloseProgramCommand
from data.logger import log_action,get_last_logs

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def cmd_start(message):
        log_action(message.from_user.id, "/start")
        bot.send_message(
            message.chat.id,
            "Choose",
            reply_markup=main_menu()
        )

    # Main menu

    @bot.message_handler(func = lambda x: x.text in ["🏠 Main", "Main", "Menu"])
    def handle_main(message):
        log_action(message.from_user.id, "Main menu")
        bot.send_message(message.chat.id, "Main menu", reply_markup=main_menu())

    @bot.message_handler(func = lambda x: x.text in ["📷 Photo", "Photo"])
    def handle_photo(message):
        log_action(message.from_user.id, "Photo menu")
        bot.send_message(message.chat.id, "📷 Photo", reply_markup=photo_menu())

    @bot.message_handler(func = lambda x: x.text in ["💻 Program", "Programs", "Open program"])
    def handle_program(message):
        log_action(message.from_user.id, "Program menu")
        bot.send_message(message.chat.id, "💻 Program", reply_markup=program_menu())

    @bot.message_handler(func = lambda x: x.text in ["Close"])
    def handle_close(message):
        log_action(message.from_user.id, "Close program")
        bot.send_message(message.chat.id, "Close program", reply_markup=program_menu())

    # ─── Фото ─────────────────────────────────────────────────
    @bot.message_handler(func=lambda m: m.text in ["📸 Webcam", "web", "Web"] )
    def handle_webcam(message):
        log_action(message.from_user.id,"Webcam photo")
        cmd = WebCamCommand(bot, message)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text in ["🖥 Screenshot", "screen", "Screenshot", "Screen", "screenshot"])
    def handle_screenshot(message):
        log_action(message.from_user.id, "Screenshot")
        cmd = ScreenshotCommand(bot, message)
        cmd.execute()

    # ─── Открыть программы ────────────────────────────────────
    @bot.message_handler(func=lambda m: m.text == "🌐 Chrome")
    def handle_chrome(message):
        log_action(message.from_user.id, "Open Chrome")
        cmd = OpenProgramCommand(bot, message, "chrome", match_closest=True)
        cmd.execute()


    @bot.message_handler(func=lambda m: m.text == "🎮 Steam")
    def handle_steam(message):
        log_action(message.from_user.id, "Open Steam")
        cmd = OpenProgramCommand(bot, message, "steam", match_closest=True)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "🐍 Pycharm")
    def handle_pycharm(message):
        log_action(message.from_user.id, "Open PyCharm")
        cmd = OpenProgramCommand(bot, message, "pycharm", match_closest=True)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "🎵 Spotify")
    def handle_spotify(message):
        log_action(message.from_user.id, "Spotify")
        cmd = OpenProgramCommand(bot, message, "spotify", match_closest=True)
        cmd.execute()

    # ─── Другие программы (ввод вручную) ──────────────────────
    @bot.message_handler(func=lambda m: m.text == "🔧 Other")
    def handle_other_open(message):
        log_action(message.from_user.id, "Other program")
        bot.send_message(message.chat.id, "Input name of program:")
        bot.register_next_step_handler(message, _open_custom_program)

    def _open_custom_program(message):
        log_action(message.from_user.id, f"Open custom: {message.text}")
        cmd = OpenProgramCommand(bot, message, message.text, match_closest=True)
        cmd.execute()

    # ─── Закрыть программу (ввод вручную) ─────────────────────
    @bot.message_handler(func=lambda m: m.text == "❌ Close")
    def handle_close(message):
        log_action(message.from_user.id, "Close menu")
        bot.send_message(message.chat.id, "Input program name to close:")
        bot.register_next_step_handler(message, _close_custom_program)

    def _close_custom_program(message):
        log_action(message.from_user.id, f"Close: {message.text}")
        cmd = CloseProgramCommand(bot, message, message.text, match_closest=True)
        cmd.execute()


    @bot.message_handler(func=lambda m: m.text == "📊 History")
    def handle_history(message):
        log_action(message.from_user.id, "History")
        bot.send_message(message.chat.id, get_last_logs(5))