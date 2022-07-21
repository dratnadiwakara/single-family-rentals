from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime

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


for city_link in city_links:
    print(city_link)
    driver = webdriver.Firefox(options=options,
                               executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
    driver.get(city_link)
    time.sleep(5)
    try:
        loadmore = driver.find_element(By.CLASS_NAME, "loadMoreResults").click()
        time.sleep(5)
    except:
        pass
    links = driver.find_elements(By.CLASS_NAME, "homeCard")
    if len(links) > 0:
        f = open('tricon_addresses.txt', 'a')
        for link in links:
            f.write(link.find_element(By.CLASS_NAME, 'price').text + "|" +
                    link.find_element(By.CLASS_NAME, 'address').text + "|" +
                    link.find_element(By.CLASS_NAME, 'bds').text + "|" +
                    link.find_element(By.CLASS_NAME, 'ba').text + "|" +
                    link.find_element(By.CLASS_NAME, 'sqft').text + "|" +
                    datetime.today().strftime('%Y-%m-%d') + "\n")
        f.close()
    driver.close()
    time.sleep(3)
