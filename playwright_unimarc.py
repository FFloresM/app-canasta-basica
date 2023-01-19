from playwright.sync_api import sync_playwright
import urllib
import time
import json

url_unimarc = 'https://www.unimarc.cl/search'
producto = 'queso'
producto = producto.replace(' ', urllib.parse.quote(' ')) #palabras con espacios ##ñs se mantienen
payload = {'q': producto}
url_unimarc+=f"?q={producto}"
print(url_unimarc)
start = time.time()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url_unimarc)
    #page.wait_for_selector('#__NEXT_DATA__')
    all_items = page.locator('#__NEXT_DATA__')
    data = json.loads(all_items.all_inner_texts()[0])
    data_unimarc = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']
    print(data_unimarc)
    #for item in all_items.all_inner_texts():
        #item = item.split('\n')[:4]
        #item = ' '.join(item)
    #    print(item)
    browser.close()
end = time.time()
print(end - start)