from playwright.sync_api import sync_playwright
import urllib
import time

url_lider = 'https://www.lider.cl/supermercado/search'
producto = 'vino'
producto = producto.replace(' ', urllib.parse.quote(' ')) #palabras con espacios ##ñs se mantienen
payload = {'ft': producto}
url_lider+=f"?query={producto}"
print(url_lider)
start = time.time()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url_lider)
    page.wait_for_selector('ul.ais-Hits-list')
    all_items_names = page.locator('div.product-info > h2 > div > div')
    all_items_prices = page.locator('div.product-info > div > div.walmart-sales-price.d-flex > div.product-card__sale-price > span')
    all_urls = page.locator('li.ais-Hits-item > div > div > a')
    print(all_items_names.all_inner_texts())
    print(all_items_prices.all_inner_texts())
    print(all_urls.get_attribute('href'))
    browser.close()
end = time.time()
print(end - start)
