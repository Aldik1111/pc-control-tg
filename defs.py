import telebot
import os
import cv2
import time
import pyautogui
from telebot import types
import webbrowser

bot = telebot.TeleBot('8703257889:AAHPprPSe5I6cR3epj19IBfUbNQMaw1JyoE')

def Photo(message): # Кнопки для фото. Веб камера и скриншот
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("web")
    btn2 = types.KeyboardButton("screen")
    btn3 = types.KeyboardButton("Main")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "Photo", reply_markup=markup)

def Open_program(message): # Кнопки для открытия программ
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Tlauncher")
    btn2 = types.KeyboardButton("VS Code")
    btn3 = types.KeyboardButton("SMS / Social Media")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "Open Programs", reply_markup=markup)

def Close_program(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Tlauncher")
    btn2 = types.KeyboardButton("VS Code")
    btn3 = types.KeyboardButton("SMS / Social Media")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "CLose Programs", reply_markup=markup)

def socmedia(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Telegram")
    btn2 = types.KeyboardButton("Discord")
    btn3 = types.KeyboardButton("Main")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "Open Social media", reply_markup=markup)

def web_photo(message): # Сделать фото из веб камеры
    web = "web.png"
    cap = cv2.VideoCapture(0)

    for i in range(30):
        cap.read()
    ret, frame = cap.read()

    cv2.imwrite(web, frame)
    with open(web, 'rb') as webcamera:
        bot.send_photo(message.chat.id, webcamera)

    time.sleep(0.2)
    os.remove(web)
    cap.release()

def screen(message): # Сделать скриншот
    time.sleep(3)
    screenshot_path = "screenshot.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)

    with open(screenshot_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    os.remove(screenshot_path)

def browse(message):
    webbrowser.open_new(message.text)