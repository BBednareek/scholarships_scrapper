import json
from bs4 import BeautifulSoup
import requests

with open("al.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

job_board = data['Jobs']
CatName = 'Staz'

for item in job_board:
    if(item['PositionLevel'] == 'praktykant / stażysta'):

        url = item['OfferUrl']
        page = requests.get(url)
        doc = BeautifulSoup(page.content, 'html.parser')

        responsibilites = doc.find('div', {'data-scroll-id' : 'responsibilities-1'})
        if responsibilites.text.startswith('T'):
            responsibilites = responsibilites.text.replace('Twój zakres obowiązków', '')
        elif responsibilites.text.startswith('Y'):
            responsibilites = responsibilites.text.replace('Your responsibilities', '')
        else:
            continue

        requirements = doc.find('div', {'data-scroll-id': 'requirements-1'})
        if requirements.text.startswith('O'):
            requirements = requirements.text.replace('Our requirements', '')
        elif requirements.text.startswith('N'):
            requirements = requirements.text.replace('Nasze wymagania', '')
        else:
            continue



        offered = doc.find('div', {'data-scroll-id': 'offered-1'})
        if type(offered) == 'NoneType':
            print('c')
        elif offered.text.startswith('W'):
            offered = offered.text.replace('What we offer', '')
            print(offered)
        elif offered.text.startswith('T'):
            offered = offered.text.replace('To oferujemy', '')
            print(offered)





