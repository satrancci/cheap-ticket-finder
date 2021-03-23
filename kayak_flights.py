from selenium import webdriver
from bs4 import BeautifulSoup as bs
import base64
from time import sleep
from random import randint


BASE_URL = "https://www.kayak.com/flights/ORD-SFO/2021-04-06/2021-04-12?sort=price_a"

results_list_xpath = "//div[@id='searchResultsList']"


def process_page(driver, base_url, timeout=20):
    print(f"[PROCESS_PAGE]: Going to {base_url}")
    driver.get(base_url)
    print(f"[PROCESS_PAGE]: Sleeping for {timeout} seconds...")
    sleep(timeout)

    print(f"[PROCESS_PAGE]: Looking for the alert close button...")
    # The alert handling can certainly be improved
    buttons = driver.execute_script(f"return document.getElementsByClassName('Button-No-Standard-Style close darkIcon');")
    button = None
    for b in buttons:
        id = b.get_attribute("id")
        id_parts = id.split('-')
        if len(id_parts[0]) < 6 and id_parts[1] == "dialog" and id_parts[2] == "close": 
            button = b
    if not button:
        print(f"[PROCESS_PAGE]: Could not find the alert close button...Returning...")
        return
    print(f"[PROCESS_PAGE]: Alert close button found!")
    print(f"[PROCESS_PAGE]: Closing the alert dialog...")
    button.click()

    print(f"[PROCESS_PAGE]: Sleeping for {timeout*2} seconds...")
    sleep(timeout*2)

    zoom_pct = 50
    print(f"[PROCESS_PAGE]: Zooming out to {zoom_pct}%...")
    driver.execute_script(f"return document.body.style.zoom='{zoom_pct}%'")

    print(f"[PROCESS_PAGE]: Taking screenshot...")
    image = driver.get_screenshot_as_base64()

    print(f"[PROCESS_PAGE]: Storing the screenshot...")
    with open(f"kayak_flights_screenshot.png","wb") as f:
        f.write(base64.b64decode(image))


    print(f"[PROCESS_PAGE]: Finding the results list element...")
    try:
        results_list = driver.find_element_by_xpath(results_list_xpath).get_attribute("outerHTML")
        print(f"[PROCESS_PAGE]: Results element found")
    except Exception as exc:
        print(f"[PROCESS_PAGE]: Could not find results list element by xpath: {exc}")
        raise
    
    try:
        print(f"[PROCESS_PAGE]: Parsing the results list element and extracting prices...")
        soup = bs(results_list, "html.parser")
        results = list(filter(lambda x: x!="\n", list(filter(lambda x: x!="\n", list(soup.children)[0]))[0]))
        prices = soup.find_all('span', {'class': 'price-text'})
        prices = sorted(list(map(lambda x: int(x.text.strip()[1:]), prices)))
        print(f"[PROCESS_PAGE]: Prices parsed: {prices}")
    except Exception as exc:
        print(f"[PROCESS_PAGE]: Could not extract prices from the results list: {exc}")
        raise
    try:
        print(f"[PROCESS_PAGE]: Writing prices to disk...")
        with open("prices.txt", "w") as f:
            for price in prices:
               f.write(str(price))
               f.write('\n')
        print(f"[PROCESS_PAGE]: Prices successfully written to disk...")
    except Exception as exc:
        print(f"[PROCESS_PAGE]: Could not write to disk: {exc}")



def run(base_url, timeout=5):

    driver = None
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--no-sandbox')
    driver=webdriver.Chrome('/usr/bin/chromedriver', options=options)
    driver.set_window_size(1920,1080)


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
    print(f"[RUNNER]: Sleeping for {timeout} seconds...")
    sleep(timeout)
    driver.quit()



if __name__=='__main__':
    run(BASE_URL)