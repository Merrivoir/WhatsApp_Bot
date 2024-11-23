from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument('C:\\Users\\Paul Lvov\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\qa82eqx1.default')

driver = webdriver.Firefox(options=options)
