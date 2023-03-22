from Scrapping.Functions.MojeStypendium.insertData import dodajWydarzenieEuroDesk

def ProgEduk():

    from bs4 import BeautifulSoup
    import requests

    url = "https://www.eurodesk.pl/wez-udzial?&whom=&age=&category=53,27,28,30,31&country="
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')

    kategoria = 'Program Edukacyjny'
    tytuly = doc.find_all('h3')
    deadline = doc.find_all('strong', string="Termin zgłoszenia:") #Nextsibling
    linki = doc.find_all('img', class_='mr-3')

    for i in range(min(len(tytuly), len(linki))):
        link = linki[i].parent['href']
        organizator = 'EuroDesk'
        tytul = tytuly[i].text.strip()
        tematyka = 'Inne'
        odbiorca = 'Uczniowie'
        zasieg = 'Ogólnopolskie'
        termin = deadline[i].nextSibling.text.strip()
        img = 'assets/images/program edukacyjny.svg'

        url = f"https://www.eurodesk.pl/{link}"
        page = requests.get(url)
        doc = BeautifulSoup(page.content, 'html.parser')

        description = doc.find_all('p')
        for j in description:
            opis = j.text.strip()
            dodajProgEdukEuroDesk(kategoria, img, tytul, organizator, tematyka, zasieg, odbiorca, termin, link, opis)
