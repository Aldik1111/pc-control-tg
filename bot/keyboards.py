from telebot import types

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Photo"))
    markup.add(types.KeyboardButton("Open Program"))
    markup.add(types.KeyboardButton("Exit"))
    return markup

def photo_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Web"))
    markup.add(types.KeyboardButton("Screen"))
    markup.add(types.KeyboardButton("Main"))
    return markup

def program_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("1"))
    markup.add(types.KeyboardButton("2"))
    markup.add(types.KeyboardButton("3"))
    markup.add(types.KeyboardButton("4"))
    markup.add(types.KeyboardButton("Main"))
    return markup

