from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from atividades import views

#Create your tests here.
class TestUrls(SimpleTestCase):

    def test_url_is_resolved(self):
        url = reverse('atividades:minhasAtividades')
        self.assertEquals(resolve(url).func.__name__, views.AtividadesProfessor.__name__)
        url = reverse('atividades:atividadesUOrganica')
        self.assertEquals(resolve(url).func.__name__, views.AtividadesCoordenador.__name__)
        url = reverse('atividades:alterarAtividade', kwargs={'id':1})
        self.assertEquals(resolve(url).func, views.alterarAtividade) 
        url = reverse('atividades:inserirSessao', kwargs={'id':1})
        self.assertEquals(resolve(url).func, views.inserirsessao) 
        url = reverse('atividades:eliminarAtividade', kwargs={'id':1})
        self.assertEquals(resolve(url).func, views.eliminarAtividade) 
        url = reverse('atividades:eliminarSessao', kwargs={'id':1})
        self.assertEquals(resolve(url).func, views.eliminarSessao)
        url = reverse('atividades:proporAtividade')
        self.assertEquals(resolve(url).func, views.proporatividade) 
        url = reverse('atividades:validarAtividade', kwargs={'id':1,'action':1})
        self.assertEquals(resolve(url).func, views.validaratividade) 
        url = reverse('atividades:verEdificios')
        self.assertEquals(resolve(url).func, views.veredificios) 
        url = reverse('atividades:verSalas')
        self.assertEquals(resolve(url).func, views.versalas) 
        url = reverse('atividades:verHorarios')
        self.assertEquals(resolve(url).func, views.verhorarios) 
        url = reverse('atividades:verResumo', kwargs={'id':1})
        self.assertEquals(resolve(url).func, views.verresumo) 
        url = reverse('atividades:confirmarResumo', kwargs={'id':1})
        self.assertEquals(resolve(url).func, views.confirmarResumo)
        