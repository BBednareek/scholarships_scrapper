import requests
import json
from bs4 import BeautifulSoup

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    grant_data = []

    noOfScholarships = int(soup.find('strong', string='Lista').next_element.next_element.next_element.text.replace('(', '').replace(')',''))
    titles = soup.find_all('h3')
    organizers = soup.find_all('span', class_='fundator')
    links = soup.find_all('img', class_='mr-3')
    deadlines = soup.find_all('span', class_='float-right deadline')

    for i in range(min(noOfScholarships, len(titles), len(organizers), len(links), len(deadlines))):
        static = 'www.eurodesk.pl'
        title = titles[i].text.strip()
        organizer = organizers[i].text.strip()
        link = f"{static}{links[i].parent['href']}"
        deadline = deadlines[i].text.replace('\r','').replace('\n','').strip()
        
        grant_info = {
            'From': 'Eurodesk',
            'Title': title,
            'Organizer': organizer,
            'Target Group': 'studenci',
            'Deadline': deadline,
            'Link': link,
            'Path': 'assets/images/stypendium.svg'
        }
        grant_data.append(grant_info)

    return grant_data

def save_to_json(data):
    with open('scholarships_data.json', 'r', encoding='utf-8') as file:
        existing_data = json.load(file) 

    existing_data.extend(data)

    with open('scholarships_data.json', 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

def scholarshipsED():
    url = 'https://www.eurodesk.pl/granty?&whom=7&category=17&sort=deadline,asc&limit=500&page=1'
    all_scholarships = scrape_page(url)
    save_to_json(all_scholarships)
    print('Scrapping page no. 1 from EuroDesk')

scholarshipsED()
