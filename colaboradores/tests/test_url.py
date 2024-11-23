from django.test import Client, TestCase, TestCase
from colaboradores.models import *
from django.utils.datetime_safe import datetime
import pytz
from django.urls import reverse
from colaboradores.views import *



#Create your tests here.


def create_Campus_0():
    return Campus.objects.get_or_create(nome='Penha')[0]



def create_UO_0(campus):
    return Unidadeorganica.objects.get_or_create(
        nome = 'Faculdade de Ciencias e Tecnologias',
        sigla = 'FCT',
        campusid = campus
        )[0]



def create_Curso_0():
    return Curso.objects.get_or_create(
        nome="CC",
        sigla="Ciências da Comunicação",
        unidadeorganicaid=create_UO_0(create_Campus_0()),
        )[0]



def create_Departamento_0(uo):
    return Departamento.objects.get_or_create(
        nome = 'Departamento de Engenharia Informatica e Eletronica',
        sigla = 'DEEI',
        unidadeorganicaid = uo
    )[0]




def create_Colaborador_0():
    return Colaborador.objects.get_or_create(
        username="andre10",
        first_name="André",
        last_name="Barrocas",
        password="andre123456", 
        email="teste10@teste.pt",
        contacto="+351967321393",
        valido="False",
        curso=create_Curso_0(),
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))

    )[0]


class TestColaboradoresUrls(TestCase):
    """ Teste suite dos urls da app "colaboradores" """
    @classmethod
    def setUpTestData(cls):
        cls.colaborador = create_Colaborador_0()
      

    def setUp(self):
        self.client.force_login(self.colaborador)
    
    def test_url_consultar_tarefas(self):
        """ Testes do url "consultar-tarefas" """
        url = self.client.get(reverse('colaboradores:consultar-tarefas'))
        self.assertEquals(url.resolver_match.func.__name__, consultar_tarefas.as_view().__name__)
    
    def test_url_concluir_tarefa(self):    
        """ Testes do url "concluir-tarefa" """
        url = self.client.get(reverse('colaboradores:concluir-tarefa', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, concluir_tarefa)
    
    def test_url_iniciar_tarefa(self): 
        """ Testes do url "iniciar-tarefa" """   
        url = self.client.get(reverse('colaboradores:iniciar-tarefa', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, iniciar_tarefa)

    def test_url_cancelar_tarefa(self):
        """ Testes do url "cancelar-tarefa" """
        url = self.client.get(reverse('colaboradores:cancelar-tarefa', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, cancelar_tarefa)
    
    def test_url_rejeitar_cancelamento_tarefa(self):    
        """ Testes do url "rejeitar-cancelamento-tarefa" """
        url = self.client.get(reverse('colaboradores:rejeitar-cancelamento-tarefa', kwargs={'id_notificacao':1}))
        self.assertEquals(url.resolver_match.func, rejeitar_cancelamento_tarefa)
    
    def test_url_validar_cancelamento_tarefa(self): 
        """ Testes do url "validar-cancelamento-tarefa" """   
        url = self.client.get(reverse('colaboradores:validar-cancelamento-tarefa', kwargs={'id_notificacao':1}))
        self.assertEquals(url.resolver_match.func, validar_cancelamento_tarefa)
