from telebot import *
from telebot.types import *
import parss, requests
bot = TeleBot('5606053767:AAGG0tLtbowLQGKZAkrLtNNwu41WyggL2zk')

uda = []
mda = []
pda = []

main_kb = types.InlineKeyboardMarkup().add(*[
				types.InlineKeyboardButton(text='◀️ Назад',callback_data='back'),
				types.InlineKeyboardButton(text='Читать 👁',callback_data='read'),
				types.InlineKeyboardButton(text='Далее ▶️',callback_data='next'),
				types.InlineKeyboardButton(text='🗑 Удалить',callback_data='clear'),

				
			])

read_kb = types.InlineKeyboardMarkup().add(*[
				types.InlineKeyboardButton(text='⬅️ Назад',callback_data='back_man'),
				types.InlineKeyboardButton(text='❌ Манга',callback_data='close'),
				types.InlineKeyboardButton(text='➡️ Далее',callback_data='next_man'),
				types.InlineKeyboardButton(text='🗑 Удалить',callback_data='clear'),
			])

def check_uda(id):
	for i in uda:
		if i.split('|')[0] == str(id):
			return i.split('|')[1]
	return 0

def write_uda(id,mang):
	uda.append(f'{id}|{mang}')

def change_uda(id,mang,to):
	uda[uda.index(f'{id}|{mang}')] = f'{id}|{to}'

def back(id,mang):
	if int(mang) == 1:
		return 1
	else:
		change_uda(id,int(mang),int(mang)-1)
		return int(mang)-1

def next(id,mang):
	change_uda(id,int(mang),int(mang)+1)
	return int(mang)+1
#------------------------------------------
def check_mda(id): # id|page|articul
	for i in mda:
		if i.split('|')[0] == str(id):
			return i.split('|')[1:]
	return 0

def write_mda(id,mang):
	mda.append(f'{id}|{mang}')

def change_mda(id,mang,to):
	mda[mda.index(f'{id}|{mang}')] = f'{id}|{to}'

def backm(id,mang):
	if int(mang) == 1:
		return 1
	else:
		change_mda(id,int(mang),int(mang)-1)
		return int(mang)-1

def nextm(id,mang):
	change_mda(id,int(mang),int(mang)+1)
	return int(mang)+1

def del_mda(id):
	for i in mda:
		if i.split('|')[0] == str(id):
			mda.pop(mda.index(i))

def apda(id):
	for i in pda:
		if i.get('id',False) != False:
			return 0
	pda.append({'id': int(id),'man':[], 'on': 0})

def pda_get(id,mas='',on=''):
	for i in pda:
		if i.get('id',False) != False:
			if mas != '':
				return i.get('mas',[])
			else:
				return i.get('on',1)
			
	apda(id)

def pda_set(id,mas='',on=''):
	for i in pda:
		if i.get('id',False) != False:
			if mas != '':
				i['mas'] = mas
			elif on != '':
				i['on'] = on
			else:
				print('ERROR, Why? ON ?? MAS??')
			return 0
	apda(id)

@bot.message_handler(commands=['start'])
def add_user(message):
	bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
	apda(message.chat.id)
	if check_uda(message.chat.id) == 0:
		write_uda(message.chat.id,1)
		f = 1
	else:
		f = int(check_uda(message.chat.id))
	del_mda(message.chat.id)
	fdata = parss.get_data(f)
	read_urlic = parss.read_urlic.format(str(f))
	bot.send_message(message.chat.id,
		'<b>{}<a href="{}">ㅤ</a></b>\n\nРейтинг: <code>{}</code>\nОписание: <i>{}</i>\n\n<a href="{}">Читать на сайте</a>'.format(
			fdata[1],fdata[0][1],fdata[2],fdata[3],read_urlic
			),
		parse_mode='HTML',
		reply_markup=main_kb)

@bot.message_handler(commands=['s'])
def ss(mes):
	bot.delete_message(chat_id=mes.chat.id,message_id=mes.message_id)
	del_mda(mes.chat.id)
	apda(mes.chat.id)
	if check_uda(mes.chat.id) == 0:  
		write_uda(mes.chat.id,int(mes.text.split('/s ')[1]))
	else:  change_uda(mes.chat.id,check_uda(mes.chat.id),int(mes.text.split('/s ')[1]))
	f = int(mes.text.split('/s ')[1])
	fdata = parss.get_data(f)
	read_urlic = parss.read_urlic.format(str(f))
	bot.send_message(mes.chat.id,
		'<b>{}<a href="{}">ㅤ</a></b>\n\nРейтинг: <code>{}</code>\nОписание: <i>{}</i>\n\n<a href="{}">Читать на сайте</a>'.format(
			fdata[1],fdata[0][1],fdata[2],fdata[3],read_urlic
			),
		parse_mode='HTML',
		reply_markup=main_kb)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	apda(call.message.chat.id)
	if call.data == 'next':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		next(call.message.chat.id,check_uda(call.message.chat.id))
	elif call.data == 'back':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		back(call.message.chat.id,check_uda(call.message.chat.id))


	if call.data in ['next','back']:
		apda(call.message.chat.id)
		del_mda(call.message.chat.id)
		if check_uda(call.message.chat.id) == 0:
			write_uda(call.message.chat.id,1)
			f = 1
		else:
			f = int(check_uda(call.message.chat.id))
		fdata = parss.get_data(f)
		read_urlic = parss.read_urlic.format(str(f))
		bot.send_message(call.message.chat.id,
			'<b>{}<a href="{}">ㅤ</a></b>\n\nРейтинг: <code>{}</code>\nОписание: <i>{}</i>\n\n<a href="{}">Читать на сайте</a>'.format(
				fdata[1],fdata[0][1],fdata[2],fdata[3],read_urlic
				),
			parse_mode='HTML',
			reply_markup=main_kb)

	if call.data == 'read':
		try:
			apda(call.message.chat.id)
			write_mda(call.message.chat.id,f'{check_uda(call.message.chat.id)}|1')
			bot.edit_message_text(chat_id=call.message.chat.id,
				message_id=call.message.message_id,
				text='⌚️ Ожидайте Загрузки...'
				)
			pdata = parss.pars_data(int(check_uda(call.message.chat.id)),int(1))
			pda_set(call.message.chat.id,mas = pdata)
			pda_set(call.message.chat.id,on=1)
			print(mda,pdata)
			bot.send_photo(
				chat_id=call.message.chat.id,
				photo=requests.get(pdata[0]).content,
				reply_markup=read_kb,
				parse_mode='HTML',
				caption=f"<a href='https://any-more.ru/manga/?manga=1-{check_uda(call.message.chat.id)}'>Читать на сайте</a>"
				)
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		except Exception as error:
			print(error, pdata[0])
			try:
				bot.send_message(
				call.message.chat.id,
				reply_markup=read_kb,
				parse_mode='HTML',
				text=f"<a href='{pdata[1]}'>ㅤ</a>\nПроизошла техническая неполадка, приносим свои извенения, но телеграм не в силах отобразить такую большую фотографию, лучше читать на сайте, сделать это вы сожете в меню манги."
				)
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			except Exception as error:
				print(error)
				bot.send_message(call.message.chat.id,'Нажмите на /start , у нас ,увы, временные неполадки с этой мангой в боте, но вы так-же можете прочитать её на нашем сайте https://any-more.ru')


	if call.data == 'next_man':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		if len(pda_get(call.message.chat.id,mas=True)) > pda_get(call.message.chat.id,on=True):
			
			try:
				bot.send_photo(
				call.message.chat.id,
				requests.get(pda_get(call.message.chat.id,mas=True)[int(pda_get(call.message.chat.id,on=True))]).content,
				reply_markup=read_kb,
				parse_mode='HTML',
				caption=f"<a href='https://any-more.ru/manga/?manga=1-{check_uda(call.message.chat.id)}'>Читать на сайте</a>"
			)
			except:
				bot.send_message(
					call.message.chat.id,
					reply_markup=read_kb,
					parse_mode='HTML',
					text=f"{pda_get(call.message.chat.id,mas=True)[int(pda_get(call.message.chat.id,on=True))]}\nПроизошла техническая неполадка, приносим свои извенения, но телеграм не в силах отобразить такую большую фотографию, лучше читать на сайте, сделать это вы сожете в меню манги."
					)
			pda_set(call.message.chat.id,on=int(pda_get(call.message.chat.id,on=True))+1)
		else:
			apda(call.message.chat.id)
			change_mda(id=call.message.chat.id,
				mang=f'{check_uda(call.message.chat.id)}|{int(check_mda(call.message.chat.id)[::-1][0])}',
				to=f'{check_uda(call.message.chat.id)}|{int(check_mda(call.message.chat.id)[::-1][0])+1}')
			pdata = parss.pars_data(int(check_uda(call.message.chat.id)),int(check_mda(call.message.chat.id)[::-1][0])+1)
			pda_set(call.message.chat.id,mas = pdata)
			pda_set(call.message.chat.id,on=1)
			print(mda,pdata)
			try:
				bot.send_photo(
					call.message.chat.id,
					requests.get(pdata[0]).content,
					reply_markup=read_kb,
					parse_mode='HTML',
					caption=f"<a href='https://any-more.ru/manga/?manga=1-{check_uda(call.message.chat.id)}'>Читать на сайте</a>"
					)
			except:
				bot.send_message(
					call.message.chat.id,
					reply_markup=read_kb,
					parse_mode='HTML',
					text=f"{pdata[0]}\nПроизошла техническая неполадка, приносим свои извенения, но телеграм не в силах отобразить такую большую фотографию, лучше читать на сайте, сделать это вы сожете в меню манги."
					)

	if call.data == 'back_man':
		if int(pda_get(call.message.chat.id,on=True)) != 1:
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			pda_set(call.message.chat.id,on=int(pda_get(call.message.chat.id,on=True))-1)
			try:
				bot.send_photo(
					call.message.chat.id,
					requests.get(pda_get(call.message.chat.id,mas=True)[int(pda_get(call.message.chat.id,on=True))-1]).content,
					reply_markup=read_kb,
					parse_mode='HTML',
					caption=f"<a href='https://any-more.ru/manga/?manga=1-{check_uda(call.message.chat.id)}'>Читать на сайте</a>"
				)
			except:
				bot.send_message(
					call.message.chat.id,
					reply_markup=read_kb,
					parse_mode='HTML',
					text=f"{pda_get(call.message.chat.id,mas=True)[int(pda_get(call.message.chat.id,on=True))-1]}\nПроизошла техническая неполадка, приносим свои извенения, но телеграм не в силах отобразить такую большую фотографию, лучше читать на сайте, сделать это вы сожете в меню манги."
					)

			print(pda)
		elif int(check_mda(call.message.chat.id)[::-1][0]) > 1:
			apda(call.message.chat.id)
			change_mda(id=call.message.chat.id,
				mang=f'{check_uda(call.message.chat.id)}|{int(check_mda(call.message.chat.id)[::-1][0])}',
				to=f'{check_uda(call.message.chat.id)}|{int(check_mda(call.message.chat.id)[::-1][0])-1}')
			pdata = parss.pars_data(int(check_uda(call.message.chat.id)),int(check_mda(call.message.chat.id)[::-1][0])-1)
			pda_set(call.message.chat.id,mas = pdata)
			pda_set(call.message.chat.id,on=1)
			print(mda,pdata)
			try:
				bot.send_photo(
					call.message.chat.id,
					requests.get(pdata[0]).content,
					reply_markup=read_kb,
					parse_mode='HTML',
					caption=f"<a href='https://any-more.ru/manga/?manga=1-{check_uda(call.message.chat.id)}'>Читать на сайте</a>"
					)
			except:
				bot.send_message(
					call.message.chat.id,
					reply_markup=read_kb,
					parse_mode='HTML',
					text=f"{pdata[0]}\nПроизошла техническая неполадка, приносим свои извенения, но телеграм не в силах отобразить такую большую фотографию, лучше читать на сайте, сделать это вы сожете в меню манги."
					)
		else:
			bot.answer_callback_query(callback_query_id=call.id, text='Это первая глава, назад - только в меню (❌)')

			
	if call.data == 'close':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		apda(call.message.chat.id)
		del_mda(call.message.chat.id)
		f = int(check_uda(call.message.chat.id))
		fdata = parss.get_data(f)
		read_urlic = parss.read_urlic.format(str(f))
		bot.send_message(call.message.chat.id,
			'<b>{}<a href="{}">ㅤ</a></b>\n\nРейтинг: <code>{}</code>\nОписание: <i>{}</i>\n\n<a href="{}">Читать на сайте</a>'.format(
				fdata[1],fdata[0][1],fdata[2],fdata[3],read_urlic
				),
			parse_mode='HTML',
			reply_markup=main_kb)

	if call.data == 'clear':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		bot.answer_callback_query(callback_query_id=call.id, text='Вы, как обычно, просто удалили сообщение')




bot.polling(non_stop=True)