from playwright.sync_api import sync_playwright
import urllib
import time

url_santa = 'https://www.santaisabel.cl/busqueda'
producto = 'cafe'
producto = producto.replace(' ', urllib.parse.quote(' ')) #palabras con espacios ##ñs se mantienen
payload = {'ft': producto}
url_santa+=f"?ft={producto}"
print(url_santa)
start = time.time()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url_santa)
    page.wait_for_selector('div.shelf-product-island')
    all_items = page.locator('.shelf-product-island ')
    all_urls = page.locator('div.shelf-product-top-island > div.shelf-product-image-island > a')
    for url in all_urls.all():
        print(url.get_attribute('href'))
    print(all_items.all_inner_texts())
    #for item in all_items.all_inner_texts():
    #    item = item.split('\n')
    #    item = '__'.join(item)
    #    print(item)
    browser.close()
end = time.time()
print(end - start)