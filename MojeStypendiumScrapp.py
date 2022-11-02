#https://www.mojestypendium.pl/znajdz-{searching_item}/page/{page_number}/

#Szukamy tytulu, organizatora, rodzaj, grupy docelowej, zasieg. termin, opis

from bs4 import BeautifulSoup
import requests
import re

title = None
organizator = None
szczegoly = None
termin = None

searching_topic = input('staz/konkurs/stypendium: ')

url = f'https://www.mojestypendium.pl/znajdz-{searching_topic}/'
page = requests.get(url)
doc = BeautifulSoup(page.content, 'html.parser')

page_text = list(doc.find(class_='page-numbers').next_siblings)
pages = int(str(page_text[-4].text))

informacje = {}

for page in range(1, pages + 1):
    url = f'https://www.mojestypendium.pl/znajdz-{searching_topic}/page/{page}'
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')

    div = doc.find(class_='columns col-80')

    for item in div:

        try:
            title = div.find(class_='title').string
            organizator = div.find(class_='organizator-title').string
            termin = div.find('span', class_='').string

            informacje[item] = {
                'Tytuł': title.replace("\n", '').replace("\r", ''),
                'Organizator': organizator.replace("\n", '').replace("\r", '').strip(),
                'Termin': termin.replace("\n", '').replace("\r", '').strip()
            }
        except:
            pass

    print(informacje[item]['Tytuł'])
    print(informacje[item]['Organizator'])
    print(informacje[item]['Termin'])
    print('==============================')

