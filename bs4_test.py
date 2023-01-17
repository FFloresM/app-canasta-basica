from bs4 import BeautifulSoup
import json

with open('vino.html', encoding='UTF-8') as fp:
    soup = BeautifulSoup(fp, 'html.parser', from_encoding='UTF-8')

scripts = soup.find_all('script')
scripts_validos = []
for script in scripts:
    if "application/ld+json" in script.attrs.values():
        scripts_validos.append(script.contents[0])

scrp = scripts_validos[1]
x = json.loads(scrp)
for element in x['itemListElement']:
    print(element['name'])

