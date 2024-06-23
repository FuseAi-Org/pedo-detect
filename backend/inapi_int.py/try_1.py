from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException  # Import the exception

def login_to_instagram(username, password):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.instagram.com/accounts/login/')

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
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
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="Instagram"]')))
    except:
        print("Login failed or took too long.")
        print(driver.page_source)  # Print page source for debugging
        driver.quit()
        return None

    return driver

def is_on_home_page(driver):
    try:
        driver.find_element(By.XPATH, '//*[@id="mount_0_0_cv"]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div/div[1]/div/span/div/a/div')
        return True
    except:
        return False

def is_on_chat_page(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, 'div[role="dialog"]')
        return True
    except:
        return False

def get_chat_messages(driver):
    driver.get('https://www.instagram.com/direct/inbox/')

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]')))
    except:
        print("Messages page did not load properly.")
        driver.quit()
        return []

    messages = []
    while True:
        try:
            chats = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="dialog"]')))
            for chat in chats:
                try:
                    chat.click()
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]')))
                    message_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"]')
                    messages.extend([message.text for message in message_elements])
                    driver.back()
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="dialog"]')))
                except StaleElementReferenceException:
                    print("Stale element reference encountered. Refetching the element.")
                    break  # Exit the for loop and refetch all chat elements
        except:
            print("Failed to refetch chat elements.")
            break  # Exit the while loop

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
    username = 'imjustakid578'  # Input your Instagram username here
    password = '@57masterbaiter'  # Input your Instagram password here
    user_handle = 'imjustakid578'    # Input the target user's handle here

    driver = login_to_instagram(username, password)
    if driver:
        if is_on_home_page(driver):
            print("Successfully logged in and on the home page.")
        else:
            print("Not on the home page.")

        messages = get_chat_messages(driver)
        print("Messages:", messages)

        profile = get_user_profile(driver, user_handle)
        print("User Profile:", profile)

        driver.quit()
