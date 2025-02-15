from django import forms
from .models import Producto, Cliente, Compra

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'destacado', 'categoria']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email']

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['cliente', 'total']