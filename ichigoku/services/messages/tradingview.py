from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from selenium.webdriver import Safari, Edge, Chrome # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from services.utilities import get_interval_index

try:
    driver = Safari()
except:
    try:
        driver = Edge()
    except:
        try:
            chrome_driver_manager = ChromeDriverManager().install()
            driver = Chrome(service=Service(chrome_driver_manager))
        except:
            pass
            # opera_driver_manager = OperaDriverManager().install()
            # driver = Opera(service=Service(opera_driver_manager))
        

def init_tradingview():
    return
    driver.maximize_window()
    driver.get('https://www.tradingview.com/#signin')
    tradingViewuserName = 'MARCO_DE_TOMASI'
    tradingViewPassword = 'Detomasi00'
    # tradingViewuserName = 'tradingviewinvasion@gmail.com'
    # tradingViewPassword = 'Canazza88'
    delay()
    button_email = driver.find_element(By.CLASS_NAME, 'js-show-email')
    button_email.click()
    delay()
    try:
        driver.find_element(By.CLASS_NAME, 'email').send_keys(tradingViewuserName)
    except:
        try:
            driver.find_element(By.NAME, 'username').send_keys(tradingViewuserName)
        except:
            driver.find_element(By.NAME, 'email').send_keys(tradingViewuserName)

    input_password = driver.find_element(By.NAME, 'password')
    input_password.send_keys(tradingViewPassword)
    input_password.submit()
    #time.sleep(20)
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'managePreferences-W4Y0hWcd').click()
    delay()
    driver.find_element(By.CLASS_NAME, 'savePreferences-vDbnNLqD').click()
    delay()
    

def get_trading_view_graph(interval, currency, exchange):
    return None
    try: 
        time.sleep(1)
        driver.get('https://www.tradingview.com/')
        time.sleep(3)
        driver.get('https://www.tradingview.com/chart/?symbol=' + exchange + ':' + currency)
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'menu-cXbh8Gcw').click()
        delay()
        index: int = get_interval_index(interval)
        driver.find_elements(By.CLASS_NAME, 'item-4TFSfyGO')[index].click()
        delay()
        buttons = driver.find_elements(By.CLASS_NAME, 'button-Rsu8YfBx')
        buttons[1].click()
        delay()
        driver.find_elements(By.CLASS_NAME, 'tab-Zcmov9JL')[0].click()
        delay()
        driver.find_element(By.CLASS_NAME, 'input-CcsqUMct').send_keys('ichimoku')
        delay()
        driver.find_elements(By.CLASS_NAME, 'main-FkkXGK5n')[0].click()
        delay()
        driver.find_element(By.CLASS_NAME, 'input-CcsqUMct').clear()
        delay
        driver.find_element(By.CLASS_NAME, 'input-CcsqUMct').send_keys('rsi 20-80 ')
        delay()
        driver.find_elements(By.CLASS_NAME, 'main-FkkXGK5n')[1].click()
        driver.find_element(By.CLASS_NAME, 'close-tuOy5zvD').click()
        delay()
        driver.find_element(By.ID, 'header-toolbar-screenshot').click()
        delay()
        driver.find_elements(By.CLASS_NAME, 'item-4TFSfyGO')[2].click()
        delay()
        root = tk.Tk()
        time.sleep(5)
        url = root.clipboard_get()
        driver.get('https://www.tradingview.com/')
        WebDriverWait(driver, 20).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(5)
        return url
    except:
        return None
    '''
    time.sleep(2)
    screenshotbutton = safariDriver.find_element_by_class_name('getimage')
    screenshotbutton.click()
    time.sleep(3)
    imageLink = safariDriver.find_element_by_class_name('textInput-3WRWEmm7-')
    return(imageLink.get_attribute('value'), safariDriver.current_url)
    '''

def delay():
    time.sleep(1)