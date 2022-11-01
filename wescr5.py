from bs4 import BeautifulSoup
import requests
import re
search_term = input("What GPU do you want to search for? ") #Czego szukamy na stronie

url = f"https://www.newegg.ca/p/pl?d=3080&N=4131" #Wskazujemy w url w ktorym miejscu tag sie ustawia
page = requests.get(url).text
doc = BeautifulSoup(page, 'html.parser')

page_text = doc.find(class_="list-tool-pagination-text").strong #Szukamy ilosci stron
pages = int(str(page_text).split('/')[-2].split('>')[-1][:-1]) #Wybieramy sama liczbe stron
items_found = {} #Tworzymy dict
print(pages)

# for page in range(1, pages + 1): #Zapis taki, zeby nie zaczynas od strony 0 ktorej nie ma, i konczyc zawsze na stronie ostatniej
#     url = f"https://www.newegg.ca/p/pl?d={search_term}&N=4131&page={page}" #do url dodajemy numer strony
#     page = requests.get(url).text
#     doc = BeautifulSoup(page, 'html.parser')
#     div = doc.find(class_='item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell') #Szukamy div z tabela itemow
#
#     items = div.find_all(text=re.compile(search_term)) #re.compile() zeby szukalo np ,,3080 FTW", czyli nie tylko samego 3080 ale i tego z napsiami po
#
#     for item in items:
#         parent = item.parent #Szukamy parenta
#         if parent.name != 'a': #Jezeli nie ma taga A, kontynuuj
#             continue
#
#         link = parent['href'] #tworzymy odnosnik wybierajac go z info
#         next_parent = item.find_parent(class_='item-container') #Szukamy parenta poprzez jego klase
#         try: #Probujemy szukac ceny przedmiotu, jezeli jest, to dodajemy ja do slownika oraz dodajemy link
#             price = next_parent.find(class_='price-current').find("strong").string
#             items_found[item] = {'price': int(price.replace(',', '')), 'link': link}
#         except:
#             pass #Jezeli nie ma ceny lub linku, pomijamy ten przedmiot
#
# sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price']) #Tworzymy posortowana liste
#
# for item in sorted_items: #Wypisujemy Nazwe przedmiotu, jego cene z waluta, odnosnik do niego
#     print(item[0])
#     print(f"${item[1]['price']}")
#     print(item[1]['link'])
#     print('----------------')
