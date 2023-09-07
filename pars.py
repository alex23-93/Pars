import requests
from bs4 import BeautifulSoup
from time import sleep
from fake_useragent import UserAgent  # ЗАПОМНИ

ua = UserAgent()
headers = {'accept': '*/*', 'user-agent': ua.firefox}  # ЗАПОМНИ


def get_url():
    for count in range(1, 7):
        url = f'https://scrapingclub.com/exercise/list_basic/?page={count}'

        response = requests.get(url, headers=headers)  # Получаем инфу с сайта

        soup = BeautifulSoup(response.text, 'lxml')  # Преобразуем инфу в нормальную html страницу

        data = soup.find_all('div', class_="w-full rounded border")
        """ find - позволяет найти интересующий элемент. 
        Тут мы ищем все тэги див с конкретным классом 
        (после слова class ставится нижнее подчеркивание ) """
        for i in data:
            card = 'https://scrapingclub.com' + i.find('a').get('href')
            yield card  # Это делает функцию генератором (вместо return yield)

            # name = i.find('h4').text  # добавляем в конце текст чтобы получить только текст тэга
            # price = i.find('h5').text
            #
            # url_img = 'https://scrapingclub.com' + i.find('img').get('src')
            # """получаем ссылку на фото, (в тэге img есть ссылка на фото (src) которую мы берем через гет)
            # но перед этим нужно добавить адрес сайта"""
            #
            # print(url_img + name + price + '\n')


for ii in get_url():
    response = requests.get(ii, headers=headers)  # Получаем инфу с сайта

    soup = BeautifulSoup(response.text, 'lxml')  # Преобразуем инфу в нормальную html страницу
    sleep(1)  # указываем перерыв в 3с чтобы нас не заблокировали

    data = soup.find('div', class_="my-8 w-full rounded border")
    name = data.find('h3').text
    price = data.find('h4').text
    text = data.find('p'). text
    url_img = 'https://scrapingclub.com' + data.find('img', class_='card-img-top').get('src')
    print(url_img + '\n' + name + '\n' + price + '\n' + text + '\n')
