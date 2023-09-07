from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import csv

alf = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ'
ua = UserAgent
headers = {'accept': '*/*', 'user-agent': ua.firefox}


def pars():

    with open('num_animal.csv', 'w', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            [
                'Буква:',
                'Кол-во',
            ]
        )

    for coun in alf:
        number = 0
        urla = f'https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%' \
               f'80%D0%B8%D1%8F%3A%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%' \
               f'D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from={coun}'

        response = requests.get(urla, headers)
        soup = BeautifulSoup(response.text, 'lxml')
        data1 = soup.find('div', class_='mw-category mw-category-columns')
        animals = data1.find_all('li')

        for i in animals:
            i = i.text.strip()
            if str(i[0]) == coun:
                number += 1
            else:
                break

        lock = True
        while lock:

            data2 = soup.find('div', id='mw-pages')
            teg_a = data2.find_all('a')
            url_next_page = ''
            for next_page in teg_a:
                page = next_page.text
                if page == 'Следующая страница':
                    url_next_page += 'https://ru.wikipedia.org/' + next_page.get('href')

            response = requests.get(url_next_page, headers)
            soup = BeautifulSoup(response.text, 'lxml')
            data1 = soup.find('div', class_='mw-category mw-category-columns')
            animals = data1.find_all('li')
            for i in animals:
                i = i.text
                if str(i[0]) == coun:
                    number += 1
                else:
                    lock = False

        with open('num_animal.csv', 'a', encoding='cp1251', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                [
                    coun,
                    number,
                ]
            )


if __name__ == '__main__':
    pars()
