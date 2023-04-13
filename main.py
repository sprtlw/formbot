from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random
import string

# ask user for number of entries
num = input("Entries: ")

# names list
with open('names.txt', 'r') as f:
    names = [line.strip() for line in f]

# generate random email
webEmail = webdriver.Chrome()
webEmail.get('https://temp-mail.org')
tEmail = ''

try:
    element = WebDriverWait(webEmail, 10).until(
        EC.presence_of_element_located((By.ID, 'mail'))
    )
    tEmail = element.get_attribute('value')
    print(f'Temporary email address: {tEmail}')
except:
    print('Temporary email address not generated')

# web init
web = webdriver.Chrome()
web.get('REDACTED')

# wait for page to load
WebDriverWait(web, 10).until(
        EC.presence_of_element_located((By.ID, 'field140649479-first'))
    )

# web elemennts
wFirstName = web.find_element(By.ID, 'field140649479-first')
wLastName = web.find_element(By.ID, 'field140649479-last')
wMail = web.find_element(By.ID, 'field140649480')

tempEmailCounter = 0

# send keys
for i in range(int(num)):
    # send first and last name entries
    wFirstName.send_keys(random.choice(names))
    wLastName.send_keys(random.choice(names))

    # generate a random string of length 5 to use as the alias
    alias = ''.join(random.choices(string.ascii_lowercase, k=5))

    # check if 10 iterations have passed (tempEmailCounter / 10 == 0 & tempEmailCounter != 0)
    if tempEmailCounter % 10 == 0 and tempEmailCounter != 0:
        # generate new temporary email after every 10 iterations
        webEmail.get('https://temp-mail.org')
        element = WebDriverWait(webEmail, 10).until(
            EC.presence_of_element_located((By.ID, 'mail'))
        )
        tEmail = element.get_attribute('value')
        print(f'New temporary email address: {tEmail}')
    
    # construct the email address with the alias
    iEmail = f'{tEmail.split("@")[0]}+{alias}@{tEmail.split("@")[1]}'
    wMail.send_keys(iEmail)
    tempEmailCounter += 1
    
# exit
webEmail.quit()
web.quit()
