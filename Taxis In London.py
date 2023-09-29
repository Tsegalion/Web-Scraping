from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd

def scrape_yell_data(url):
    driver = webdriver.Chrome(r"C:\Users\Tsega\Downloads\chromedriver-win64\chromedriver.exe")
    driver.get(url)
    time.sleep(20)

    # Scrolling to the bottom of the page to load all the content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Extract the page source
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    container = soup.find('div', class_='col-sm-24 col-md-17 col-lg-17 results--rightNav')

    cabs = container.find_all('article', class_=lambda x: x and x.startswith('col-sm-24 businessCapsule businessCapsule-'))

    return cabs

def extract_data(cab):
    try:
        name = cab.find('h2', class_='businessCapsule--name text-h2').text.strip()
    except AttributeError:
        name = 'N/A'
    
    try:
        phone = cab.find('div', class_='business--telephoneContent').text.strip()
    except AttributeError:
        phone = 'N/A'
    
    try:
        web = cab.find('div', class_='col-sm-24 businessCapsule--ctas')
        links = web.find_all('a', href=True)
        website = [link['href'] for link in links]
    except AttributeError:
        website = 'N/A'

    try:
        rating = cab.find('span', class_='starRating--average').text
    except AttributeError:
        rating = 0

    return {
        'Name': name,
        'Phone': phone,
        'Website': website,
        'Rating': rating
    }

def main():
    url = 'https://www.yell.com/ucs/UcsSearchAction.do?keywords=Taxis+%26+Private+Hire+Vehicles&location=ledbury&scrambleSeed=1738547925&pageNum='
    
    # Using list comprehension to create the data list
    data = [extract_data(cab) for x in range(1, 3) for cab in scrape_yell_data(url + str(x))]

    # Creating the DataFrame directly from the data list
    df = pd.DataFrame(data)
    # print(df)
    df.to_csv('yell_data.csv', index=False)

if __name__ == "__main__":
    main()
