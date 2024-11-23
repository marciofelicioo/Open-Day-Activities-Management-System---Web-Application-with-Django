import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

GROUPS = ['Coordenador', 'Participante', 'ProfessorUniversitario', 'Administrador', 'Colaborador']

class Command(BaseCommand):
    help = 'Cria os grupos'

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
        
        self.stdout.write(self.style.SUCCESS('Grupos criados com sucesso'))
