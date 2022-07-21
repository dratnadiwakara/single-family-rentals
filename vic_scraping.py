from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.executable_path = r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe'
driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get("https://www.valueinvestorsclub.com/ideas")
time.sleep(1)

for i in range(2002, 2024):
    time.sleep(5)
    print(i)
    try:
        driver.get("https://www.valueinvestorsclub.com/ideas")
        driver.find_elements(By.CLASS_NAME, 'btn.dropdown-toggle')[6].click()
        time.sleep(1)
        driver.find_element(By.ID, 'dash_goto_date').clear()
        driver.find_element(By.ID, 'dash_goto_date').send_keys('1/1/' + str(i))
        driver.find_element(By.ID, 'dash_goto_date_btn').click()
        time.sleep(1)
        for i in range(1, 50):
            try:
                load_more = driver.find_element(By.CLASS_NAME, "load-more.load_more_ideas")
                if load_more.text == 'LOAD MORE IDEAS':
                    load_more.click()
                    time.sleep(5)
                else:
                    break
            except:
                pass

        ideas_body = driver.find_element(By.ID, 'ideas_body')
        idea_rows = ideas_body.find_elements(By.CLASS_NAME, 'row')
        if len(idea_rows) > 0:
            print(len(idea_rows))
            idea_date = ""
            f = open('vic_ideas_2.txt', 'a')
            for idea_row in idea_rows:
                if len(idea_row.find_elements(By.CLASS_NAME, 'header')) > 0:
                    idea_date = idea_row.find_elements(By.CLASS_NAME, 'header')[0].text
                if len(idea_row.find_elements(By.CLASS_NAME, 'entry-header')) > 0:
                    entry_header = idea_row.find_elements(By.CLASS_NAME, 'entry-header')[0]
                    f.write(idea_date + "|" +
                            entry_header.find_element(By.CSS_SELECTOR, 'a').text + "|" +
                            entry_header.text + "|" + idea_row.find_element(By.CLASS_NAME, 'submitted-by').text+"\n")
                    time.sleep(1)
            f.close()
        else:
            print('no rows')
    except:
        pass

driver.close()
