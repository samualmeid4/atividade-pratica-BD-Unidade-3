from django.contrib import admin
from .models import Atleta, Treinador, Organizador

admin.site.register(Atleta)
admin.site.register(Treinador)
admin.site.register(Organizador)