from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import gspread

sa = gspread.service_account(filename='C:/Users/Dimuthu/Documents/LK Economic Indicators/data_processing/'
                                      'lk-indicators-585e699aa78d.json')
sh = sa.open('sfr_listings')
wks = sh.worksheet('progress')

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.executable_path = r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe'
driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get("https://rentprogress.com/404-not-found/")

cities = driver.find_elements(By.CLASS_NAME, "custom-link")
city_links = ['']
for city in cities:
    city_link = city.get_attribute("href")
    if city_link != None:
        city_links.append(city_link)
driver.close()
city_links = city_links[1:48]

f = open('progress_links.txt', 'a')
for city_link in city_links:
    driver = webdriver.Firefox(options=options,
                               executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
    driver.get(city_link)
    time.sleep(3)
    city_link = driver.current_url
    print(city_link)
    time.sleep(2)
    try:
        pages = driver.find_elements(By.CLASS_NAME,'pagination')
        pages = pages[0].find_elements(By.CSS_SELECTOR, 'ul')[0].text
        if pages[len(pages) - 4:len(pages)] == 'NEXT':
            page_ends = [i for i in range(len(pages)) if pages.startswith('\n', i)]
            last_page = int(pages[page_ends[(len(page_ends)-2)]+1:page_ends[(len(page_ends)-1)]])
        for page in range(1, last_page + 1):
            f.write(city_link[0:city_link.find("page-")+5]+str(page)+city_link[city_link.find("page-")+6:]+'\n')
        time.sleep(2)
    except:
        f.write(city_link+"\n")
    driver.close()
    time.sleep(3)
f.close()

with open('progress_links.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]


for line in lines:
    driver = webdriver.Firefox(options=options,
                               executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
    driver.get(line)
    time.sleep(10)
    print(line)
    addresses = driver.find_elements(By.CLASS_NAME, 'property-address')
    f = open('progress_addresses.txt', 'a')
    for add in addresses:
        f.write(line+"|"+add.text + "\n")
    f.close()
    driver.close()
