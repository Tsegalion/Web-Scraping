import requests
from bs4 import BeautifulSoup

links = []
for x in range(1,100):
    source = requests.get(f'https://www.trustpilot.com/review/www.uber.com?page={x}&stars=1').text
    soup = BeautifulSoup(source, 'lxml')

    review_items = soup.find_all('div', class_='styles_consumerDetailsWrapper__p2wdr')
    for review in review_items:
        for link in review.find_all('a', href=True):
            href = link['href']
            full_link = "https://www.trustpilot.com" + href
            links.append(full_link)
            
# iterating through each link to extract desired data
rev = []
for link in links:
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')

    ree_view = soup.find_all('div', class_ = 'styles_container__BnfUR')

    for ree in ree_view:
        try:
            # Extract the name of the reviewer
            Name = ree.find('h1', class_ = 'typography_display-xs__sDdPF typography_appearance-default__AAY17 styles_consumerDisplayName__QDr6f').text.strip()
            # print(Name)
        except AttributeError:
            Name = 'N/A'

        try:
            # Extract the country of the reviewer
            Date = ree.find('p', class_ = 'typography_body-m__xgxZ_ typography_appearance-default__AAY17').text.strip()
            # print(Date)
        except AttributeError:
            Date = 'N/A'

        try:
            # Extract the date of the experience
            Revieww = ree.find('h2', class_ = 'typography_heading-s__f7029 typography_appearance-default__AAY17').text.strip()
            # print(Review)
        except AttributeError:
            Revieww = 'N/A'

        try:
            # Extract the review text
            Country = ree.find('p', class_ = 'typography_body-l__KUYFJ typography_appearance-subtle__8_H2l').text.strip()
            # print(Country)
        except AttributeError:
            Country = 'N/A'

        try:
            # Extract the review text
            Reviewww = ree.find('p', class_ = 'typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn').text.strip()
            # print(Country)
        except AttributeError:
            Reviewww = 'N/A'

        Uber = {
            'Name' : Name,
            'Date' : Date,
            'Country' : Country,
            'Revieww' : Revieww,
            'Reviewww' : Reviewww
        }

        rev.append(Uber)
