from telebot import *
from telebot.types import *
import parss, requests,random

#Main per
bot = TeleBot('5606053767:AAEq7OXIYEQ70QRc4kFw3WGCCbjhLFOiY4I')
uda = []
mda = []
pda = []

#keyboard
main_kb = types.InlineKeyboardMarkup().add(*[
				types.InlineKeyboardButton(text='◀️ Назад',callback_data='back'),
				types.InlineKeyboardButton(text='Читать 👁',callback_data='read'),
				types.InlineKeyboardButton(text='Далее ▶️',callback_data='next'),
				types.InlineKeyboardButton(text='🗑 Удалить',callback_data='clear'),

				
			])

clear_kb = types.InlineKeyboardMarkup().add(*[types.InlineKeyboardButton(text='🗑 Удалить',callback_data='clear')])

read_kb = types.InlineKeyboardMarkup().add(*[
				types.InlineKeyboardButton(text='⬅️ Назад',callback_data='back_man'),
				types.InlineKeyboardButton(text='❌ Обложка',callback_data='close'),
				types.InlineKeyboardButton(text='➡️ Далее',callback_data='next_man'),
				types.InlineKeyboardButton(text='🗑 Удалить',callback_data='clear'),
			])

def search_kb(num):
	return types.InlineKeyboardMarkup(row_width=1).add(*[
				types.InlineKeyboardButton(text='Читать 👁',callback_data=f'reads_{num}'),
				types.InlineKeyboardButton(text='🗑 Удалить',callback_data='clear'),	
			])

def test_kb(id,num=1):
	mang_but=[
				types.InlineKeyboardButton(text=f'{i}№ Читать 👁',callback_data=f'reads_{i}') for i in range(num,num+96)
			]
	mang_but.append(types.InlineKeyboardButton(text='🗑 Удалить',callback_data='clear'))
	bot.send_message(id,f'Все номера от {num} до {num+95}',reply_markup=types.InlineKeyboardMarkup(row_width=8).add(*mang_but))


#database on json
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

def loading_answer(id):
	bot.answer_callback_query(callback_query_id=id, text='Загрузка ... Ожидайте, она быстрая.')

#commands ,bot body
@bot.message_handler(commands=['start'])
def add_user(message):
	bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
	apda(message.chat.id)
	if check_uda(message.chat.id) == 0:
		write_uda(message.chat.id,1)
		f = 1
		bot.send_message(message.chat.id,'<code>Copyright ©2022 </code><a gref="https://any-more.ru">FRG-TEAM</a>',parse_mode='HTML')
	else:
		f = int(check_uda(message.chat.id))
		#i=1
		#while i+96 < 260:
		#	test_kb(message.chat.id,i)
		#	i+=96

	del_mda(message.chat.id)
	fdata = parss.get_data(f)
	read_urlic = parss.read_urlic.format(str(f))
	bot.send_message(message.chat.id,
		'<b>{}<a href="{}">ㅤ</a></b>\n\nРейтинг: <code>{}</code>\nОписание: <i>{}</i>\n\n<a href="{}">Читать на сайте</a>\n\nКороткая команда для выбора этой манги: <code>/s {}</code>'.format(
			fdata[1],fdata[0][1],fdata[2],fdata[3],read_urlic,f
			),
		parse_mode='HTML',
		reply_markup=main_kb)

@bot.message_handler(commands=['s'])
def ss(mes):
	bot.delete_message(chat_id=mes.chat.id,message_id=mes.message_id)
	del_mda(mes.chat.id)
	apda(mes.chat.id)
	if ' ' not in mes.text:
		return bot.send_message(mes.chat.id,
			f'<i>Для использования команды поиска по номеру вы должны </i><b><u>указать номер манги через пробел после команды.</u></b>\n\nПример: <code>/s {random.randint(1,200)}</code>',parse_mode='HTML'
			,reply_markup=clear_kb)

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


@bot.message_handler(commands=['search'])
def ss(message):
	bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
	del_mda(message.chat.id)
	apda(message.chat.id)
	if ' ' not in message.text:
		return bot.send_message(message.chat.id,
			'<i>Для использования команды поиска по названию вы должны </i><b><u>указать кусок названия манги через пробел после команды.</u></b>\n\nПример: <code>/search 999</code>',parse_mode='HTML'
			,reply_markup=clear_kb)
	f = message.text.split('/search ')[1]
	jdata = parss.search_data(f)
	for jd in jdata:
		fdata = parss.get_data(int(jd.get('num',1)))
		read_urlic = parss.read_urlic.format(str(int(jd.get('num',1))))
		bot.send_message(message.chat.id,
			'<b>{}</b><a href="{}">ㅤ</a>\n\nРейтинг: <code>{}</code>\nОписание: <i>{}</i>\n\n<a href="{}">Читать на сайте</a>\n\nКороткая команда для выбора этой манги: <code>/s {}</code>'.format(
				fdata[1],fdata[0][1],fdata[2],fdata[3],read_urlic,str(int(jd.get('num',1)))
			),
			parse_mode='HTML',
			reply_markup=search_kb(int(jd.get('num',1)))
			)


@bot.message_handler(commands=['rand'])
def rand(mes):
	bot.delete_message(chat_id=mes.chat.id,message_id=mes.message_id)
	del_mda(mes.chat.id)
	apda(mes.chat.id)
	f = int(parss.get_rand())
	if check_uda(mes.chat.id) == 0:  
		write_uda(mes.chat.id,f)
	else:  change_uda(mes.chat.id,check_uda(mes.chat.id),f)
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
			'<b>{}</b><a href="{}">ㅤ</a>\n\nРейтинг: <code>{}</code>\nОписание: <i>{}</i>\n\n<a href="{}">Читать на сайте</a>\n\nКороткая команда для выбора этой манги: <code>/s {}</code>'.format(
				fdata[1],fdata[0][1],fdata[2],fdata[3],read_urlic,f),
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
			
			try:
				print(error, pdata[0])
				bot.send_message(
				call.message.chat.id,
				reply_markup=read_kb,
				parse_mode='HTML',
				text=f"{pdata[1]}\n\nПроизошла техническая неполадка, приносим свои извенения, но телеграм не в силах отобразить такую большую фотографию, лучше читать на сайте, сделать это вы сожете в меню манги."
				)
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			except Exception as error:
				print(error)
				bot.send_message(
						call.message.chat.id,
						reply_markup=read_kb,
						parse_mode='HTML',
						text=f"Манги под этим номером не существует. введите /start для возвращения в меню")
				apda(call.message.chat.id)
				del_mda(call.message.chat.id)
				change_uda(call.message.chat.id,check_uda(call.message.chat.id),int(check_uda(call.message.chat.id))-1)


	if call.data == 'next_man':
		loading_answer(call.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		try:
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
		except:
			bot.send_message(
						call.message.chat.id,
						reply_markup=read_kb,
						parse_mode='HTML',
						text=f"Манги под этим номером не существует. введите /start для возвращения в меню")
			apda(call.message.chat.id)
			del_mda(call.message.chat.id)
			change_uda(call.message.chat.id,check_uda(call.message.chat.id),int(check_uda(call.message.chat.id))-1)

	if call.data == 'back_man':
		loading_answer(call.id)
		try:
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
					try:
						bot.send_message(
							call.message.chat.id,
							reply_markup=read_kb,
							parse_mode='HTML',
							text=f"{pdata[0]}\nПроизошла техническая неполадка, приносим свои извенения, но телеграм не в силах отобразить такую большую фотографию, лучше читать на сайте, сделать это вы сожете в меню манги."
							)
					except:
						bot.send_message(
							call.message.chat.id,
							reply_markup=read_kb,
							parse_mode='HTML',
							text=f"Манги под этим номером не существует. введите /start для возвращения в меню")
						apda(call.message.chat.id)
						del_mda(call.message.chat.id)
						change_uda(call.message.chat.id,check_uda(call.message.chat.id),int(check_uda(call.message.chat.id))-1)

			else:
				bot.answer_callback_query(callback_query_id=call.id, text='Это первая глава, назад - только в меню (❌)')
		except:
			bot.send_message(
						call.message.chat.id,
						reply_markup=read_kb,
						parse_mode='HTML',
						text=f"Манги под этим номером не существует. введите /start для возвращения в меню")
			apda(call.message.chat.id)
			del_mda(call.message.chat.id)
			change_uda(call.message.chat.id,check_uda(call.message.chat.id),int(check_uda(call.message.chat.id))-1)
			
	if call.data == 'close':
		loading_answer(call.id)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		apda(call.message.chat.id)
		del_mda(call.message.chat.id)
		f = int(check_uda(call.message.chat.id))
		fdata = parss.get_data(f)
		read_urlic = parss.read_urlic.format(str(f))
		bot.send_message(call.message.chat.id,
			'<b>{}</b><a href="{}">ㅤ</a>\n\nРейтинг: <code>{}</code>\nОписание: <i>{}</i>\n\n<a href="{}">Читать на сайте</a>\n\nКороткая команда для выбора этой манги: <code>/s {}</code>'.format(
				fdata[1],fdata[0][1],fdata[2],fdata[3],read_urlic,f),
			parse_mode='HTML',
			reply_markup=main_kb)

	if call.data == 'clear':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		bot.answer_callback_query(callback_query_id=call.id, text='Вы, как обычно, просто удалили сообщение')

	if 'reads_' in call.data:
		try:
			loading_answer(call.id)
			apda(call.message.chat.id)
			change_uda(call.message.chat.id,int(check_uda(call.message.chat.id)),int(call.data.split('_')[1]))
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
				text=f"{pdata[1]}\n\nПроизошла техническая неполадка, приносим свои извенения, но телеграм не в силах отобразить такую большую фотографию, лучше читать на сайте, сделать это вы сожете в меню манги."
				)
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			except Exception as error:
				print(error)
				bot.send_message(call.message.chat.id,'Нажмите на /start , у нас ,увы, временные неполадки с этой мангой в боте, но вы так-же можете прочитать её на нашем сайте https://any-more.ru')




bot.polling(non_stop=True)
