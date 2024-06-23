from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_to_instagram(username, password):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.instagram.com/accounts/login/')

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, 'username')))
    except:
        print("Login page did not load properly.")
        driver.quit()
        return None

    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[text()='']")))
    except:
        print("Login failed or took too long.")
        driver.quit()
        return None

    return driver

def get_chat_messages(driver):
    driver.get('https://www.instagram.com/direct/inbox/')

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll')))
    except:
        print("Messages page did not load properly.")
        driver.quit()
        return []

    messages = []
    chats = driver.find_elements(By.CSS_SELECTOR, 'div._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll')

    for chat in chats:
        chat.click()
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll')))
        except:
            print("Chat did not load properly.")
            continue

        message_elements = driver.find_elements(By.CSS_SELECTOR, 'div._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll')
        messages.extend([message.text for message in message_elements])

        driver.back()
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._7UhW9.xLCgt.qyrsm.KV-D4.se6yk.T0kll')))
        except:
            print("Inbox did not load properly.")
            continue

    return messages

def get_user_profile(driver, user_handle):
    driver.get(f'https://www.instagram.com/{user_handle}/')

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
    except:
        print("Profile page did not load properly.")
        driver.quit()
        return {}

    profile = {
        'username': user_handle,
        'name': driver.find_element(By.CSS_SELECTOR, 'h1').text,
        'bio': driver.find_element(By.CSS_SELECTOR, 'div.-vDIg span').text,
        'followers': driver.find_element(By.CSS_SELECTOR, 'a.-nal3 span').get_attribute('title'),
        'following': driver.find_element(By.CSS_SELECTOR, 'a.-nal3:nth-child(3) span').text,
    }

    return profile

if __name__ == "__main__":
    username = 'imjustakid578'
    password = '@57masterbaiter'
    user_handle = 'imjustakid578'

    driver = login_to_instagram(username, password)
    if driver:
        messages = get_chat_messages(driver)
        print("Messages:", messages)

        profile = get_user_profile(driver, user_handle)
        print("User Profile:", profile)

        driver.quit()


