import requests
from bs4 import BeautifulSoup as bs 
import json



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
	soup = get_page(page)
	return [get_img(soup),get_names(soup),get_rate(soup),get_opis(soup)]

#--------------------------------------------

def pars_page(page,artic):
	return bs(requests.get(pars_url.format(page,artic)).content,'html5lib')

def pars_imgs(soup):
	return [i.get('src') for i in soup.find_all('img',class_='img')]

def pars_data(page,artic):
	soup = pars_page(page,artic)
	return pars_imgs(soup)
