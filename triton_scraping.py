from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import gc
import pandas as pd
import time
from datetime import datetime, timedelta
import os
import PyPDF2
import gspread

sa = gspread.service_account(filename='C:/Users/Dimuthu/Documents/LK Economic Indicators/data_processing/'
                                      'lk-indicators-585e699aa78d.json')
sh = sa.open('sfr_listings')
wks = sh.worksheet('tricon')

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.executable_path = r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe'
driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get("https://triconresidential.com/find/")

cities = driver.find_elements(By.CLASS_NAME, "hasHomes")
city_links = ['']
for city in cities:
    city_link = city.get_attribute("href")
    if city_link != None:
        city_links.append(city_link)
driver.close()
city_links = city_links[1:]

count = 1
for city_link in city_links:
    print(city_link)
    driver = webdriver.Firefox(options=options,
                               executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
    driver.get(city_link)
    time.sleep(2)
    try:
        loadmore = driver.find_element(By.CLASS_NAME, "loadMoreResults").click()
        time.sleep(2)
    except:
        pass
    links = driver.find_elements(By.CLASS_NAME, "homeCard")
    if len(links) > 0:
        for link in links:
            add = [city_link, link.get_attribute("title")]
            wks.append_row(add)
            count = count + 1
            if (count % 50) == 0:
                time.sleep(300)
    driver.close()
    time.sleep(3)
