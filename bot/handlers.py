from bot.keyboards import main_menu, photo_menu,program_menu, notes_menu, turn_menu
from bot.auth import owner_only
from commands.photo_command import WebCamCommand, ScreenshotCommand
from commands.program_command import OpenProgramCommand, CloseProgramCommand
from data.logger import log_action,get_last_logs
from data.notes import add_note, get_all_notes, delete_note
from commands.computer_command import (StatsCommand, ProcessesCommand,
    ShutdownCommand, RestartCommand, CancelShutdownCommand,
    SleepCommand, LockCommand)
from commands.weather_command import WeatherCommand
from utils.decorators import owner_required,log_command


def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def cmd_start(message):
        if not owner_only(bot, message):
            return
        log_action(message.from_user.id, "/start")
        bot.send_message(
            message.chat.id,
            "Choose",
            reply_markup=main_menu()
        )

    # Main menu

    @bot.message_handler(func = lambda x: x.text in ["🏠 Main", "Main", "Menu"])
    @owner_required(bot)
    @log_command("Main")
    def handle_main(message):
        bot.send_message(message.chat.id, "Main menu", reply_markup=main_menu())

    @bot.message_handler(func = lambda x: x.text in ["📷 Photo", "Photo"])
    @owner_required(bot)
    @log_command("Photo")
    def handle_photo(message):
        bot.send_message(message.chat.id, "📷 Photo", reply_markup=photo_menu())

    @bot.message_handler(func = lambda x: x.text in ["💻 Program", "Programs", "Open program"])
    @owner_required(bot)
    @log_command("Program Menu")
    def handle_program(message):
        bot.send_message(message.chat.id, "💻 Program", reply_markup=program_menu())

    @bot.message_handler(func = lambda x: x.text in ["Close"])
    @owner_required(bot)
    @log_command("Close program")
    def handle_close(message):
        bot.send_message(message.chat.id, "Close program", reply_markup=program_menu())


    @bot.message_handler(func = lambda x: x.text in ["🔴 Turnoff"])
    @owner_required(bot)
    @log_command("Turn off menu")
    def turnoff_menu(message):
        bot.send_message(message.chat.id, "🔴 Turnoff menu", reply_markup=turn_menu())
    # ─── Фото ─────────────────────────────────────────────────
    @bot.message_handler(func=lambda m: m.text in ["📸 Webcam", "web", "Web"] )
    @owner_required(bot)
    @log_command("Web photo")
    def handle_webcam(message):
        cmd = WebCamCommand(bot, message)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text in ["🖥 Screenshot", "screen", "Screenshot", "Screen", "screenshot"])
    @owner_required(bot)
    @log_command("Screenshot")
    def handle_screenshot(message):
        cmd = ScreenshotCommand(bot, message)
        cmd.execute()

    # ─── Открыть программы ────────────────────────────────────
    @bot.message_handler(func=lambda m: m.text == "🌐 Chrome")
    @owner_required(bot)
    @log_command("Chrome")
    def handle_chrome(message):
        cmd = OpenProgramCommand(bot, message, "chrome", match_closest=True)
        cmd.execute()


    @bot.message_handler(func=lambda m: m.text == "🎮 Steam")
    @owner_required(bot)
    @log_command("Steam")
    def handle_steam(message):
        cmd = OpenProgramCommand(bot, message, "steam", match_closest=True)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "🐍 Whatsapp")
    @owner_required(bot)
    @log_command("Whatsapp")
    def handle_pycharm(message):
        cmd = OpenProgramCommand(bot, message, "whatsapp", match_closest=True)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "🎵 Spotify")
    @owner_required(bot)
    @log_command("Spotify")
    def handle_spotify(message):
        cmd = OpenProgramCommand(bot, message, "spotify", match_closest=True)
        cmd.execute()

    # ─── Другие программы (ввод вручную) ──────────────────────
    @bot.message_handler(func=lambda m: m.text == "🔧 Other")
    @owner_required(bot)
    @log_command("Other")
    def handle_other_open(message):
        bot.send_message(message.chat.id, "Input name of program:")
        bot.register_next_step_handler(message, _open_custom_program)

    def _open_custom_program(message):
        cmd = OpenProgramCommand(bot, message, message.text, match_closest=True)
        cmd.execute()

    # ─── Закрыть программу (ввод вручную) ─────────────────────
    @bot.message_handler(func=lambda m: m.text == "❌ Close")
    @owner_required(bot)
    @log_command("Close program")
    def handle_close(message):
        bot.send_message(message.chat.id, "Input program name to close:")
        bot.register_next_step_handler(message, _close_custom_program)

    def _close_custom_program(message):
        log_action(message.from_user.id, f"Close: {message.text}")
        cmd = CloseProgramCommand(bot, message, message.text, match_closest=True)
        cmd.execute()



    #────────── Notes ────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text == "📊 History")
    @owner_required(bot)
    @log_command("History")
    def handle_history(message):
        bot.send_message(message.chat.id, get_last_logs(5))

    @bot.message_handler(func=lambda m: m.text == "📝 Notes")
    @owner_required(bot)
    @log_command("notes")
    def handle_notes(message):
        bot.send_message(message.chat.id, "📝 Notes menu:", reply_markup=notes_menu())

    @bot.message_handler(func=lambda m: m.text == "📋 All notes")
    @owner_required(bot)
    @log_command("All notes")
    def handle_all_notes(message):
        bot.send_message(message.chat.id, get_all_notes())

    @bot.message_handler(func=lambda m: m.text == "➕ Add note")
    @owner_required(bot)
    @log_command("new note")
    def handle_add_note(message):
        bot.send_message(message.chat.id, "✏️ Write your note:")
        bot.register_next_step_handler(message, _save_note)

    def _save_note(message):
        add_note(message.from_user.id, message.text)
        bot.send_message(message.chat.id, f"✅ Note saved!\n\n" + get_all_notes())

    @bot.message_handler(func=lambda m: m.text == "🗑 Delete note")
    @owner_required(bot)
    @log_command("Delete note")
    def handle_delete_note(message):
        bot.send_message(message.chat.id, get_all_notes() + "\nEnter # to delete (e.g. 2):")
        bot.register_next_step_handler(message, _delete_note)

    def _delete_note(message):
        if not owner_only(bot, message):
            return
        try:
            index = int(message.text.strip("#"))
            if delete_note(index):
                bot.send_message(message.chat.id, f"✅ Note #{index} deleted!\n\n" + get_all_notes())
            else:
                bot.send_message(message.chat.id, f"❌ Note #{index} not found.")
        except ValueError:
            bot.send_message(message.chat.id, "❌ Enter a number, e.g. 1 or 3")


    # _________________________________Process and Stats ------------------------
    @bot.message_handler(func=lambda m: m.text == "📊 Stats")
    @owner_required(bot)
    @log_command("Stats")
    def handle_stats(message):
        bot.send_message(message.chat.id, "⏳ Collecting data...")
        cmd = StatsCommand(bot, message)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "⚡ Processes")
    @owner_required(bot)
    @log_command("Processes")
    def handle_processes(message):
        bot.send_message(message.chat.id, "⏳ Collecting processes...")
        cmd = ProcessesCommand(bot, message)
        cmd.execute()

    # --------------------------- Shutdown / Restart ------------------------------

    @bot.message_handler(func=lambda m: m.text == "🔴 Shutdown")
    @owner_required(bot)
    @log_command("Shutdown")
    def handle_shutdown(message):
        cmd = ShutdownCommand(bot, message)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "🔄 Restart")
    @owner_required(bot)
    @log_command("Restart")
    def handle_restart(message):
        cmd = RestartCommand(bot, message)
        cmd.execute()

    @bot.message_handler(commands=["cancel"])
    @owner_required(bot)
    @log_command("cancel shutdown")
    def handle_cancel(message):
        cmd = CancelShutdownCommand(bot, message)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "😴 Sleep")
    @owner_required(bot)
    @log_command("Sleep")
    def handle_sleep(message):
        cmd = SleepCommand(bot, message)
        cmd.execute()

    @bot.message_handler(func=lambda m: m.text == "🔒 Lock")
    @owner_required(bot)
    @log_command("Lock")
    def handle_lock(message):
        cmd = LockCommand(bot, message)
        cmd.execute()


    # -------------------------------- download photo from tg -----------------------
    @bot.message_handler(content_types=["photo"])
    @owner_required(bot)
    @log_command("Receive photo")
    def handle_incoming_photo(message):
        # Берём фото лучшего качества (последнее в списке)
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)

        # Сохраняем на ПК
        save_path = f"data/photos/received_{file_id[:8]}.jpg"
        with open(save_path, "wb") as f:
            f.write(downloaded)

        bot.send_message(message.chat.id, f"✅ Photo saved to: {save_path}")

    # ----------------------------- Weather -----------------------------------
    @bot.message_handler(func=lambda m: m.text == "🌤 Weather")
    @owner_required(bot)
    @log_command("Weather")
    def handle_weather(message):
        if not owner_only(bot, message):
            return
        bot.send_message(message.chat.id, "🌍 Enter city name:")
        bot.register_next_step_handler(message, _get_weather)

    def _get_weather(message):
        log_action(message.from_user.id, f"Weather: {message.text}")
        cmd = WeatherCommand(bot, message, message.text)
        cmd.execute()