from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import gspread

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.executable_path = r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe'


driver = webdriver.Firefox(options=options,
                               executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get('https://lease.invitationhomes.com/search?ptr=sem&gclid=CjwKCAjwh-CVBhB8EiwAjFEPGXTYHB9UdGmqkrVCwf5M26-eVFk0pA2XhuW28s1bC87p4GBVei1vZhoCDO4QAvD_BwE')
cities = driver.find_elements(By.CLASS_NAME,'MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-6')

for i in range(11,len(cities)):
    #try:
        print(i)
        cities[i].click()
        time.sleep(2)
        no_homes = driver.find_elements(By.CLASS_NAME, 'MuiTypography-root.MuiTypography-body1')
        for nh in no_homes:
            if nh.text[0:7] == 'Viewing':
                break
        time.sleep(2)
        no_homes = int(nh.text[nh.text.find(' of ')+4:nh.text.find(' homes')])//10+1
        for j in range(0,no_homes+1):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',driver.find_element(By.ID, 'search-results-scroller'))
            time.sleep(10)

        homes = driver.find_elements(By.CLASS_NAME,'HouseCard-address')
        if len(homes)>0:
            print('extracting '+str(len(homes))+"\n")
            f = open('invitaion_homes_addresses.txt', 'a')
            for home in homes:
                f.write(home.find_element(By.CLASS_NAME,'address').get_attribute('innerHTML')+"|"+home.find_element(By.CSS_SELECTOR,'a').get_attribute('href') + "|"+
                        home.find_element(By.CLASS_NAME,'HouseCard-price').find_element(By.CSS_SELECTOR,'span').get_attribute('innerHTML')+"\n")
            f.close()
        time.sleep(3)
        driver.get(
            'https://lease.invitationhomes.com/search?ptr=sem&gclid=CjwKCAjwh-CVBhB8EiwAjFEPGXTYHB9UdGmqkrVCwf5M26-eVFk0pA2XhuW28s1bC87p4GBVei1vZhoCDO4QAvD_BwE')
        cities = driver.find_elements(By.CLASS_NAME, 'MuiGrid-root.MuiGrid-item.MuiGrid-grid-xs-12.MuiGrid-grid-sm-6')
        time.sleep(2)
driver.close()
