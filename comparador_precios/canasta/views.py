from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from .forms import ProductoForm

url = 'https://www.jumbo.cl/busqueda?ft='

def index(request):
    if request.method == 'GET':
        form = ProductoForm(request.GET)
        if form.is_valid():
            prod = form.cleaned_data['producto']
            return HttpResponseRedirect(f'{prod}/buscar')
    else:
        form = ProductoForm()
    return render(request, 'canasta/index.html', {'form': form})

def buscar(request, prod):
    url += prod
    r = requests.get(url)
    context = {
        'data': r.json(),
    }
    return render(request, 'canasta/prods_list.html', context=context)

