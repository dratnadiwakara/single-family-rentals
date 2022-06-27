from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.executable_path = r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe'

city_links = ['']

driver = webdriver.Firefox(options=options,
                           executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get('https://www.firstkeyhomes.com/firstkey-homes-locations-markets;offset=0;pageSize=12')
cities = driver.find_element(By.CLASS_NAME, "market-place-card").find_elements(By.CSS_SELECTOR, 'a')
for city in cities:
    city_links.append(city.get_attribute('href'))
city_links = city_links[1:]
city_links = list(dict.fromkeys(city_links))

driver.get('https://www.firstkeyhomes.com/firstkey-homes-locations-markets;offset=12;pageSize=12')
cities = driver.find_element(By.CLASS_NAME, "market-place-card").find_elements(By.CSS_SELECTOR, 'a')
for city in cities:
    city_links.append(city.get_attribute('href'))
city_links = list(dict.fromkeys(city_links))

driver.get('https://www.firstkeyhomes.com/firstkey-homes-locations-markets;offset=24;pageSize=12')
cities = driver.find_element(By.CLASS_NAME, "market-place-card").find_elements(By.CSS_SELECTOR, 'a')
for city in cities:
    city_links.append(city.get_attribute('href'))
city_links = list(dict.fromkeys(city_links))

for city_link in city_links[7:]:
    print(city_link)
    try:
        driver.get(city_link)
        time.sleep(2)
        f = open('firstkey_addresses.txt', 'a')
        for i in range(0, 200):
            scrollable_content = driver.find_elements(By.CLASS_NAME, 'property-showcase-box-top-details')
            if len(scrollable_content)>0:
                for sc in scrollable_content:
                    f.write(sc.find_element(By.CSS_SELECTOR, 'a').get_attribute('href') + "|" +
                            sc.find_element(By.CSS_SELECTOR, 'h2').text + "|" +
                            sc.find_element(By.CLASS_NAME, 'property-address').text.replace('\n', '-') + "|" +
                            sc.find_element(By.CLASS_NAME, 'property-details-info').text.replace('\n', '-') + "|" +
                            datetime.today().strftime('%Y-%m-%d') + "\n")
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',
                                      driver.find_element(By.CLASS_NAME, 'vertical.selfScroll.ng-star-inserted'))
                time.sleep(1)
        f.close()
    except:
        print('failed')

driver.close()