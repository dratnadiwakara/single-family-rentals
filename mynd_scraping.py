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

start_points = list(range(0, 561))[::20]

for sp in start_points:
    driver.get('https://mynd.rentlinx.com/listings/start:' + str(sp))
    time.sleep(5)
    listings = driver.find_elements(By.CLASS_NAME, 'rl-content')
    if len(listings) > 0:
        f = open('mynd_addresses.txt', 'a')
        for listitem in listings:
            f.write(listitem.find_element(By.CLASS_NAME, 'PropertyName').text + "|" +
                    listitem.find_element(By.CLASS_NAME, 'rl-location').text + "|" +
                    listitem.find_element(By.CLASS_NAME, 'rl-rent').text + "|" +
                    listitem.find_element(By.CLASS_NAME, 'rl-bedrooms').text + "|" +
                    datetime.today().strftime('%Y-%m-%d') + "\n")
        f.close()
driver.close()
