import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Cliente, Coche, Servicio, CocheServicio

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'app_gestion_coches/lista_clientes.html', {'clientes': clientes})


def lista_coches(request):
    """EXTRA: Lista todos los coches registrados en el taller."""
    coches = Coche.objects.select_related('cliente').all()
    return render(request, 'app_gestion_coches/lista_coches.html', {'coches': coches})

@csrf_exempt
def registrar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nombre=data['nombre'],
                telefono=data['telefono'],
                email=data['email']
            )
            return JsonResponse({"mensaje": "Cliente registrado con exito", "cliente_id": cliente.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)

@csrf_exempt
def registrar_coche(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(id=data['cliente_id'])
            coche = Coche.objects.create(
                cliente=cliente,
                marca=data['marca'],
                modelo=data['modelo'],
                matricula=data['matricula']
            )
            return JsonResponse({"mensaje": "Coche registrado con exito", "coche_id": coche.id})
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)

@csrf_exempt
def registrar_servicio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            coche = Coche.objects.get(id=data['coche_id'])
            servicio = Servicio.objects.create(
                nombre=data['nombre'],
                descripcion=data['descripcion']
            )
            CocheServicio.objects.create(coche=coche, servicio=servicio)
            return JsonResponse({"mensaje": "Servicio registrado con exito", "servicio_id": servicio.id})
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Metodo no permitido"}, status=405)

@csrf_exempt
def buscar_cliente_por_email(request, email):
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(email=email)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)

@csrf_exempt
def buscar_coches_por_marca(request, marca):
    coches = list(Coche.objects.filter(marca__iexact=marca).values("id", "marca", "modelo", "matricula", "cliente_id"))
    return JsonResponse(coches, safe=False)

def listar_servicios_taller(request):
    """EXTRA: Muestra todos los servicios disponibles en el taller con cuántas veces se han realizado."""
    servicios = Servicio.objects.all()
    return render(request, 'app_gestion_coches/lista_servicios.html', {'servicios': servicios})

def detalle_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        coches = Coche.objects.filter(cliente=cliente)
        contexto = {
            'cliente': cliente,
            'coches': coches,
        }
        return render(request, 'app_gestion_coches/detalle_cliente.html', contexto)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)


def detalle_coche(request, coche_id):
    """EXTRA: Muestra el detalle de un coche con su propietario y el historial de servicios."""
    try:
        coche = Coche.objects.select_related('cliente').get(id=coche_id)
        coche_servicios = CocheServicio.objects.filter(coche=coche).select_related('servicio')
        contexto = {
            'coche': coche,
            'coche_servicios': coche_servicios,
        }
        return render(request, 'app_gestion_coches/detalle_coche.html', contexto)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)

@csrf_exempt
def buscar_coche_por_matricula(request, matricula):
    try:
        coche = Coche.objects.select_related('cliente').get(matricula=matricula)
        respuesta = {
            "coche": {
                "id": coche.id,
                "marca": coche.marca,
                "modelo": coche.modelo,
                "matricula": coche.matricula,
            },
            "cliente": {
                "id": coche.cliente.id,
                "nombre": coche.cliente.nombre,
                "telefono": coche.cliente.telefono,
                "email": coche.cliente.email,
            }
        }
        return JsonResponse(respuesta)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)

@csrf_exempt
def buscar_coches_de_cliente(request, cliente_id):
    try:
        if not Cliente.objects.filter(id=cliente_id).exists():
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        coches = list(Coche.objects.filter(cliente_id=cliente_id).values("id", "marca", "modelo", "matricula"))
        return JsonResponse(coches, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def buscar_servicios_de_coche(request, coche_id):
    try:
        coche = Coche.objects.select_related('cliente').get(id=coche_id)
        coche_servicios = CocheServicio.objects.filter(coche=coche).select_related('servicio')
        contexto = {
            'coche': coche,
            'coche_servicios': coche_servicios,
        }
        return render(request, 'app_gestion_coches/servicios_coche.html', contexto)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)