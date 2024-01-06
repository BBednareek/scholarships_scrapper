import requests
from bs4 import BeautifulSoup
import json

# Function to scrape data from a single page
def scrape_page(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, 'html.parser')
    scholarship_rows = soup.find_all('div', class_='row large-up-2 list-open')
    scholarships_data = []

    for row in scholarship_rows:
        
        title = row.find('h2', class_='title').text.strip()
        organizer = row.find('p', class_='organizator-title').text.strip()
        target_group = row.find_all('span', class_='taxonomy-list w2')[0].text.strip()
        deadline = row.find('span', class_='content').find_next('span', class_='').text.strip()
        link = row.find('a', class_='hide-for-large anchor')['href']
        

        scholarship = {
            "Title": title,
            "Organizer": organizer,
            "Target Group": target_group,
            "Deadline": deadline,
            "Link": link,
            'Path': 'assets/images/stypendium.svg'
        }
        scholarships_data.append(scholarship)
    return scholarships_data

# Function to scrape data from every page in url -> save to .json file
def scholarshipsMS():
    fpartUrl= "https://www.mojestypendium.pl/znajdz-stypendium/page/"
    spartUrl = "/?grupa_docelowa_45=studenci"

    first_page_url = f"{fpartUrl}1{spartUrl}"
    first_page_res = requests.get(first_page_url)
    first_page_soup = BeautifulSoup(first_page_res.content, 'html.parser')
    page_text = list(first_page_soup.find(class_='page-numbers').next_siblings)
    pages = int(page_text[-4].text)

    all_scholarships = []
    for page_num in range(1, pages):
        url = f"{fpartUrl}{page_num}{spartUrl}"
        scholarships = scrape_page(url)
        all_scholarships.extend(scholarships)
        print('Scrapping page no. ', page_num, ' from MojeStypendium')
    with open('scholarships_data.json', 'w', encoding='utf-8') as file:
        json.dump(all_scholarships, file, ensure_ascii=False, indent=4)

scholarshipsMS()