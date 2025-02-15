from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Producto, Categoria, Cliente, Compra, DetalleCompra
from .forms import CompraForm, ClienteForm, ProductoForm

def home(request, categoria_id=None):
    if categoria_id:
        productos = Producto.objects.filter(categoria_id=categoria_id)
    else:
        productos = Producto.objects.all()
    
    categorias = Categoria.objects.all()  # Categorías para la barra de navegación

    return render(request, "tienda_app/home.html", {
        "productos": productos,
        "categorias": categorias,
    })
    
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:  
            login(request, user)
            return redirect("home")  # Ahora redirige a home en vez del admin
        else:
            return render(request, "tienda_app/login.html", {"error": "Usuario o contraseña incorrectos"})

    return render(request, "tienda_app/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductoForm()
    return render(request, 'tienda_app/agregar_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    if not request.user.is_superuser:
        return redirect("home")  # Evitar acceso no autorizado
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == "POST":
        producto.nombre = request.POST.get("nombre", producto.nombre)
        producto.descripcion = request.POST.get("descripcion", producto.descripcion)
        producto.precio = request.POST.get("precio", producto.precio)
        producto.save()
        return redirect("home")

    return render(request, "tienda_app/editar_producto.html", {"producto": producto})

@login_required
def eliminar_producto(request, producto_id):
    if request.user.is_superuser:
        producto = get_object_or_404(Producto, id=producto_id)
        producto.delete()
    return redirect("home")

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'tienda_app/cliente.html', {'clientes': clientes})

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'tienda_app/editar_cliente.html', {'form': form})

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'tienda_app/eliminar_cliente.html', {'cliente': cliente})

@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'tienda_app/agregar_cliente.html', {'form': form})

# Vista para agregar compra
def agregar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save()  # Guarda la compra (sin productos aún)

            # Obtenemos los productos seleccionados
            productos_seleccionados = request.POST.getlist('productos')  # Recoge los productos seleccionados

            # Creamos los detalles de la compra
            total_compra = 0
            for producto_id in productos_seleccionados:
                producto = Producto.objects.get(id=producto_id)
                cantidad = int(request.POST.get(f'cantidad_{producto_id}', 1))  # Obtener la cantidad ingresada
                subtotal = producto.precio * cantidad
                DetalleCompra.objects.create(compra=compra, producto=producto, cantidad=cantidad, subtotal=subtotal)
                total_compra += subtotal  # Acumulamos el total

            compra.total = total_compra  # Guardamos el total calculado en la compra
            compra.save()  # Guardamos la compra con su total calculado

            return redirect('ver_compras')  # Redirige a la vista de compras
    else:
        form = CompraForm()
        productos = Producto.objects.all()  # Obtenemos todos los productos disponibles

    return render(request, 'tienda_app/agregar_compra.html', {'form': form, 'productos': productos})

def ver_compras(request):
    compras = Compra.objects.all()
    return render(request, "tienda_app/compras.html", {
        "compras": compras,
    })

@login_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    detalles = DetalleCompra.objects.filter(compra=compra)
    return render(request, 'tienda_app/detalle_compra.html', {'compra': compra, 'detalles': detalles})