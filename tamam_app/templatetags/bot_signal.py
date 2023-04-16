from django import template
from django.contrib.auth.models import Group
import telebot
import requests
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')
TOKEN = config['TELEBOT']['token']


bot = telebot.TeleBot(TOKEN)


labazan_test = config['TELEBOT']['labazan_test']
base_chat = config['TELEBOT']['base_chat']
turkmen = config['TELEBOT']['turkmen']

register = template.Library()

@register.simple_tag
def bot_first_signal():
	print('!внутри бота!')
	alert_sms = 'Сработало нажатие кнопки "Купить игру" на первой странице сайта.'
	url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={base_chat}&parse_mode=html&text={alert_sms}'
	#r = requests.get(url)
	#print(r.text)

@register.simple_tag
def bot_second_signal():
	print('!внутри бота!')
	alert_sms = 'Код красный! Клиент прикрепил чек с оплатой игры! Срочно требуется проверить чек на валидность!'
	url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={base_chat}&parse_mode=html&text={alert_sms}'
	#r = requests.get(url)
	#print(r.text)

@register.simple_tag
def bot_final_signal():
	print('!внутри бота!')
	alert_sms = 'Ахтунг! Клиент подтвердил оплату!'
	url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={base_chat}&parse_mode=html&text={alert_sms}'
	#r = requests.get(url)
	#print(r.text)

