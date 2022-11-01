#https://www.mojestypendium.pl/znajdz-{searching_item}/page/{page_number}/

#Szukamy tytulu, organizatora, rodzaj, grupy docelowej, zasieg. termin, opis

from bs4 import BeautifulSoup
import requests

searching_topic = input('staz/konkurs/stypendium: ')

url = f'https://www.mojestypendium.pl/znajdz-{searching_topic}/'
page = requests.get(url)
doc = BeautifulSoup(page.content, 'html.parser')

page_text = list(doc.find(class_='page-numbers').next_siblings)
pages = int(str(page_text[-4].text))
print(pages)
details_found = {}
#
for page in range(1, pages + 1):
    url = f'https://www.mojestypendium.pl/znajdz-{searching_topic}/page/{page}'
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')

    info = doc.find_all(class_='column first-col')  #Tytul, organizator
    details = doc.find_all(class_='column second-col')#Rodzaj, grupa, zasieg, termin

    parent = info[0].parent
    h2 = parent.find("h2")
    print(h2.string)

    anchor = doc.find(class_='hide-for-large anchor')

    for item in anchor: #Szukamy odnosnika do informacji na temat danego stypendia
        parent = item.parent
        if parent.name != 'a':
            continue

        link = parent['href']


        result = info+details+link
        details_found[item] = {"Informacje": result.replace("\n", '').replace("\r", '').replace('Więcej', '')}

    print(details_found[item])





