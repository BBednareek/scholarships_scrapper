from Scrapping.Functions.MojeStypendium.insertData import dodajStazMojeStypendia

def staz_mojestypendia():
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
        tytuly = doc.find_all(class_='title')
        organizatorzy = doc.find_all(class_='organizator-title')
        odbiorcy = doc.find_all('span', class_='taxonomy-list w2')
        zasiegi = doc.find_all('div', class_='fleft', string="Zasięg:")
        linki = doc.find_all(class_='hide-for-large anchor')

        #Przechodzimy przez kazdy element i wrzucamy go do bazy
        for i in range(min(len(tytuly), len(organizatorzy))):
            tytul = tytuly[i].text.strip().replace('\\n', '').replace('\\r', '')
            organizator = organizatorzy[i].text.strip().replace('\\n', '').replace('\\r', '')
            tematyka = 'Naukowa'
            odbiorca = odbiorcy[i].text.strip().replace('\\n', '').replace('\\r', '').capitalize().split(',')[0]
            zasieg = zasiegi[i].find_next().text.strip().replace('\\n', '').replace('\\r', '').capitalize().split(',')[0]
            link = linki[i]['href'].strip().replace('\\n', '').replace('\\r', '')
            kategoria = 'Staż'
            img = 'assets/images/staż.svg'

            url = f"{link}"
            page = requests.get(url)
            doc = BeautifulSoup(page.content, 'html.parser')

            opis = doc.find('div', class_='').text

            dodajStazMojeStypendia(kategoria, img, tytul, organizator, tematyka, zasieg, odbiorca, link, opis)

