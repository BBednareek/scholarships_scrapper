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

        for i in div.find_all('h2', class_='title'):
            title = i.text

        for i in div.find_all('p', class_='organizator-title'):
            organizator = i.text


        for i in div.find_all(class_='fleft'):
            j = list(i.next_siblings)
            for k in j:
                szczegoly = k.text

        for i in div.find_all('span', class_=''):
            termin = i.text
            print(termin)

        informacje[item] = {
                            'Tytuł': title,
                            'Organizator': organizator,
                            'Szczegóły': szczegoly,
                            'Termin': termin
                            }
        print(informacje[item])


