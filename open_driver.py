from selenium import webdriver

print(f"----------------------------------------------------------------------------")
print(f"Скрипт open_driver начал работу")

number = input("Введите номер WhatsApp: ")
options = webdriver.FirefoxOptions()

options.set_preference("devtools.debugger.remote-enabled", True)
options.set_preference("devtools.debugger.remote-port", 9223)
options.add_argument('-profile')
options.add_argument('C:\\MEGA\\profiles\\firefox\\' + number)

driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/"
driver.get(url)

print(f"Драйвер запущен")
print(f"----------------------------------------------------------------------------")
