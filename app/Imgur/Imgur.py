from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from imgurpython import ImgurClient
from dotenv import dotenv_values


def authenticate():
    # Get client ID and secret from auth.ini
    config = dotenv_values(".env")
    client_id = config['CLIENT_ID']
    client_secret = config['CLIENT_SECRET']

    client = ImgurClient(client_id, client_secret)
    # Authorization flow, pin example (see docs for other auth types)
    authorization_url = client.get_auth_url('pin')

    driver = webdriver.Chrome
    driver.get(driver, authorization_url)

    username = driver.find_element_by_xpath('//*[@id="username"]')
    password = driver.find_element_by_xpath('//*[@id="password"]')
    username.clear()
    username.send_keys(config['IMGUR_USERNAME'])
    password.send_keys(config['IMGUR_PASSWORD'])

    driver.find_element_by_name("allow").click()

    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.ID, 'pin'))
        WebDriverWait(driver, timeout).until(element_present)
        pin_element = driver.find_element_by_id('pin')
        pin = pin_element.get_attribute("value")
    except TimeoutException:
        print("Timed out waiting for page to load")

    driver.close()

    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(config['access_token'], config['refresh_token'])
    print("Authentication successful!")

    return client