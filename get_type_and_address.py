import pandas as pd
import os
from bs4 import BeautifulSoup
import requests

ROOT_URL = 'https://prawdom.ru'
START_URL = '/k_seria.php?d=progjekt_docs/s1-447.php&s=3&r=99050'


def get_html(url):
    r = requests.get(url)
    return r.text


def get_date(html):
    soup = BeautifulSoup(html, 'lxml')
    series = soup.find('div', id='Left-Content').findAll('li')
    return series


def main():
    for s in get_date(get_html(ROOT_URL + START_URL)):
        print([s.find('a').get('href'), s.find('a').text])


if __name__ == '__main__':
    main()
