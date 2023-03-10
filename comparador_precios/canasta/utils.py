def price2int(price):
    return int(price.replace('$','').replace('.','',3))