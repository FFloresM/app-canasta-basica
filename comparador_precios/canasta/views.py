from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from .forms import ProductoForm
import urllib
from playwright.sync_api import sync_playwright
import time

def index(request):
    if request.method == 'GET':
        form = ProductoForm(request.GET)
        if form.is_valid():
            prod = form.cleaned_data['producto']
            return HttpResponseRedirect(f'buscar/{prod}')
    else:
        form = ProductoForm()
    return render(request, 'canasta/index.html', {'form': form})

def buscar(request, producto):
    start = time.time()
    url_jumbo = 'https://www.jumbo.cl/busqueda'
    url_unimarc = 'https://www.unimarc.cl/search'
    url_lider = 'https://www.lider.cl/supermercado/search'
    url_santa = 'https://www.santaisabel.cl/busqueda'
    producto = producto.replace(' ', urllib.parse.quote(' ')) #palabras con espacios ##ñs se mantienen
    payload = {'ft': producto}
    url_jumbo+=f"?ft={producto}"
    url_unimarc += f"?q={producto}"
    url_lider+=f"?query={producto}"
    url_santa += f"?ft={producto}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page1 = context.new_page()
        page2 = context.new_page()
        page3 = context.new_page()
        page4 = context.new_page()
        page2.goto(url_unimarc)
        page1.goto(url_jumbo)
        page3.goto(url_lider)
        page4.goto(url_santa)
        #jumbo
        page1.locator('div.shelf-product-island')
        all_items = page1.locator('.shelf-product-island ')
        all_urls = page1.locator('div.shelf-product-top-island > div.shelf-product-image-island > a')
        data_jumbo = []
        for item, url in zip(all_items.all_inner_texts(), all_urls.all()):
            item = item.split('\n')
            item_dict = {
                'brand': item[0],
                'name': item[1],
                'unit': item[2],
                'prices': item[3:-2],
                'url': url.get_attribute('href')
            }
            data_jumbo.append(item_dict)
        #unimarc
        all_items = page2.locator('#__NEXT_DATA__')
        data = json.loads(all_items.all_inner_texts()[0])
        data_unimarc = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']
        #lider
        page3.locator('ul.ais-Hits-list')
        all_items_names = page3.locator('div.product-info > h2 > div > div')
        all_items_prices = page3.locator('div.product-info > div > div.walmart-sales-price.d-flex > div.product-card__sale-price > span')
        all_urls = page3.locator('li.ais-Hits-item > div > div > a')
        data_lider = [{'name': name, 'price': price, 'url': url.get_attribute('href')} for name, price, url in zip(all_items_names.all_inner_texts(), all_items_prices.all_inner_texts(), all_urls.all())]
        #santa
        page4.locator('div.shelf-product-island')
        all_items = page4.locator('.shelf-product-island')
        all_urls = page4.locator('div.shelf-product-top-island > div.shelf-product-image-island > a')
        data_santa = []
        for item, url in zip(all_items.all_inner_texts(), all_urls.all()):
            item = item.split('\n')
            item_dict = {
                'brand': item[0],
                'name': item[1],
                'unit': item[2],
                'prices': item[3:-2],
                'url': url.get_attribute('href')
            }
            data_santa.append(item_dict)
        browser.close()
    end = time.time()
    print(f"tiempo consultas: {end-start}")
    context = {
        'data_jumbo': data_jumbo,
        'data_unimarc': data_unimarc,
        'data_lider': data_lider,
        'data_santa': data_santa,
    }
    return render(request, 'canasta/prods_list.html', context=context)

