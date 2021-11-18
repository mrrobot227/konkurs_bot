from defs import *

server = Flask(__name__)




if __name__ == '__main__':
	server.run(host = '0.0.0.0', port = int(os.environ.get('PORT', '5000')))


@bot.message_handler(content_types = ['text'])
def start(message):
	if message.text == '/start':
		
		if check(message) == False:
			#enter_refcode(message)
			registration(message)
			greatings(message)
		else:
			already(message)

	if message.text == 'Профиль':
		if check(message) == True:
			profile(message)
		else:
			pass

	else:
		if check_code_entering(message) == False:

			check_code(message)
		else:	
			if check_category(message) == 'enter_refcode':
				bot.send_message(message.chat.id, 'Код уже активирован!')		
			else:
				pass

	if check_notif(message) == False:

		send_notif(message)				

@bot.callback_query_handler(func = lambda call : True)
def start_call(call):
	if call.data == 'entercode':
		fl = loadjs()
		if fl['Users'][str(call.message.chat.id)]['is_wrote_refcode'] == 0:
			enter_refcode(call)
		else:
			pass	

	if call.data == 'mycode':
		print_refcode(call)

		

@server.route('/' + token, methods = ['POST'])
def get_message():
	json_string = request.get_data().decode('utf-8')
	update = telebot.types.Update.de_json(json_string)
	bot.process_new_updates([update])
	return '!', 200

@server.route('/')
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url = APP_URL)
	return '!', 200	



#bot.polling(none_stop = True, timeout = 100000)
