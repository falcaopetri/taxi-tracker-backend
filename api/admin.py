from django.contrib import admin

from .models import Motorista, Cooperativa, Veiculo

# Register your models here.
admin.site.register(Motorista)
admin.site.register(Cooperativa)
admin.site.register(Veiculo)
