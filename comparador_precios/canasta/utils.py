import re

def price2int(price):
    price = re.search('\$[0-9.]+', price).group()
    return int(price.replace('$','').replace('.','',3))

class Producto:
    def __init__(self) -> None:
        self.nombre: str = ""
        self.marca: str = ""
        self.unidadMedida: str = ""
        self.precio: int = 0
        self.listaPrecios: list = []
        self.url: str = "" 

    def setNombre(self, nombre: str) -> None:
        self.nombre = nombre

    def setMarca(self, marca: str) -> None:
        self.marca = marca if marca != "" else ""

    def setUnidadMedida(self, unidadMEdida: str) -> None:
        self.unidadMedida = unidadMEdida

    def setPrecio(self, precio: int) -> None:
        self.precio = precio

    def setListaPrecios(self, listaPrecios: list) -> None:
        if len(listaPrecios) > 0:
            self.listaPrecios = listaPrecios
            if '(Normal)' in listaPrecios: #para jumbo y santa
                self.setPrecio(price2int(listaPrecios[listaPrecios.index('(Normal)') - 1]))
            else:
                self.setPrecio(price2int(listaPrecios[0]))

    def setURL(self, url: str) -> str:
        self.url = url

    def getNombre(self) -> str:
        return self.nombre
    
    def getMarca(self) -> str:
        return self.marca
    
    def getUnidadMedida(self) -> str:
        return self.unidadMedida
    
    def getPrecio(self) -> int:
        return self.precio
    
    def getListaPrecios(self) -> list:
        return self.listaPrecios

    def getURL(self) -> str:
        return self.url    
    
    def __str__(self) -> str:
        return f"Nombre: {self.getNombre()}, Marca: {self.getMarca()}, Unidad: {self.getUnidadMedida()}, Precio: {self.getPrecio()}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Producto):
            return NotImplemented
        return (self.getNombre(), self.getMarca()) == (other.getNombre(), other.getMarca())