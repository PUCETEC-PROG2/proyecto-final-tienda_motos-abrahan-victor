from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    destacado = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")

    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Solo auto_now_add=True

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)  # Campo no editable
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra {self.id} - {self.cliente.nombre}"

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
