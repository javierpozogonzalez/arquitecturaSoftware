from django.contrib import admin
from .models import Cliente, Coche, Servicio, CocheServicio

admin.site.register(Cliente)
admin.site.register(Coche)
admin.site.register(Servicio)
admin.site.register(CocheServicio)