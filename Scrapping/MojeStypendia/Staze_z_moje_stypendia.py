from Functions.MojeStypendium.createStaze import *
def staze_mojestypendia():
    from bs4 import BeautifulSoup
    import requests

    url = f"https://www.mojestypendium.pl/znajdz-staz"
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')

    page_text = list(doc.find(class_='page-numbers').next_siblings)
    pages = int(page_text[-4].text) #Szukamy ilosci stron

    for page in range(1, pages + 1): #Przechodzimy przez kazda strone
        url = f"https://www.mojestypendium.pl/znajdz-staz/page/{page}"
        page = requests.get(url)
        doc = BeautifulSoup(page.content, 'html.parser')

        #Materialy do scrapowania
        tytul = doc.find_all(class_='title')
        organizator = doc.find_all(class_='organizator-title')
        rodzaj = doc.find_all('div', class_='fleft', string="Rodzaj:")
        grupa = doc.find_all('span', class_='taxonomy-list w2')
        zasieg = doc.find_all('div', class_='fleft', string="Zasięg:")
        branza = doc.find_all('div', class_='fleft', string="Branża:")
        link = doc.find_all(class_='hide-for-large anchor')

        #Przechodzimy przez kazdy element i wrzucamy go do bazy
        for i in range(min(len(tytul), len(grupa))):
            t = tytul[i].text.strip().replace('\\n', '').replace('\\r', '')
            o = organizator[i].text.strip().replace('\\n', '').replace('\\r', '')
            r = rodzaj[i].find_next().text.strip().replace('\\n', '').replace('\\r', '')
            g = grupa[i].text.strip().replace('\\n', '').replace('\\r', '')
            z = zasieg[i].find_next().text.strip().replace('\\n', '').replace('\\r', '')
            b = branza[i].find_next().text.strip().replace('\\n', '').replace('\\r', '')
            l = link[i]['href'].strip().replace('\\n', '').replace('\\r', '')

            appendStaze(t, o, r, z, g, b, l)

