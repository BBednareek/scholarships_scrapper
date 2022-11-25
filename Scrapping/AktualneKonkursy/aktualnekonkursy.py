from Functions.AktualneKonkursy.createKonkurs import *
def aktualneKonkursy():
    from bs4 import BeautifulSoup
    import requests

    url = "https://aktualnekonkursy.pl/"
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')

    div = doc.find('div', class_='pagination')
    unordered_list = div.find('ul')
    list_items = list(unordered_list.find_all('li'))
    pages = int(list_items[-3].text)

    rodzaje = ['literackie', 'fotograficzne', 'plastyczne', 'filmowe']

    for i in range(0, len(rodzaje)-1):
        for j in range(0, pages + 2):
            url = f"https://aktualnekonkursy.pl/konkursy-{rodzaje[i]}?start={j-1}0"
            page = requests.get(url)
            doc = BeautifulSoup(page.content, 'html.parser')

            tytul = doc.find_all('a', class_='title')
            termin = doc.find_all('b', class_='')
            text = doc.find_all('div', class_='item_desc')
            link = doc.find_all('a', class_='title')

            for k in range(len(link)):
                title = tytul[k].text.strip().replace('\\n', '').replace('\\r', '')
                term = termin[k].text.strip().replace('\\n', '').replace('\\r', '')
                txt = text[k].text.strip().replace('\\n', '').replace('\\r', '')
                rodzaj = 'artystyczne'

                anchor = 'https://aktualnekonkursy.pl'+link[k]['href'].strip().replace('\\n', '').replace('\\r', '')

                url = f"https://aktualnekonkursy.pl/konkursy-literackie/ad{link[k]['href']}"
                page = requests.get(url)
                doc = BeautifulSoup(page.content, 'html.parser')

                organizator = doc.find('p')
                organizator = organizator.text[39:].strip()
                div = doc.find('div', class_='desc_content')
                grupa_docelowa = div.select('p')[1]
                grupa_docelowa = grupa_docelowa.text.replace('Uczestnicy', '').replace('Opis', '').replace('Zasady konkursu w skrócie', '')

                appendKonkurs(title, organizator, term, anchor, txt, grupa_docelowa, rodzaj)









