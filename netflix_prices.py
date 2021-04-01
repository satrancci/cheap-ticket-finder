from selenium import webdriver
from bs4 import BeautifulSoup as bs
import base64
from time import sleep
from random import randint


BASE_URL = "https://help.netflix.com/en/node/24926"


def process_page(driver, base_url, timeout=20):
    print(f"[PROCESS_PAGE]: Going to {base_url}")
    driver.get(base_url)
    print(f"[PROCESS_PAGE]: Sleeping for {timeout} seconds...")
    sleep(timeout)


    zoom_pct = 50
    print(f"[PROCESS_PAGE]: Zooming out to {zoom_pct}%...")
    driver.execute_script(f"return document.body.style.zoom='{zoom_pct}%'")

    print(f"[PROCESS_PAGE]: Taking screenshot...")
    image = driver.get_screenshot_as_base64()

    print(f"[PROCESS_PAGE]: Storing the screenshot...")
    with open(f"./data/nflx.png","wb") as f:
        f.write(base64.b64decode(image))



def run(base_url, timeout=5):

    userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    print(f"[RUNNER]: user-agent: {userAgent}")

    driver = None
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument(f'user-agent={userAgent}')
    driver=webdriver.Chrome('/usr/bin/chromedriver', options=options)



    print(f"[RUNNER]: Chrome driver successfully configured")
    try:
        print(f"[RUNNER]: Processing page...")
        process_page(driver, base_url)
        print(f"[RUNNER]: Page successfully processed.")
    except Exception as exc:
        print(f"[RUNNER]: Page could not be processed: {exc}")
        raise

    print("[RUNNER]: Crawling successfully done!")
    print("[RUNNER]: Quitting the driver...")
    print(f"[RUNNER]: Sleeping for {timeout*10} seconds...")
    sleep(timeout*10)
    driver.quit()



if __name__=='__main__':
    run(BASE_URL)