import scrapy
from scrapy import Request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the Selenium WebDriver
driver = webdriver.Chrome(r"C:\Users\Tsega\Downloads\chromedriver_win32\chromedriver.exe")  # You can change the WebDriver based on your browser choice
driver.get("https://icodrops.com/category/ended-ico/")

links = []
last_height = driver.execute_script("return document.body.scrollHeight")
ico_count = 1400

while ico_count > len(links):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(5)  # Wait for the page to load

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break

    last_height = new_height

    elements = driver.find_elements(By.CSS_SELECTOR, '#ended-icos-container > div')
    links = []

    for element in elements:
        link = element.find_element(By.TAG_NAME, 'a')
        href = link.get_attribute('href')
        links.append(href)

# Now unto Scrapy

class IcospiderSpider(scrapy.Spider):
    name = 'icospider'
    allowed_domains = ['icodrops.com']
    start_urls = ['http://icodrops.com/category/ended-ico/']


    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
        for url in self.start_urls:
            yield Request(url, headers=headers)
    
    def parse(self, response):
        for link in links:
            yield response.follow(link, callback=self.parse_icolists)

    def parse_icolists(self, response):
        icolists = response.css('article')

        try: 
            for ico in icolists:
                try:
                    date = ico.css('div.col-12.title-h4 i.fa.fa-calendar + h4::text').get().strip()
                    ICO_period = date.split(':')[1].strip()
                except (AttributeError, IndexError):
                    ICO_period = 'N/A'

                try:
                    D = response.css('span.ico-category-name::text').get().strip()
                    Category = D.split(')')[0].split('(')[1].strip()
                except (AttributeError, IndexError):
                    Category = 'N/A'

                try:
                    p = response.css('div.col-12.col-md-6 span.grey:contains("ICO Token Price:")').xpath('following-sibling::text()').get()
                    ICO_price = p.split('=')[1]
                except (AttributeError, IndexError):
                    ICO_price = 'N/A'

                try:
                    Project = ico.css('h3::text').get().strip()
                except (AttributeError, IndexError):
                    Project = 'N/A'

                try:
                    Description = ico.css('div.ico-description::text').get().strip()
                except (AttributeError, IndexError):
                    Description = 'N/A'
                
                try:
                    Token_sale_end = ico.css('div.sale-date::text').get().strip()
                except (AttributeError, IndexError):
                    Token_sale_end = 'N/A'
                    
                try:    
                    Raised_usd = ico.css('div.blue.money-goal::text').get().strip()
                except (AttributeError, IndexError):
                    Raised_usd = 'N/A'
                
                try:    
                    Ticker = ico.css('div.col-12.col-md-6 span.grey:contains("Ticker:")').xpath('following-sibling::text()').get().strip()
                except (AttributeError, IndexError):
                    Ticker = 'N/A'
                    
                try:
                    Platform = ico.css('div.col-12.col-md-6 span.grey:contains("Token type:")').xpath('following-sibling::text()').get().strip()
                except (AttributeError, IndexError):
                    Platform = 'N/A'

                try:
                    Fundraise_goal = ico.css('div.col-12.col-md-6 span.grey:contains("Fundraising Goal:")').xpath('following-sibling::text()').get().strip()
                except (AttributeError, IndexError):
                    Fundraise_goal = 'N/A'
                    
                try:
                    Total_token = ico.css('div.col-12.col-md-6 span.grey:contains("Total Tokens:")').xpath('following-sibling::text()').get()
                except (AttributeError, IndexError):
                    Total_token = 'N/A'
            
                try:
                    Sold = ico.css('div.col-12.col-md-6 span.grey:contains("Available for Token Sale:")').xpath('following-sibling::text()').get()
                except (AttributeError, IndexError):
                    Sold = 'N/A'
                
                try:
                    Token_Role = ico.css('div.col-12.info-analysis-list span.grey:contains("Role of Token:")').xpath('following-sibling::text()').get().strip()
                except (AttributeError, IndexError):
                    Token_Role = 'N/A'


                yield {
                    'Project' : Project if Project else 'N/A',
                    'Category' : Category if Category else 'N/A',
                    'Description' : Description if Description else 'N/A',
                    'ICO_period': ICO_period if ICO_period else 'N/A',
                    'Token_sale_end' : Token_sale_end if Token_sale_end else 'N/A',
                    'Raised_usd' : Raised_usd if Raised_usd else 'N/A',
                    'Ticker' : Ticker if Ticker else 'N/A',
                    'Platform' : Platform if Platform else 'N/A',
                    'ICO_price' : ICO_price  if ICO_price else 'N/A',
                    'Fundraise_goal' : Fundraise_goal if Fundraise_goal else 'N/A',
                    'Total_token' : Total_token if Total_token else 'N/A',
                    'Sold_%' : Sold if Sold else 'N/A',
                    'Token_Role' : Token_Role if Token_Role else 'N/A',

                }
        except Exception as error:
            print('Error:', error)
