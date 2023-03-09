from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    format = models.CharField(max_length=30)
    measurementUnit = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return f'{self.name} {self.brand} {self.format}'
    
class Supermarket(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name
    
class Sells(models.Model):
    unitPrice = models.IntegerField(null=False)
    detailURL = models.URLField(default='')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        return f"{self.item} {self.supermarket} {self.unitPrice}"


