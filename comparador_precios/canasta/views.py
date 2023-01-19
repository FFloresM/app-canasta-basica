from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from .forms import ProductoForm
import urllib
from playwright.sync_api import sync_playwright

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
    url_jumbo = 'https://www.jumbo.cl/busqueda'
    url_unimarc = 'https://www.unimarc.cl/search'
    producto = producto.replace(' ', urllib.parse.quote(' ')) #palabras con espacios ##ñs se mantienen
    payload = {'ft': producto}
    url_jumbo+=f"?ft={producto}"
    url_unimarc += f"?q={producto}"
    with sync_playwright() as p:
        #jumbo
        browser = p.chromium.launch()
        page1 = browser.new_page()
        page2 = browser.new_page()
        page2.goto(url_unimarc)
        page1.goto(url_jumbo)
        page1.wait_for_selector('div.shelf-product-island')
        all_items = page1.locator('.shelf-product-island ')
        all_urls = page1.locator('div.shelf-product-top-island > div.shelf-product-image-island > a')
        data_jumbo = []
        for item, url in zip(all_items.all_inner_texts(), all_urls.all()):
            item = item.split('\n')[:4]
            item_dict = {
                'brand': item[0],
                'name': item[1],
                'unit': item[2],
                'price': item[3],
                'url': url.get_attribute('href')
            }
            data_jumbo.append(item_dict)
        #unimarc
        all_items = page2.locator('#__NEXT_DATA__')
        data = json.loads(all_items.all_inner_texts()[0])
        data_unimarc = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']
        browser.close()

    context = {
        'data_jumbo': data_jumbo,
        'data_unimarc': data_unimarc,
    }
    return render(request, 'canasta/prods_list.html', context=context)

