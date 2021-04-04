import sys
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import base64
from time import sleep
from random import randint

from parse_selenium_args import *

### Validation ###

try:
    print(f"[kayak_flights.py]: Validating arguments...")
    args = sys.argv
    ret_code, COUNTRY_CODE, DATA_ID, TRAVEL_TYPE, AIRPORT_ORIG, AIRPORT_DEST, FLIGHT_DATE = parse_flight_args(args)
    if ret_code != 0:
        print(f"[kayak_flights.py]: Could not import or parse arguments")
        raise
    print(f"[kayak_flights.py]: imported the following arguments: COUNTRY_CODE: {COUNTRY_CODE}, DATA_ID={DATA_ID}, TRAVEL_TYPE={TRAVEL_TYPE}, AIRPORT_ORIG={AIRPORT_ORIG}, AIRPORT_DEST:{AIRPORT_DEST}, FLIGHT_DATE: {FLIGHT_DATE}")
except Exception as exc:
    print(f"[kayak_flights.py]: Could not import or parse arguments {exc}")
    raise

### End of validation ###

### Kayak constants ###

BASE_URL = f"https://www.kayak.com/flights/{AIRPORT_ORIG}-{AIRPORT_DEST}/{FLIGHT_DATE}?sort=price_a"

RESULTS_LIST_XPATH = "//div[@id='searchResultsList']"

### End of Kayak constants ###

##### Functions #####

def process_page(driver, base_url, country_code, data_id):

    BASE_DIR = "data"
    ZOOM_PCT = 50
    TIMEOUT = randint(20,30)
    FILENAME_BASE= f"./{BASE_DIR}/{data_id}_{country_code}"

    print(f"[PROCESS_PAGE]: Going to {base_url}")
    driver.get(base_url)
    print(f"[PROCESS_PAGE]: Sleeping for {TIMEOUT} seconds...")
    sleep(TIMEOUT)

    print(f"[PROCESS_PAGE]: Looking for the alert close button...")
    # The alert handling can certainly be improved

    try:
        buttons = driver.execute_script(f"return document.getElementsByClassName('Button-No-Standard-Style close darkIcon');")
        button = None
        for b in buttons:
            id = b.get_attribute("id")
            id_parts = id.split('-')
            if len(id_parts[0]) < 6 and id_parts[1] == "dialog" and id_parts[2] == "close": 
                button = b
        if button is None:
            print(f"[PROCESS_PAGE]: Could not find the alert close button...")
            print(f"[PROCESS_PAGE]: Taking screenshot to identify problem... Zooming out to {ZOOM_PCT}%...")
            driver.execute_script(f"return document.body.style.zoom='{ZOOM_PCT}%'")

            print(f"[PROCESS_PAGE]: Taking screenshot...")
            image = driver.get_screenshot_as_base64()
            print(f"[PROCESS_PAGE]: Storing the screenshot...")
            with open(FILENAME_BASE+"_1.png","wb") as f: # 1 stands for error
                f.write(base64.b64decode(image))
            return
    except Exception as exc:
        print(f"[PROCESS_PAGE]: Something went wrong during alert button discovery: {exc}")
        raise

    print(f"[PROCESS_PAGE]: Alert close button found!")
    print(f"[PROCESS_PAGE]: Closing the alert dialog...")
    button.click()

    print(f"[PROCESS_PAGE]: Sleeping for {TIMEOUT*2} seconds...")
    sleep(TIMEOUT*2)

    try:
        print(f"[PROCESS_PAGE]: Finding the results list element...")
        results_list = driver.find_element_by_xpath(RESULTS_LIST_XPATH).get_attribute("outerHTML")
        print(f"[PROCESS_PAGE]: Results element found")
    except Exception as exc:
        print(f"[PROCESS_PAGE]: Could not find results list element by xpath: {exc}")
        raise
    
    try:
        print(f"[PROCESS_PAGE]: Parsing the results list element and extracting prices...")
        soup = bs(results_list, "html.parser")
        results = list(filter(lambda x: x!="\n", list(filter(lambda x: x!="\n", list(soup.children)[0]))[0]))
        prices = soup.find_all('span', {'class': 'price-text'})
        prices = sorted(list(map(lambda x: int(x.text.strip()[1:].replace(',', '')), prices)))
        print(f"[PROCESS_PAGE]: Prices parsed: {prices}")
    except Exception as exc:
        print(f"[PROCESS_PAGE]: Could not extract prices from the results list: {exc}")
        raise
    try:
        print(f"[PROCESS_PAGE]: Writing prices to disk...")
        with open(FILENAME_BASE+"_prices.txt", "w") as f:
            for price in prices:
               f.write(str(price))
               f.write('\n')
        print(f"[PROCESS_PAGE]: Prices successfully written to disk...")
    except Exception as exc:
        print(f"[PROCESS_PAGE]: Could not write to disk: {exc}")
        raise

    try:
        print(f"[PROCESS_PAGE]: Zooming out to {ZOOM_PCT}%...")
        driver.execute_script(f"return document.body.style.zoom='{ZOOM_PCT}%'")

        print(f"[PROCESS_PAGE]: Taking screenshot...")
        image = driver.get_screenshot_as_base64()

        print(f"[PROCESS_PAGE]: Storing the screenshot...")
        with open(FILENAME_BASE+"_0.png","wb") as f: # 0 for success
            f.write(base64.b64decode(image))
    except Exception as exc:
        print(f"[PROCESS_PAGE]: Could not take screenshot on success: {exc}")
        raise


def run(base_url, country_code, data_id):

    TIMEOUT = randint(5,10)

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
    driver.set_window_size(1024,768)
    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


    print(f"[RUNNER]: Chrome driver successfully configured")
    try:
        print(f"[RUNNER]: Processing page...")
        process_page(driver, base_url, country_code, data_id)
        print(f"[RUNNER]: Page successfully processed.")
    except Exception as exc:
        print(f"[RUNNER]: Page could not be processed: {exc}")
        raise

    print("[RUNNER]: Crawling successfully done!")
    print("[RUNNER]: Quitting the driver...")
    print(f"[RUNNER]: Sleeping for {TIMEOUT} seconds...")
    sleep(TIMEOUT)
    driver.quit()



if __name__=='__main__':
    run(BASE_URL, COUNTRY_CODE, DATA_ID)