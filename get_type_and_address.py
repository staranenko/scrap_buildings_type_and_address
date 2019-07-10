import pandas as pd
import os
from bs4 import BeautifulSoup
import requests

ROOT_URL = 'https://prawdom.ru'
START_URL = '/k_seria.php?d=progjekt_docs/s1-447.php&s=3&r=99050'


# data = {'type',
#         'url',
#         'address'
#         }


def get_html(url):
    r = requests.get(url)
    return r.text


def get_building_series(html):
    soup = BeautifulSoup(html, 'lxml')
    series = soup.find('div', id='Left-Content').findAll('li')
    return series


def get_address_list(html):
    soup = BeautifulSoup(html, 'lxml')
    addresses = soup.find('div', id='Right-Content').find('p', class_='mstr150').findAll('a')
    return addresses


def get_building_info(html):
    soup = BeautifulSoup(html, 'lxml')
    info = soup.find('div', id='Left-1-dom').find('ul').findAll('li')
    return info


def main():
    table_out = []
    for page_type_name in get_building_series(get_html(ROOT_URL + START_URL)):
        lot_url = ROOT_URL + page_type_name.find('a').get('href')
        lot_name = page_type_name.find('a').text
        data_series = {'SERIES_NAME': lot_name,
                       'SERIES_URL': lot_url
                       }
        print('\n', data_series, sep='')

        for address in get_address_list(get_html(lot_url)):
            building_url = ROOT_URL + address.get('href')
            building_address = address.text.split(' - ')
            building_street = building_address[0]
            building_house = building_address[1]
            data_building = {'BUILDINGS_URL': building_url,
                             'BUILDINGS_STREET': building_street,
                             'BUILDINGS_HOUSE': building_house}
            print(data_building)

            data_info = {}

            for i in get_building_info(get_html(building_url)):
                info_tag = i.text.split('-')[0].strip()
                try:
                    info_value = i.find('span').text.strip()
                except AttributeError:
                    # print(i)
                    try:
                        info_value = i.find('u').text
                    except AttributeError:
                        info_value = i

                # if len(info_value) > 1:
                #     if info_value[-1] == ',':
                #         info_value = info_value[:-1]
                try:
                    info_value = info_value.rstrip(',').rstrip('.')
                except TypeError:
                    pass

                data_info[info_tag.upper()] = info_value
                # print(info_tag, ':', info_value)

            print(data_info)
            table_out.append(dict(**data_series, **data_building, **data_info))

        if lot_name == 'Серия I-447':
            break

    df_out = pd.DataFrame(table_out)

    writer = pd.ExcelWriter('output.xlsx')
    df_out.to_excel(writer, na_rep='NaN')
    writer.save()


if __name__ == '__main__':
    main()
