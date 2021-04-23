import telebot
import requests
import json
from models import News
from db import DbConnection
from redis_r import r
from config import TOKEN_TELEGRAM_BOT
from telebot import types
from config import OPEN_WEATHER_TOKER


bot = telebot.TeleBot(TOKEN_TELEGRAM_BOT)
DbConnection.dbhandle.connect()


def get_temp_from_sity(sity):
    param = {'q': sity, 'appid': OPEN_WEATHER_TOKER, 'units': 'metric'}
    req = requests.get(
        'https://api.openweathermap.org/data/2.5/weather', params=param)
    result = json.loads(req.text)
    temp = result['main']['temp']
    return temp


def get_main_keyboard():
    user_markup = types.ReplyKeyboardMarkup(True, True)
    user_markup.row("Погода", "Новости о боте")
    return user_markup


@bot.message_handler(commands=["start"])
def start_message(message):
    user_markup = get_main_keyboard()
    bot.send_message(message.chat.id, "Добрый день", reply_markup=user_markup)


@bot.message_handler(regexp="Новости о боте")
def weather_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    news_all = News.select()
    for news in news_all:
        bot.send_message(message.chat.id, "Заголовок: {} \nСодержание: {} \nДата публикации: {}".format(
            news.name, news.text, news.created_at))


@bot.message_handler(regexp="Погода")
def weather_message(message):
    bot.send_message(message.chat.id, "Введите ваш город: ")
    bot.register_next_step_handler(
        message, set_period_weather)


def set_period_weather(message):
    r.set(message.chat.id, message.text)

    user_markup = types.ReplyKeyboardMarkup(True, True)
    user_markup.row("Сейчас", "Неделя")

    bot.send_message(message.chat.id, "Выберите период",
                     reply_markup=user_markup)
    bot.register_next_step_handler(message, get_weather)


def get_weather(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sity = r.get(message.chat.id)
    per = message.text
    user_markup = get_main_keyboard()
    if per == 'Сейчас':
        temp = get_temp_from_sity(sity)
        bot.send_message(message.chat.id, "{} в {} : {} градусов по цельсию".format(
            per, sity, temp),  reply_markup=user_markup)
    else:
        bot.send_message(
            message.chat.id, "Пока я такого не умею, следите за новостями",  reply_markup=user_markup)


bot.polling()
