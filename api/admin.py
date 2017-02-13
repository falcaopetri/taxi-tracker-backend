from django.contrib import admin

from .models import * 

# Register your models here.
admin.site.register(Motorista)
admin.site.register(Veiculo)
admin.site.register(Corrida)
admin.site.register(Passageiro)
admin.site.register(Uso)

