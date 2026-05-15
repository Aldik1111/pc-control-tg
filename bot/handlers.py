from telebot import types
from bot.keyboards import main_menu, photo_menu,program_menu
from commands.photo_command import WebCamCommand, ScreenshotCommand
from commands.program_command import OpenProgramCommand, CloseProgramCommand
from data.logger import log_action

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

    @bot.message_handler(func = lambda x: x.text in ["Main", "Menu"])
    def handle_main(message):
        log_action(message.from_user.id, "Main menu")
        bot.send_message(message.chat.id, "Main menu", reply_markup=main_menu())

    @bot.message_handler(func = lambda x: x.text in ["Photo"])
    def handle_photo(message):
        log_action(message.from_user.id, "Photo menu")
        bot.send_message(message.chat.id, "Photo menu", reply_markup=photo_menu())

    @bot.message_handler(func = lambda x: x.text in ["Program"])
    def handle_program(message):
        log_action(message.from_user.id, "Program menu")
        bot.send_message(message.chat.id, "Program menu", reply_markup=program_menu())
    @bot.message_handler(func = lambda x: x.text in ["Close"])
    def handle_close(message):
        log_action(message.from_user_id, "Close program")
        bot.send_message(message.chat.id, "Close program", reply_markup=program_menu())

    # ─── Фото ─────────────────────────────────────────────────
    @bot.message_handler(func=lambda m: m.text in ["web", "Web"] )
    def handle_webcam(message):
        log_action(message.from_user.id, "Webcam photo")
        cmd = WebCamCommand(bot, message)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text in ["screen", "Screenshot", "Screen", "screenshot"])
    def handle_screenshot(message):
        log_action(message.from_user.id, "Screenshot")
        cmd = ScreenshotCommand(bot, message)
        cmd.execute()

    # ─── Открыть программы ────────────────────────────────────
    @bot.message_handler(func=lambda m: m.text == "Tlauncher")
    def handle_tlauncher(message):
        log_action(message.from_user.id, "Open Tlauncher")
        cmd = OpenProgramCommand(bot, message, "Tlauncher")
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "VS Code")
    def handle_vscode(message):
        log_action(message.from_user.id, "Open VS Code")
        cmd = OpenProgramCommand(bot, message, "Visual Studio Code")
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "Telegram")
    def handle_telegram(message):
        log_action(message.from_user.id, "Open Telegram")
        cmd = OpenProgramCommand(bot, message, "Telegram", match_closest=True)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "Discord")
    def handle_discord(message):
        log_action(message.from_user.id, "Open Discord")
        cmd = OpenProgramCommand(bot, message, "Discord")
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "💬 SMS / Social Media")
    def handle_social(message):
        log_action(message.from_user.id, "Social media menu")
        bot.send_message(message.chat.id, "Выбери приложение:", reply_markup=social_menu())

    # ─── Другие программы (ввод вручную) ──────────────────────
    @bot.message_handler(func=lambda m: m.text == "Other")
    def handle_other_open(message):
        log_action(message.from_user.id, "Other program")
        bot.send_message(message.chat.id, "Введи название программы:")
        bot.register_next_step_handler(message, _open_custom_program)

    def _open_custom_program(message):
        log_action(message.from_user.id, f"Open custom: {message.text}")
        cmd = OpenProgramCommand(bot, message, message.text, match_closest=True)
        cmd.execute()

    # ─── Закрыть программу (ввод вручную) ─────────────────────
    @bot.message_handler(func=lambda m: m.text == "Close")
    def handle_close(message):
        bot.send_message(message.chat.id, "Что закрыть?")
        bot.register_next_step_handler(message, _close_custom_program)

    def _close_custom_program(message):
        log_action(message.from_user.id, f"Close: {message.text}")
        cmd = CloseProgramCommand(bot, message, message.text)
        cmd.execute()