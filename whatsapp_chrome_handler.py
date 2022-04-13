from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def login(driver):
    driver.get("https://web.whatsapp.com")


def get_contact(phone, driver):
    driver.get('https://web.whatsapp.com/send?phone=' + str(phone))
    print('Loaded contact: {}'.format(phone))


def find_text_input(driver, inp_xpath='//div[@title="Type a message"]'):
    input_box = driver.find_element(by=By.XPATH, value=inp_xpath)
    print('FOUND INPUT ELEMENT')
    # print(input_box)
    return input_box


def enter_message(text, input_box):
    input_box.send_keys(text)  # + Keys.ENTER)
    print('ENTERED MESSAGE')


def send_message(input_box):
    input_box.send_keys(Keys.ENTER)
    print('Sent message')


def get_contact_compose_and_send(driver, text_messages, phone, inp_xpath='//div[@title="Type a message"]'):
    get_contact(phone, driver)
    time.sleep(8)
    input_box = find_text_input(driver, inp_xpath=inp_xpath)
    time.sleep(2)
    for text in text_messages:
        enter_message(text=text, input_box=input_box)
        time.sleep(1)
        send_message(input_box)
        time.sleep(2)


def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))
