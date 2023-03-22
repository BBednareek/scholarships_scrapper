from Scrapping.Functions.MojeStypendium.insertData import dodajWydarzenieEuroDesk

def Staże():

    from bs4 import BeautifulSoup
    import requests

    url = "https://www.eurodesk.pl/wez-udzial?&whom=&age=&category=29&country="
    page = requests.get(url)
    doc = BeautifulSoup(page.content, 'html.parser')

    kategoria = 'Staż'
    tytuly = doc.find_all('h3')
    deadline = doc.find_all('strong', string="Termin zgłoszenia:") #Nextsibling
    linki = doc.find_all('img', class_='mr-3')

    for i in range(min(len(tytuly), len(linki))):
        link = linki[i].parent['href']
        organizator = 'EuroDesk'
        tytul = tytuly[i].text.strip()
        tematyka = 'Inne'
        odbiorca = 'Studenci'
        zasieg = 'Ogólnopolskie'
        termin = deadline[i].nextSibling.text.strip()
        img = 'assets/images/staż.svg'

        url = f"https://www.eurodesk.pl/{link}"
        page = requests.get(url)
        doc = BeautifulSoup(page.content, 'html.parser')

        description = doc.find_all('p')
        for j in description:
            opis = j.text.strip()
            dodajStażEuroDesk(kategoria, img, tytul, organizator, tematyka, zasieg, odbiorca, termin, link, opis)
