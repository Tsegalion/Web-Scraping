from selenium import webdriver
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome(r"C:\Users\Tsega\Downloads\chromedriver_win32\chromedriver.exe")

base_url = driver.get("https://neefty.io/xrpl?cid=63fea0117ecc1a23708fd704")

NFT = []

# Define the number of pages to scrape
num_pages = 144
time.sleep(5)

for page in range(1, num_pages + ):
    # Load the page

    # Scroll to the bottom of the page to load all the content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    # Extract the page source
    page_source = driver.page_source

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    elements = soup.find_all('div', class_=lambda x: x and x.startswith('bubble-element GroupItem group-item entry-'))

    for element in elements:
        nft_names = element.find_all('div', class_='bubble-element Text')
        for nft_name in nft_names:
            Nam = nft_name.find('div', class_='content')

            if 'RANK' in Nam.text:
                Rank = Nam.text.strip()

            if 'Top G' in Nam.text and 'Money Minded Apes - Top G Apes' not in Nam.text:
                Name = Nam.text.strip()

        Non = {
            'Name': Name,
            'Rank': Rank
        }

        NFT.append(Non)

    # Click the "Next" button
    next_button = driver.find_element_by_xpath('//button[contains(text(), "arro_forward_ios")]')
    next_button.click()

driver.quit()
