from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📷 Photo"),
        types.KeyboardButton("💻 Program")
    )
    markup.add(types.KeyboardButton("📊 History"))

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

