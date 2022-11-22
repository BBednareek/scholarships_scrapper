from bs4 import BeautifulSoup
import requests
from mojeStypendiumFunctions import *

url = f"https://www.mojestypendium.pl/znajdz-stypendium"
page = requests.get(url)
doc = BeautifulSoup(page.content, 'html.parser')

page_text = list(doc.find(class_='page-numbers').next_siblings)
pages = int(page_text[-4].text)

for page in range(1, pages + 1):
    url = f"https://www.mojestypendium.pl/znajdz-stypendium/page/{page}"
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')

    title = doc.find_all(class_='title')
    for i in title:
        x = append_title(i.text.strip().replace('\\n', '').replace('\\r', ''))

    organizator = doc.find_all(class_='organizator-title')
    for i in organizator:
        x = append_organizator(i.text.strip().replace('\\n', '').replace('\\r', ''))


    rodzaj = doc.find_all('div', class_='fleft', string="Rodzaj:")
    for i in rodzaj:
        x = append_type(i.find_next().text.strip().replace('\\n', '').replace('\\r', ''))

    zasieg = doc.find_all('div', class_='fleft', string="Zasięg:")
    for i in zasieg:
        x = append_range(i.find_next().text.strip().replace('\\n', '').replace('\\r', ''))

    content = doc.find_all(class_='column second-col')
    for i in content:
        termin = i.find_all('span', class_='')
        for j in termin:
            x = append_deadline(j.text.strip().replace('\\n', '').replace('\\r', ''))

    link = doc.find_all(class_='hide-for-large anchor')
    for i in link:
        i = append_link(i['href'].strip().replace('\\n', '').replace('\\r', ''))


