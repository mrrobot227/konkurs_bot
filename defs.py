import telebot
from telebot import types
from config import *
import json
import random
from random import choice
import flask
from flask import Flask, request
import os


bot = telebot.TeleBot(token)

def dumpjs(fl):
	with open('users.json', 'w') as file:
		json.dump(fl, file, indent = 4)

def check_code_entering(message):
	fl = loadjs()
	if fl['Users'][str(message.chat.id)]['is_wrote_refcode'] == 0:
		return False
	else:
		return True	
def loadjs():
	with open('users.json', 'r') as read_file:
		fl = json.load(read_file)
	return fl
def ref_write_markup():

	inline_markup = types.InlineKeyboardMarkup()
	inline_markup.add(types.InlineKeyboardButton(text = 'Ввести реферальный код', callback_data = 'entercode'))
	inline_markup.add(types.InlineKeyboardButton(text = 'Мой реферальный код', callback_data = 'mycode'))
	inline_markup.add(types.InlineKeyboardButton(text = 'Ссылка на общий чат', url = 'https://t.me/futures_investment'))
		
	return inline_markup

def ref_write_markup_2():

	inline_markup = types.InlineKeyboardMarkup()
	
	inline_markup.add(types.InlineKeyboardButton(text = 'Мой реферальный код', callback_data = 'mycode'))
	inline_markup.add(types.InlineKeyboardButton(text = 'Ссылка на общий чат', url = 'https://t.me/futures_investment'))
		
	return inline_markup	

def check_category(message):
	fl = loadjs()
	category = fl['Users'][str(message.chat.id)]['last_category']
	return category


def profile_markup():
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

	item_registration = types.KeyboardButton('Профиль')
	markup.add(item_registration)
	return markup

def check(message):
	fl = loadjs()
	if str(message.chat.id) in fl['Users']:
		return True
	else:
		return False	

def registration(message):

	fl = loadjs()
	data = user_data
	ref_code = ''
	data['id'] = message.chat.id
	for i in range(10):
		ref_code += random.choice(chars)
	data['ref_code'] = ref_code

	fl['Users'][str(message.chat.id)] = data
	dumpjs(fl)

	with open('ref_codes.json', 'r') as file:
		codes = json.load(file)

	codes['Codes'][ref_code] = str(message.chat.id)
	with open('ref_codes.json', 'w') as file:
		json.dump(codes, file, indent = 4)

	with open('users_list.json', 'r') as dile:
		us_list = json.load(dile)

	us_list['Users_list'].append(str(message.chat.id))

	with open('users_list.json', 'w') as mile:
		json.dump(us_list, mile, indent = 4)	
#def already(message):

def enter_refcode(call):
	bot.send_message(call.message.chat.id, 'Введите реферальный код:')
	fl = loadjs()
	fl['Users'][str(call.message.chat.id)]['last_category'] = 'enter_refcode'
	dumpjs(fl)
	

def greatings(message):
	fl = loadjs()
	ref_code = fl['Users'][str(message.chat.id)]["ref_code"]
	bot.send_message(message.chat.id, f'Поздравляю, вы успешно зарегистрировались в конкурсе! Ваш реферальный код: {str(ref_code)}. Один приглашенный пользователь = 1 билет в конкурсе. Приглашайте больше людей чтобы повысить шансы на победу!\n\nПерейдите в "Профиль" - "Ввести реферальный код", введите реферальный код приласившего вас участника и получите 5 билетов!', reply_markup = profile_markup())

def already(message):

	bot.send_message(message.chat.id, 'Ваш аккаунт уже зарегистрирован в конкурсе!', reply_markup = profile_markup())

def check_code(message):
	
	fl = loadjs()
	if fl['Users'][str(message.chat.id)]['last_category'] == 'enter_refcode':
		code = message.text
		code = code.upper()
		with open('ref_codes.json', 'r') as file:
			codes_list = json.load(file)
		if code in codes_list['Codes']:
			if code != fl['Users'][str(message.chat.id)]['ref_code']:
				username = codes_list['Codes'][code]
				
				fl['Users'][username]['refferals'] += 1
				fl['Users'][username]['tickets'] += 1
				fl['Users'][username]['refferals_list'].append(str(message.chat.id))
				fl['Users'][str(message.chat.id)]['tickets'] += 5
				fl['Users'][str(message.chat.id)]['is_wrote_refcode'] = 1
				dumpjs(fl)
				bot.send_message(message.chat.id, 'Код успешно активирован!')
			else:
				bot.send_message(message.chat.id, 'Нельзя вводить свой код!')	
		elif code == 'Профиль':
			profile(message)
		else:
			bot.send_message(message.chat.id, 'Код не найден! Введите повторно')	
				


	else:
		pass	

def profile(message):
	fl = loadjs()
	user_data = fl['Users'][str(message.chat.id)]
	tickets = user_data['tickets']
	refs = user_data['refferals']
	refs_list = fl['Users'][str(message.chat.id)]['refferals_list']
	all_users = len(fl['Users'])
	active_referrals = 0
	for i in range(refs):
		referral = refs_list[i]
		if fl['Users'][referral]['refferals'] >= 3:
			active_referrals += 1

	if user_data['is_wrote_refcode'] == 0:

		bot.send_message(message.chat.id, f'👤 Профиль\n\n🎟 Билетов: {tickets}\n👫 Рефералов приведено: {refs}\n🤝 Активных рефералов: {active_referrals}\n👨‍👨‍👧‍👧 Количество участников: {all_users}\n\nВведи реферальный код и получи 5 билетов! ⬇️', reply_markup = ref_write_markup())

	else:
		bot.send_message(message.chat.id, f'👤 Профиль\n\n🎟 Билетов: {tickets}\n👫 Рефералов приведено: {refs}\n🤝 Активных рефералов: {active_referrals}\n👨‍👨‍👧‍👧 Количество участников: {all_users}', reply_markup = ref_write_markup_2())	

	fl['Users'][str(message.chat.id)]['last_category'] = 'profile'
	dumpjs(fl)


def print_refcode(call):
	
	fl = loadjs()
	bot.send_message(call.message.chat.id, fl['Users'][str(call.message.chat.id)]['ref_code'])	

def check_notif(message):
	
	fl = loadjs()
	if fl['Users'][str(message.chat.id)]['notification'] == 0:
		return False
	else:
		return True		

def send_notif(message):
	
	bot.send_message(message.chat.id, 'Друзья, напоминаю, что одним из условий участия в конкурсе является вступление в наш групповой чат! Если вы не сделали этого, то перейдите в "Профиль" - "Ссылка на общий чат" и присоединяйтесь!')
	fl = loadjs()
	fl['Users'][str(message.chat.id)]['notification'] = 1
	dumpjs(fl)		