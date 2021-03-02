from selenium import webdriver
from time import sleep
import base64
from random import randint

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument('--no-sandbox')
driver=webdriver.Chrome('/usr/bin/chromedriver', options=options)

print('driver configured!')

driver.get("https://www.kayak.com/flights")
print("sleeping for 10 seconds...")
sleep(10)

image = driver.get_screenshot_as_base64()

i = randint(1,1000)
print('i:', i)
with open(f"kayak_{i}.png","wb") as f:
    f.write(base64.b64decode(image))


driver.quit()