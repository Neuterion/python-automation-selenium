from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
import sys
from config import CHROME_PROFILE_PATH

try:
    if sys.argv[1]:
        with open(sys.argv[1], 'r', encoding='utf8') as f:
            numbers = [number.strip() for number in f.readlines()]
except IndexError:
    print('Please provide the number list as the first argument.')

with open('msg.txt', 'r', encoding='utf8') as f:
    msg = f.read()

browser = webdriver.Chrome()
browser.maximize_window()

browser.get('https://web.whatsapp.com/')

input("Press ENTER after login into Whatsapp Web and your chats are visible.")

added_numbers = []

# Load added numbers from /contacted.txt
with open('contacted.txt', 'r', encoding='utf8') as f:
    contacts = f.read().splitlines()
    added_numbers = contacts

for number in numbers:
    if number in added_numbers:
        continue
    else:
        new_chat_btn = browser.find_element(by=By.XPATH, value='//span[@data-icon="new-chat-outline"]')
        
        time.sleep(1)
        
        new_chat_btn.click()
        
        try:
            search_css_selector = '.selectable-text.copyable-text.x15bjb6t.x1n2onr6'

            search_box = WebDriverWait(browser, 500).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, search_css_selector))
            )

            search_box.clear()

            time.sleep(1)

            pyperclip.copy(number)

            search_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"

            time.sleep(2)

            chat_css_selector = '._ak72._ak73'
            chat_title = browser.find_element(by=By.CSS_SELECTOR, value=chat_css_selector)

            chat_title.click()

            time.sleep(1)

            try:
                if sys.argv[2]:
                    attachment_box = browser.find_element(by=By.XPATH, value='//div[@title="Attach"]')
                    attachment_box.click()
                    time.sleep(1)

                    image_box = browser.find_element(by=By.XPATH, value='//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                    image_box.send_keys(sys.argv[2])
                    time.sleep(2)

                    send_btn = browser.find_element(by=By.XPATH, value='//span[@data-icon="send"]')
                    send_btn.click()
                    time.sleep(2)
            except IndexError:
                pass

            input_xpath = '//div[@contenteditable="true"][@role="textbox"][@title="Type a message"]'
            input_box = browser.find_element(by=By.XPATH, value=input_xpath)

            pyperclip.copy(msg)
            input_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"
            input_box.send_keys(Keys.ENTER)
            
            added_numbers.append(number)

            time.sleep(1)
        except:
            back_btn = browser.find_element(by=By.XPATH, value='//div[@role="button"][@aria-label="Back"]')
            back_btn.click()
            pass
        
# Save added_numbers to /contacted.txt
with open('contacted.txt', 'w', encoding='utf8') as f:
    for number in added_numbers:
        f.write(f'{number}\n')
