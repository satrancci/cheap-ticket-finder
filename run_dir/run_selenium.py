import sys
from selenium import webdriver
from time import sleep
import base64

URL = "https://www.kayak.com/flights"

try:
    args = sys.argv
    server_code = args[1]
except Exception as exc:
    print(f"[run_selenium.py][{server_code}]: Usage: python3 run_selenium.py <server_code>: {exc}")

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument('--no-sandbox')
driver=webdriver.Chrome('/usr/bin/chromedriver', options=options)

print(f"[run_selenium.py][{server_code}]: driver configured!")
print(f"[run_selenium.py][{server_code}]: Going to {URL}...")

driver.get(URL)

print(f"[run_selenium.py][{server_code}]: sleeping for 10 seconds...")
sleep(10)

print(f"[run_selenium.py][{server_code}]: taking the screenshot...")
image = driver.get_screenshot_as_base64()

print(f"[run_selenium.py][{server_code}]: storing the screenshot..")
with open(f"{server_code}.png","wb") as f:
    f.write(base64.b64decode(image))


driver.quit()