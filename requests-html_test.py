from requests_html import HTMLSession
import requests
"""
session = HTMLSession()
url = 'https://www.lider.cl/supermercado/search'
item = 'vino'
payload = {'query': item}

r = session.get(url, params=payload, verify='lider.cl.crt')
print(r.url)
r.html.render()

print(r)

"""
r = requests.get('https://apis.santaisabel.cl/catalog/api/v1/pedrofontova/search/leche?page=1',)