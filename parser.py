from random import choice
import requests
from bs4 import BeautifulSoup
from commands import add_link, del_link
from models.models import session, Link


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


city = 'Калуга'     # город парсинга
category = 'Здоровье'   # категория парсинга: 'Красота', 'Рестораны', 'Здоровье', 'Развлечения', 'Авто', 'Дети', 'Разное', 'Отели'
domen = 'https://kaluga.biglion.ru'  # домен для итоговой ссылки
url = 'https://webcache.googleusercontent.com/search?q=cache:noodtlQOA9IJ:https://kaluga.biglion.ru/services/health/&cd=8&hl=ru&ct=clnk&gl=ru'  # ссылка для парсинга


r = requests.get(url, headers=random_headers(), timeout=20)
soup_ing = str(BeautifulSoup(r.content, 'lxml'))
soup_ing = soup_ing.encode()
with open("test.html", "wb") as file:
    file.write(soup_ing)

s = set()  # множество для добавление напарсинных ссылок


def fromSoup():
    html_file = ("test.html")
    html_file = open(html_file, encoding='UTF-8').read()
    soup = BeautifulSoup(html_file, 'lxml')
    c = '/deals/'
    for link in soup.find_all('a'):
        if c in str(link.get('href'))[:7]:
            s.add(domen + link.get('href') + '?utm_campaign=p4793100&utm_medium=cpa&utm_source=p4793100')  # формируем и добавляем итоговые ссылки


fromSoup()

del_link(city, category) # каждый раз очищаем таблицу по выбранному городу и категории

link = session.query(Link).all()
for i in s:
    add_link(i, city, category)   # добавляе актуальные ссылки по выбранному городу и категории
