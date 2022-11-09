from bs4 import BeautifulSoup
import requests

url = f"https://www.mojestypendium.pl/znajdz-stypendium"
page = requests.get(url)
doc = BeautifulSoup(page.content, 'html.parser')

page_text = list(doc.find(class_='page-numbers').next_siblings)
pages = int(page_text[-4].text)

for page in range(1, pages + 1):
    url = f"https://www.mojestypendium.pl/znajdz-stypendium/page/{page}"
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')

    title = doc.find(class_='title')
    organizator = doc.find(class_='organizator-title')
    rodzaj = doc.find('span', class_='taxonomy-list')
    grupa_docelowa = doc.find('span', class_='taxonomy-list w2')
    content = doc.find(class_='column second-col')
    termin = content.find('span', class_='')

    print('Tytuł: ' + title.text.strip())
    print('Organizator: ' + organizator.text.strip())
    print('Grupa docelowa: ' + grupa_docelowa.text.strip())
    print('Termin składania wniosków: ' + termin.text.strip())
    print('=================================================')







