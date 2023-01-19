from bs4 import BeautifulSoup
import requests
import json

#with open('vino.html', encoding='UTF-8') as fp:
#    soup = BeautifulSoup(fp, 'html.parser', from_encoding='UTF-8')

url = 'https://www.unimarc.cl/search'
item = 'palta'
payload = {'q': item}
response = requests.get(url, params=payload)
print(response.url)
print(response.headers)
soup = BeautifulSoup(response.content, 'html.parser', from_encoding='UTF-8')
scripts = soup.find_all('script')
scripts_validos = []
for script in scripts:
    if "__NEXT_DATA__" in script.attrs.values():
        scripts_validos.append(script.contents[0])
#unimarc
#print(scripts_validos)
scrp = scripts_validos[0]
x = json.loads(scrp)
for element in x['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['data']['availableProducts']:
    print(element['name'], f"${element['sellers'][0]['price']}", sep='\t\t\t')


