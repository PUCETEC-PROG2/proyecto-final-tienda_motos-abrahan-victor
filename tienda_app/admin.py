from django.contrib import admin
from .models import Producto, Categoria, Cliente, Compra, DetalleCompra

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Compra)
admin.site.register(DetalleCompra)
