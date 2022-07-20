from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from selenium.webdriver import Safari, Chrome # pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import tkinter as tk

chrome_driver_manager = ChromeDriverManager().install()
# chromeDriver = Chrome(service=Service(chrome_driver_manager))

safariDriver = Safari()
safariDriver.maximize_window()

def init_tradingview():
    
    safariDriver.get('https://www.tradingview.com/#signin')
    tradingViewuserName = 'MARCO_DE_TOMASI'
    tradingViewPassword = 'Detomasi00'
    delay()
    button_email = safariDriver.find_element(By.CLASS_NAME, 'js-show-email')
    button_email.click()
    delay()
    try:
        safariDriver.find_element(By.CLASS_NAME, 'email').send_keys(tradingViewuserName)
    except:
        try:
            safariDriver.find_element(By.NAME, 'username').send_keys(tradingViewuserName)
        except:
            safariDriver.find_element(By.NAME, 'email').send_keys(tradingViewuserName)

    input_password = safariDriver.find_element(By.NAME, 'password')
    input_password.send_keys(tradingViewPassword)
    input_password.submit()
    time.sleep(1)
    

def get_trading_view_graph(interval, currency, exchange):


    #init_tradingview(safariDriver)
    time.sleep(1)
    safariDriver.get('https://www.tradingview.com/chart/?symbol=' + exchange + ':' + currency)
    delay()
    safariDriver.find_element(By.CLASS_NAME, 'managePreferences-W4Y0hWcd').click()
    delay()
    safariDriver.find_element(By.CLASS_NAME, 'savePreferences-vDbnNLqD').click()
    delay()
    safariDriver.find_element(By.CLASS_NAME, 'menu-cXbh8Gcw').click()
    delay()
    intervals = safariDriver.find_elements(By.CLASS_NAME, 'item-4TFSfyGO')
    if interval == '1m':
        intervals[5].click()
    
    buttons = safariDriver.find_elements(By.CLASS_NAME, 'button-Rsu8YfBx')
    buttons[1].click()
    delay()
    safariDriver.find_elements(By.CLASS_NAME, 'tab-Zcmov9JL')[0].click()
    delay()
    safariDriver.find_element(By.CLASS_NAME, 'input-CcsqUMct').send_keys('ichimoku ' + interval)
    delay()
    safariDriver.find_elements(By.CLASS_NAME, 'main-FkkXGK5n')[0].click()
    delay()
    safariDriver.find_element(By.CLASS_NAME, 'input-CcsqUMct').clear()
    delay
    safariDriver.find_element(By.CLASS_NAME, 'input-CcsqUMct').send_keys('rsi 20-80 ')
    delay()
    safariDriver.find_elements(By.CLASS_NAME, 'main-FkkXGK5n')[1].click()
    safariDriver.find_element(By.CLASS_NAME, 'close-tuOy5zvD').click()
    delay()
    safariDriver.find_element(By.ID, 'header-toolbar-screenshot').click()
    delay()
    safariDriver.find_elements(By.CLASS_NAME, 'item-4TFSfyGO')[2].click()
    delay()
    root = tk.Tk()
    time.sleep(5)
    url = root.clipboard_get()
    return url

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