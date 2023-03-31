from django.db import models
from django.utils import timezone

class Brand(models.Model):
    brand_name = models.CharField(max_length=30)

    def __str__(self):
        return self.brand_name
    

class Product(models.Model):
    name = models.CharField(max_length=40)
    format = models.CharField(max_length=40)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    measurementUnit = models.CharField(max_length=30)
    #agregar campo sabor
    
    def __str__(self) -> str:
        return f'{self.name} {self.brand} {self.format}'



class Supermarket(models.Model):
    name = models.CharField(max_length=30)
    #guardar posición GPS

    def __str__(self) -> str:
        return self.name
    
class Sell(models.Model):
    unitPrice = models.IntegerField(null=False)
    detailURL = models.URLField(default='')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    last_update = models.DateTimeField('fecha ultima busqueda', default=timezone.now)

    def __str__(self) -> str:
        return f"{self.item} {self.supermarket} ${self.unitPrice} {self.last_update.strftime('%d-%b-%Y %H:%M')}"


