from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.executable_path = r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe'
driver = webdriver.Firefox(options=options,
                           executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get(
    'https://hotpads.com/baton-rouge-la/houses-for-rent?propertyTypes=house')
time.sleep(5)

listings_href = ['']
last_page = False

while not last_page:
    listings = driver.find_element(By.XPATH,"//ul[@data-testid='search-result-list-container']").find_elements(By.CSS_SELECTOR,'a')
    if len(listings)>2:
        f = open('zillow/br_listings.txt', 'a')
        for listi in listings:
            href = listi.get_attribute('href')
            if href not in listings_href:
                listings_href.append(href)
                f.write(href + "\n")
            try:
                next_page = driver.find_element(By.XPATH,"//li[@data-testid='pagination-next-page']")
                time.sleep(2)
                next_page.find_element(By.CSS_SELECTOR,'a').click()
                time.sleep(5)
            except:
                last_page = True
        f.close()
driver.close()
