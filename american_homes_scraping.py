from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import gspread

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.executable_path = r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe'

states = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
links = ['']

for state in states:
    url = 'https://www.ah4r.com/query?criteria='+state
    driver = webdriver.Firefox(options=options,
                               executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
    driver.get(url)
    time.sleep(5)

    btn = driver.find_elements(By.XPATH, "//button[@data-testid='list-view-switch']")
    for b in btn:
        if b.text == 'List View':
            b.click()
            break
    try:
        btn = driver.find_elements(By.XPATH, "//button[@aria-label='Close']")
        btn[len(btn) - 1].click()
        time.sleep(5)
    except:
        pass

    no_listings = driver.find_element(By.CLASS_NAME,'text-tertiary').text
    no_listings = int(no_listings[0:len(no_listings)-8])
    driver.close()

    if no_listings<1500:
        for page_no in range(1, no_listings//24+1):
            links.append(url + '&page='+str(page_no))
links = links[1:]

with open('american_homes_links.txt', 'w') as f:
    for link in links:
        f.write("%s\n" % link)


with open('american_homes_links.txt') as f:
    links = f.read().splitlines()


driver = webdriver.Firefox(options=options,
                           executable_path=r'C:\Users\Dimuthu\cse2022\cse2022\scripts\geckodriver.exe')
driver.get(links[0])

link_prefix = ''

for link in links:
    print(link)
    try:
        if link_prefix == link[0:link.find('&page')]:
            print('if')
            try:
                cookie_btn = driver.find_element(By.CLASS_NAME, 'bg-yellow-primary')
                cookie_btn.click()
                time.sleep(1)
            except:
                pass
            next_btn = driver.find_elements(By.XPATH, "//button[@data-testid='page-next']")
            for b in next_btn:
                if b.get_attribute('class') == 'select-none':
                    print('click next')
                    b.click()
                    time.sleep(5)
                    break
        else:
            print('else')
            link_prefix = link[0:link.find('&page')]
            driver.get(link)
            time.sleep(3)
            btn = driver.find_elements(By.XPATH, "//button[@data-testid='list-view-switch']")
            for b in btn:
                if b.text == 'List View':
                    b.click()
                    break
            time.sleep(3)
            try:
                cookie_btn = driver.find_element(By.CLASS_NAME, 'bg-yellow-primary')
                cookie_btn.click()
                time.sleep(1)
            except:
                pass
        addresses = driver.find_elements(By.XPATH, "//div[contains(@class, 'container')]//a[@rel='nofollow']")
        if len(addresses) > 0:
            f = open('american_addresses.txt', 'a')
            for add in addresses:
                f.write(add.text + "|" + add.get_attribute('href') + "|" + link + "\n")
            f.close()
    except:
        pass


'''
for link in links[0:4]:
    try:
        print(link)
        driver.get(link)
        time.sleep(5)

        btn = driver.find_elements(By.XPATH, "//button[@data-testid='list-view-switch']")
        for b in btn:
            if b.text == 'List View':
                b.click()
                break
        btn = driver.find_elements(By.XPATH, "//button[@aria-label='Close']")
        btn[len(btn) - 1].click()
        time.sleep(5)
        addresses = driver.find_elements(By.XPATH, "//div[contains(@class, 'container')]//a[@rel='nofollow']")
        if len(addresses) > 0:
            f = open('american_addresses.txt', 'a')
            for add in addresses:
                f.write(add.text + "|" + add.get_attribute('href') + "|" + link + "\n")
            f.close()
        driver.close()
    except:
        pass
'''
