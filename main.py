from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import extension

service = Service(executable_path='../webdriver/chromedriver.exe')
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--window-size=640,560")
chrome_options.add_argument('--disable-dev-shm-usage')


def scrape(csv_file):
    data = extension.read_csv(csv_file)
    scraped = []
    driver = webdriver.Chrome(service=service, options=chrome_options)

    for item in data:
        item_id = item[1]
        asin = item[2]
        country = item[3]
        url = 'https://amazon.{}/dp/{}'.format(country, asin)
        driver.get(url)
        page = BeautifulSoup(driver.page_source, "html.parser")
        title = page.select_one('#productTitle')
        # Use the product title selector to check whether a product exists
        if title is None:
            print('URL not avaiable: {}'.format(url))
            continue
        else:
            title = title.text.strip()

        # Different pages use different kind of image placement and selectors
        img = page.select_one('#landingImage') or page.select_one('#imgTagWrapperId img') or page.select_one('#imgBlkFront')
        if img is not None:
            img = img['src']
        else: img = ""

        price = page.select_one('#price')
        if price is None:
            price = page.select_one('.swatchElement a span.a-color-base')
            if price is None:
                price = page.select_one('#corePrice_feature_div span.a-price .a-offscreen').text
            else:
                price = price.text.strip()
        else:
            price = price.text

        # The details list is stored in key value pairs
        details_list = page.select('div#detailBullets_feature_div>ul span.a-list-item')
        details = []
        for detail in details_list:
            key = detail.select_one('span.a-text-bold').text.strip()
            key = key[:key.find('\n')]
            value = detail.select_one('span.a-text-bold+span').text.strip()
            details.append({key: value})

        item_info = {
            "id": item_id,
            "asin": asin,
            "country": country,
            "title": title,
            "price": price,
            "image": img,
            "details": details
        }
        scraped.append(item_info)

    driver.close()
    return scraped


if __name__ == "__main__":
    scraped_data = scrape('Amazon Scraping - Sheet1')
    if len(scraped_data) > 0:
        extension.save_json(scraped_data, 'items')
