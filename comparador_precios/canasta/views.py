from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
import requests
from .forms import ProductoForm
from bs4 import BeautifulSoup
from django.conf import settings

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
    url = 'https://www.jumbo.cl/busqueda'
    payload = {'ft': producto}
    #url += producto
    response = requests.get(url, params=payload, verify=settings.BASE_DIR / 'Zscaler_Root_CA.crt')
    print(response.url)
    if response.status_code != 204:
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding='UTF-8')
        scripts = soup.find_all('script')
        scripts_validos = []
        for script in scripts:
            if "application/ld+json" in script.attrs.values():
                scripts_validos.append(script.contents[0])
        scrp = scripts_validos[1]
        data = json.loads(scrp)
        context = {
            'data': data,
        }
    return render(request, 'canasta/prods_list.html', context=context)

