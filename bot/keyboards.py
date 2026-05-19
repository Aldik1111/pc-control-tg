from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📷 Photo"),
        types.KeyboardButton("💻 Program")
    )
    markup.add(
        types.KeyboardButton("📊 History"),
        types.KeyboardButton("📝 Notes")
    )
    markup.add(
        types.KeyboardButton("📊 Stats"),
        types.KeyboardButton("⚡ Processes")
    )
    markup.add(
        types.KeyboardButton("🔴 Shutdown"),
        types.KeyboardButton("🔄 Restart")
    )

    return markup

def photo_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📸 Webcam"),
        types.KeyboardButton("🖥 Screenshot"))
    markup.add(types.KeyboardButton("🏠 Main"))
    return markup

def program_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("🌐 Chrome"),
           types.KeyboardButton("🎵 Spotify"))
    markup.add(
        types.KeyboardButton("🎮 Steam"),
        types.KeyboardButton("🐍 Pycharm"))
    markup.add(
        types.KeyboardButton("🔧 Other"),
        types.KeyboardButton("❌ Close")
    )
    markup.add(types.KeyboardButton("🏠 Main"))
    return markup

def notes_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("➕ Add note"),
        types.KeyboardButton("🗑 Delete note")
    )
    markup.add(types.KeyboardButton("📋 All notes"))
    markup.add(types.KeyboardButton("🏠 Main"))
    return markup

