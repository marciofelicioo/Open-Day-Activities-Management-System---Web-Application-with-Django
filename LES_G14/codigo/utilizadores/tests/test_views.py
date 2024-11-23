from django.test import TestCase
from utilizadores.models import *
from configuracao.models import *
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from utilizadores.tests.test_models import *

class GroupTests(TestCase):
    ''' Testes para a criação de grupos de utilizadores '''
    def setUp(self):
        call_command('create_groups')



    def test_admin(self):
        ''' Testes grupo de administradores '''
        g = Group.objects.get(name='Administrador')
        self.assertEqual(str(g), 'Administrador')

    
    def test_coord(self):
        ''' Testes grupo de coordenadores '''
        g = Group.objects.get(name='Coordenador')
        self.assertEqual(str(g), 'Coordenador')    


    def test_colab(self):
        ''' Testes grupo de colaboradores '''
        g = Group.objects.get(name='Colaborador')
        self.assertEqual(str(g), 'Colaborador')        


    def test_participamte(self):
        ''' Testes grupo de participante '''
        g = Group.objects.get(name='Participante')
        self.assertEqual(str(g), 'Participante')           

    def test_prof_universitario(self):
        ''' Testes grupo de coordenadores '''
        g = Group.objects.get(name='ProfessorUniversitario')
        self.assertEqual(str(g), 'ProfessorUniversitario')                


