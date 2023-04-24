from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
from .forms import ProductoForm
import urllib
from playwright.sync_api import sync_playwright
import time
from .models import *
from .utils import price2int, Producto
from asgiref.sync import sync_to_async

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
    producto_URL = producto.replace(' ', urllib.parse.quote(' ')) #palabras con espacios ##ñs se mantienen
    payload = {'ft': producto_URL}
    url_jumbo+=f"?ft={producto_URL}"
    url_unimarc += f"?q={producto_URL}"
    url_lider+=f"?query={producto_URL}"
    url_santa += f"?ft={producto_URL}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page1 = context.new_page()
        page2 = context.new_page()
        page3 = context.new_page()
        page4 = context.new_page()
        page1.goto(url_jumbo)
        page2.goto(url_unimarc)
        page3.goto(url_lider)
        page4.goto(url_santa)

        #get data jumbo
        page1.locator('div.shelf-product-island')
        all_items = page1.locator('.shelf-product-island ')
        all_urls = page1.locator('div.shelf-product-top-island > div.shelf-product-image-island > a')
        all_items_txt = all_items.all_inner_texts()
        all_urls_txt = [url.get_attribute('href') for url in  all_urls.all()]
        data_jumbo = buscar_jumbo(all_items_txt, all_urls_txt, producto) #lista de productos
        
        #unimarc
        all_items = page2.locator('#__NEXT_DATA__')
        data = json.loads(all_items.all_inner_texts()[0])
        items_unimarc = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['availableProducts']
        print("__UNIMARC__\n")
        data_unimarc = []
        for item in items_unimarc:
            print(item)
            if producto.lower() in item['name'].lower():
                data_unimarc.append(item)
        
        #lider
        page3.locator('ul.ais-Hits-list')
        item_list = page3.locator('ul.ais-Hits-list')
        all_items_brands = item_list.locator('div.product-info > h2 > div > div > span:nth-child(1)')
        all_items_names = item_list.locator('div.product-info > h2 > div > div > span:nth-child(2)')
        all_items_prices = item_list.locator('div.product-info > div > div.walmart-sales-price.d-flex > div.product-card__sale-price > span')
        all_urls = item_list.locator('li.ais-Hits-item > div > div > a')
        brands_txt = all_items_brands.all_inner_texts()
        names_txt = all_items_names.all_inner_texts()
        prices_txt = all_items_prices.all_inner_texts()
        urls_txt = [url.get_attribute('href') for url in all_urls.all()]
        data_lider = buscar_lider(brands_txt, names_txt, prices_txt, urls_txt, producto)
        
        #santa
        page4.locator('div.shelf-product-island')
        all_items = page4.locator('.shelf-product-island')
        all_urls = page4.locator('div.shelf-product-top-island > div.shelf-product-image-island > a')
        all_items_txt = all_items.all_inner_texts()
        all_urls_txt = [url.get_attribute('href') for url in  all_urls.all()]
        data_santa = buscar_santa(all_items_txt, all_urls_txt, producto)
        browser.close()
    end = time.time()
    print(f"tiempo consultas: {end-start}")
    context = {
        'data_unimarc': data_unimarc,
        'data_lider': data_lider,
        'data_santa': data_santa,
        'data_jumbo': data_jumbo,
    }
    return render(request, 'canasta/prods_list.html', context=context)

def buscar_jumbo(all_items, all_urls, producto):
    data_jumbo = []
    raw_data_jumbo = []
    print("__JUMBO__")
    for item, url in zip(all_items, all_urls):
        item = item.split('\n')
        if 'Oferta' in item: item.remove('Oferta')
        if 'Cenco Black' in item: item.remove('Cenco Black')
        if 'Exclusivo Internet' in item: item.remove('Exclusivo Internet')
        print(item)
        result = serchProductInResult(producto, " ".join(item))
        if checkResult(result): #producto in brand or name 
            prod = Producto()
            prod.setNombre(item[1])
            prod.setMarca(item[0])
            prod.setUnidadMedida(item[2])
            prod.setURL(url)
            prod.setListaPrecios(item[3:-2])
            print(prod)
            data_jumbo.append(prod)
        raw_data_jumbo.append(item)
    return data_jumbo

def buscar_santa(all_items, all_urls, producto):
    data_santa = []
    print("__SANTA ISABEL__")
    for item, url in zip(all_items, all_urls):
        item = item.split('\n')
        if 'Oferta' in item: item.remove('Oferta')
        if 'Producto sin stock' in item: continue #ignore item sin stock
        if 'Cenco Black' in item: item.remove('Cenco Black')
        if 'Exclusivo Internet' in item: item.remove('Exclusivo Internet')
        print(item)
        result = serchProductInResult(producto, " ".join(item))
        if checkResult(result):
            prod = Producto()
            prod.setNombre(item[1])
            prod.setMarca(item[0])
            prod.setUnidadMedida(item[2])
            prod.setURL(url)
            prod.setListaPrecios(item[3:-2])
            print(prod)
            data_santa.append(prod)
    return data_santa

def buscar_lider(brands_txt, names_txt, prices_txt, urls_txt, producto):
    data_lider = []
    print("__LIDER__")
    for name, brand, price, url in zip(names_txt, brands_txt, prices_txt, urls_txt):
        print(f"{brand} {name} {price} {url}")
        result = serchProductInResult(producto, " ".join([brand,name]))
        if checkResult(result):
            prod = Producto()
            prod.setNombre(name.split(',', 1)[0])
            prod.setMarca(brand)
            prod.setUnidadMedida(name.split(',', 1)[1])
            prod.setURL(url)
            prod.setPrecio(price2int(price))
            print(prod)
            data_lider.append(prod)
    return data_lider

@sync_to_async
def save_data(data, supermarket):
    superMarket, _ = Supermarket.objects.get_or_create(name=supermarket)
    for item in data:
        brand, _ = Brand.objects.get_or_create(
            brand_name = item['brand']
        )
        product, _ = Product.objects.get_or_create(
            name = item['name'],
            format = item['unit'],
            brand = brand,
            measurementUnit = item['priceByUnit']
        )
        try:
            unitPrice_ = price2int(item['prices'][0])
        except:
            unitPrice_ = price2int(item['prices'][1])
        sell, _ = Sell.objects.update_or_create(
            detailURL = item['url'],
            item = product,
            supermarket = superMarket,
            unitPrice = unitPrice_    
        )
        print(sell, _)

def serchProductInResult(product, searchable):
    product = [word.lower() for word in product.split()]
    searchable = searchable.lower()
    result = {word:False for word in product}
    for name in product:
        if name in searchable:
            result[name] = True
            continue
    return result

def checkResult(result):
    boolean_result = True
    for value in result.values():
        boolean_result |= value
    return boolean_result