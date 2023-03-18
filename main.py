from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random
import string
import time

# ask user for number of entries
num = input("Entries: ")

# names list
with open('names.txt', 'r') as f:
    names = [line.strip() for line in f]

# generate random email
webEmail = webdriver.Chrome()
webEmail.get('https://fakermail.com')
tEmail = ''

try:
    # wait for page to load
    element = WebDriverWait(webEmail, 10).until(
        EC.presence_of_element_located((By.ID, 'email-address'))
    )
    
    # set tEmail to the value of the element
    tEmail = element.get_attribute('value')
    
    #print(f'Temporary email address: {tEmail}')
except:
    print('Temporary email address not generated')

# web init
web = webdriver.Chrome()

tempEmailCounter = 0
sucSub = 0

# send keys
for i in range(int(num)):
    # open form
    web.get('https://olyent.formstack.com/forms/teacher_of_the_year_2023')
    
    # check if page is loaded
    try:
        WebDriverWait(web, 10).until(
            EC.presence_of_element_located((By.ID, 'field140649479-first'))
        )
    except:
        print("Page not loaded.")
    
    # web elements
    wFirstName = web.find_element(By.ID, 'field140649479-first')
    wLastName = web.find_element(By.ID, 'field140649479-last')
    wMail = web.find_element(By.ID, 'field140649480')
    wTeach = web.find_element(By.ID, 'field140649482_5')
    wSubmit = web.find_element(By.ID, 'fsSubmitButton5198207')
    
    # send first and last name entries
    wFirstName.send_keys(random.choice(names))
    wLastName.send_keys(random.choice(names))

    # generate a random string of length 5 to use as the alias
    alias = ''.join(random.choices(string.ascii_lowercase, k=5))

    # check if 10 iterations have passed (tempEmailCounter / 10 == 0 & tempEmailCounter != 0)
    if tempEmailCounter % 10 == 0 and tempEmailCounter != 0:
        # generate new temporary email after every 10 iterations
        webEmail.get('https://fakermail.com')
        
        try:
            # wait for page to load
            tElement = WebDriverWait(webEmail, 10).until(
                EC.presence_of_element_located((By.ID, 'email-address'))
            )
    
            # set tEmail to the value of the element
            tEmail = tElement.get_attribute('value')
    
            print(f'Temporary email address: {tEmail}')
        except:
            print('Temporary email address not generated')
    
    # merge the email address with the alias
    if "@" in tEmail:
        iEmail = f'{tEmail.split("@")[0]}+{alias}@{tEmail.split("@")[1]}'
    else:
        print("Invalid email address:", tEmail)
        
    wMail.send_keys(iEmail)
    
    # click the checkbox & submit
    wTeach.click()
    wSubmit.click()
    
    # check if the form was submitted successfully
    try:
        success_message = web.find_element(By.XPATH, "//p[text()='The form was submitted successfully.']")
        print("\033[92mForm submitted successfully!\033[0m")
        
        sucSub += 1
    except:
        print("Form submission failed.")
    
    tempEmailCounter += 1

print("========================================")
print(f"Successfully submitted {sucSub} forms out of {num}.")
print("========================================")

time.sleep(5)

# exit
webEmail.quit()
web.quit()