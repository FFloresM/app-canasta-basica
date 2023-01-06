from django import forms

class ProductoForm(forms.Form):
    producto = forms.CharField(label='Producto', max_length=100)