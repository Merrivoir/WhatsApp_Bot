from selenium import webdriver

profile_path = r'C:\Users\Paul Lvov\AppData\Roaming\Mozilla\Firefox\Profiles\qa82eqx1.default'
options = webdriver.FirefoxOptions()
options.add_argument("--start-maximized")
options.add_argument('-profile')
options.add_argument(profile_path)

driver = webdriver.Firefox(options=options)

driver.get('https://web.whatsapp.com/')