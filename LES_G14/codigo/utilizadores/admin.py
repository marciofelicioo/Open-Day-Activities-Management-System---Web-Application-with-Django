from django.contrib import admin
from .models import Utilizador,Administrador,Participante,ProfessorUniversitario,Coordenador,Colaborador
# Register your models here.
admin.site.register(Utilizador)

admin.site.register(Administrador)

admin.site.register(Participante)

admin.site.register(ProfessorUniversitario)

admin.site.register(Coordenador)

admin.site.register(Colaborador)