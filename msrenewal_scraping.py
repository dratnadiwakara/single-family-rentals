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
driver.get('https://www.msrenewal.com/search')

cities = driver.find_elements(By.CLASS_NAME, "text-btn.w-full")
city_names = ['']

for city in cities:
    city_names.append(city.text)
city_names = city_names[1:]

for city in city_names:
    print(city)
    try:
        driver.get('https://www.msrenewal.com/search/' + city)
        time.sleep(5)
        homelist = driver.find_element(By.CLASS_NAME, 'p-4.space-y-4.w-full').find_elements(By.CSS_SELECTOR, 'a')
        if len(homelist) > 0:
            f = open('msrenewal_addresses.txt', 'a')
            for home in homelist:
                f.write(home.find_element(By.CLASS_NAME, 'font-serif.text-2xl.font-light').text + "|" +
                        home.find_element(By.CLASS_NAME, 'flex.mt-2').text.replace("\n", ", ") + "|" +
                        home.find_element(By.CLASS_NAME, 'flex.items-center.text-gray-700.pt-3').text.replace("\n",
                                                                                                              ", ") + "|" +
                        datetime.today().strftime('%Y-%m-%d') + "\n")
            f.close()
    except:
        print(" failed")
driver.close()

