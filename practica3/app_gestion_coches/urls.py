from django.urls import path
from .views import (
    lista_clientes, registrar_cliente, registrar_coche, registrar_servicio,
    buscar_cliente_por_email, buscar_coches_por_marca, listar_servicios_taller,
    detalle_cliente, buscar_coche_por_matricula, buscar_coches_de_cliente,
    buscar_servicios_de_coche, lista_coches, detalle_coche,
    nuevo_usuario, nuevo_coche, nuevo_servicio
)

urlpatterns = [
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),
    path('coches/<int:coche_id>/servicios/', buscar_servicios_de_coche, name='buscar_servicios_de_coche'),

    path('coches/', lista_coches, name='lista_coches'),
    path('coches/<int:coche_id>/', detalle_coche, name='detalle_coche'),
    path('servicios/', listar_servicios_taller, name='listar_servicios_taller'),
    path('usuarios/nuevo/', nuevo_usuario, name='nuevo_usuario'),
    path('coches/nuevo/', nuevo_coche, name='nuevo_coche'),
    path('servicios/nuevo/', nuevo_servicio, name='nuevo_servicio'),

    path('clientes/registrar/', registrar_cliente, name='registrar_cliente'),
    path('coches/registrar/', registrar_coche, name='registrar_coche'),
    path('servicios/registrar/', registrar_servicio, name='registrar_servicio'),

    path('clientes/email/<str:email>/', buscar_cliente_por_email, name='buscar_cliente_por_email'),
    path('coches/marca/<str:marca>/', buscar_coches_por_marca, name='buscar_coches_por_marca'),

    path('coches/matricula/<str:matricula>/', buscar_coche_por_matricula, name='buscar_coche_por_matricula'),
    path('clientes/<int:cliente_id>/coches/', buscar_coches_de_cliente, name='buscar_coches_de_cliente'),
]