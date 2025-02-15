from django.urls import path
from .views import home, login_view, logout_view, editar_producto, eliminar_producto, listar_clientes, editar_cliente, eliminar_cliente, agregar_compra, ver_compras, detalle_compra, agregar_cliente, agregar_producto
from . import views

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("editar_producto/<int:producto_id>/", editar_producto, name="editar_producto"),
    path('agregar/', agregar_producto, name='agregar_producto'),
    path("eliminar_producto/<int:producto_id>/", eliminar_producto, name="eliminar_producto"),
    path("categoria/<int:categoria_id>/", home, name="filtrar_categoria"),
    path("clientes/", listar_clientes, name="listar_clientes"),
    path("clientes/editar/<int:cliente_id>/", editar_cliente, name="editar_cliente"),
    path("clientes/eliminar/<int:cliente_id>/", eliminar_cliente, name="eliminar_cliente"),
    path("clientes/agregar/", agregar_cliente, name="agregar_cliente"),
    path("agregar_compra/", agregar_compra, name="agregar_compra"),
    path('compras/', ver_compras, name='ver_compras'),
    path('compras/detalle/<int:compra_id>/', detalle_compra, name='detalle_compra'),
]