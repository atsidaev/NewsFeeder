from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import telebot

from urllib.request import urlopen
from bs4 import BeautifulSoup

from storage.inmemory_storage import InmemoryStorage
from exports.export_base import ExportBase

bot = telebot.TeleBot('942366907:AAG3-yvksu0jZn0DVNULD75XDT-fP7eU8OE')

class TelegramExport(ExportBase):
    def __init__(self, username):
        self.username = username
    def get_key(self):
        return 'telegram'
        
    def get_news(message, feed_element):
        bot.send_message(message.chat.id, feed_element.date + feed_element.author)
        if feed_element.body:
			bot.send_message(message.chat.id, feed_element.body)
        for image in feed_element.images:
            bot.send_message(message.chat.id, base64.b64encode(image.file_contents).decode("utf-8"))

      

    def export(self, feed_element):
        updater = Updater('942366907:AAG3-yvksu0jZn0DVNULD75XDT-fP7eU8OE') #http://t.me/BotForNews_bot ссылка на бота
        updater.dispatcher
        dp.add_handler(CommandHandler('news',get_news(message, feed_element)))
        updater.start_polling()
        updater.idle()