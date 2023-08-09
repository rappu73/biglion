import os
from random import choice
import requests
from bs4 import BeautifulSoup
from commands import add_link, del_link
from models.models import session, Link

# ПАРСИНГ ПОКА ЧТО В ПОЛУРУЧНОМ РЕЖИМЕ, копирую код страницы в файл test.html. Никак не могу обойти блокировку от Biglion

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


def random_headers():
    return {'User-Agent': choice(desktop_agents), 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


city = 'Казань'     # город парсинга
category = 'Здоровье'   # категория парсинга: 'Красота', 'Рестораны', 'Здоровье', 'Развлечения', 'Авто', 'Дети', 'Разное', 'Отели'
domen = 'https://kazan.biglion.ru'  # поддомен для итоговой ссылки на акцию


# url = 'view-source:https://kaluga.biglion.ru/services/'  # ссылка из кеша гугла или яндекса для парсинга
# r = requests.get(url, headers=random_headers(), timeout=20)
# soup_ing = str(BeautifulSoup(r.content, 'lxml'))
# soup_ing = soup_ing.encode()
# with open("test.html", "wb") as file:
#     file.write(soup_ing)

link_data = []   # список с ссылками
img_data = []   # список с путем до картинки
title_data = []  # список с названиями


# Парсим ссылки
def fromSoupLink():
    html_file = ("test.html")
    html_file = open(html_file, encoding='UTF-8').read()
    soup = BeautifulSoup(html_file, 'lxml')
    c = '/deals/'
    for link in soup.find_all('a'):
        if c in str(link.get('href'))[:7]:
            link_finish = domen + link.get('href') + '?utm_campaign=p4793100&utm_medium=cpa&utm_source=p4793100' # Формируем итоговую ссылку на акцию
            if link_finish not in link_data:
                link_data.append(link_finish)  # Добавляем в список с ссылками


# Парсим картинки
def fromSoupIMG():
    html_file = ("test.html")
    html_file = open(html_file, encoding='UTF-8').read()
    soup = BeautifulSoup(html_file, 'lxml')
    if not os.path.exists(f'media\{city}'):  # Проверяем есть ли каталог с городом. Если нет, то создаём его
        os.mkdir(f'media\{city}')
    if not os.path.exists(f'media\{city}\{category}'): # Проверяем есть ли каталог с категорией. Если нет, то создаём его
        os.mkdir(f'media\{city}\{category}')
    g = '.jpg'
    i = 0  # Счётчик для названия картинок. Прибавляется к названию
    for img in soup.find_all('img'):
        if g in img.get('data-src'):
            img = 'https:' + img.get('data-src')  # Формируем ссылку на картинку
            img_data.append(f'media\{city}\{category}\img{i+1}.jpg')  # Добавляем в список с картинками

            p = requests.get(img)
            with open(f'media\{city}\{category}\img{i+1}.jpg', "wb") as out: # Скачиваем картинку себе в соответсвующий каталог Город/Категория
                out.write(p.content)
                out.close()
                i = i + 1


# Парсим названия
def fromSoupTitle():
    html_file = ("test.html")
    html_file = open(html_file, encoding='UTF-8').read()
    soup = BeautifulSoup(html_file, 'lxml')
    g = '.jpg'
    for title in soup.find_all('img'):
        if g in title.get('data-src'):
            if title.get('alt') not in title_data:
                title_data.append(title.get('alt'))  # Добавляем в список с названиями


fromSoupLink()
fromSoupIMG()
fromSoupTitle()

del_link(city, category)  # Каждый раз очищаем таблицу для выбранного города и категории


# Добавляем в таблицу напарсенные данные из списков: Ссылка, Картинка, Название
link = session.query(Link).all()
el = 0 # Счётчик для передобора по таблице
for link_name in link_data:
    if el < len(title_data):
        add_link(link_name, img_data[el], title_data[el], city, category)
        el = el + 1
