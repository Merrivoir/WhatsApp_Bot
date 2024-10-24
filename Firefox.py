from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, SessionNotCreatedException
from time import sleep
from datetime import datetime
import urllib.parse
import random

options = webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument('C:\\Users\\Merri\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ui70pfgh.default-release')

driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/"
driver.get(url)