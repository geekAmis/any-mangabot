import requests
from bs4 import BeautifulSoup as bs 
import json, random



url = 'https://any-more.ru/manga/?manga=1-{}'
read_urlic = 'https://any-more.ru/manga/1-{}/1_index.php'
pars_url = 'https://any-more.ru/manga/1-{}/{}_index.php'

def get_page(page):
	return bs(requests.get(url.format(page)).content,'html5lib')

def get_img(soup):
	soup = str(soup).replace("""<!DOCTYPE html>
<html lang="zxx"><head><style type="text/css">.select select {display: block;width: 22.2%; /* от ширины блока div */padding: .75rem 2.5rem .75rem 1rem;/* отступы от текста до рамки */background: white; /* убираем фон */border: 3px solid #ccc; /* рамка */border-radius: 6px;/* скругление полей формы */-webkit-appearance: none;/* Chrome */-moz-appearance: none;/* Firefox */appearance: none;/* убираем дефолнтные стрелочки */font-family: inherit;/* наследует от родителя */font-size: 1rem;color: #444;text-align: left;}.example > .block > .side {animation: animation-demon 4s ease;position: absolute;top: 0;left: 0;background-image: url('""",'')
	return (soup.split("');")[0],soup.split("');")[0].replace('_mini',''))

def get_names(soup):
	return soup.find('div',class_='anime__details__title').text.replace('\n','')

def get_rate(soup):
	return soup.find('div',class_='anime__details__rating').find('span').text

def get_opis(soup):
	return soup.find('div',class_='anime__details__text').find('p').text

def get_data(page):
	try:
		soup = get_page(page)

		return [get_img(soup),get_names(soup),get_rate(soup),get_opis(soup)]
	except:
		return ['https://any-more.ru/mang.png',['Не найдено','Not FOUND'],0,'ERROR CODE: 404']

#--------------------------------------------

def pars_page(page,artic):
	return bs(requests.get(pars_url.format(page,artic)).content,'html5lib')

def pars_imgs(soup):
	return [i.get('src') for i in soup.find_all('img',class_='img')]

def pars_data(page,artic):
	soup = pars_page(page,artic)
	return pars_imgs(soup)

def search_soup(s="",redirect_to="https://any-more.ru/categories.php"):
	data = {"s":s,"redirect_to": redirect_to}
	return bs(requests.post('https://any-more.ru/search/',data=data).text,'html5lib')

def search_json(soup):
	data = []
	for i in soup.find_all('div',class_='col-lg-4 col-md-6 col-sm-6'):
		data.append(
				{
					"num": i.find('a').get('href').split('?manga=1-')[1],
					"img": i.find('div',class_='product__item__pic set-bg').get('data-setbg'),
					"name": i.find('h5').text,
					"ep": i.find('div',class_='ep').text,
					"view": i.find('div',class_='view').text
				}
			)
	return data

def search_data(text=''):
	return search_json(search_soup(s=text))

def get_rand():
	soup = bs(requests.get('https://any-more.ru').text,'html5lib').find('div',class_='product__sidebar__view')
	ran = random.randint(1,int(soup.find('a',class_='primary-btn').get('href').split('categories.php?page=')[1])*10+5)
	if get_data(ran)[0] != 'https://any-more.ru/mang.png':  return ran
	else:
		print(f'Error ran - {ran}')
		return get_rand()

