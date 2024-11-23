from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import resolve,reverse
from coordenadores import views

#Create your tests here.
class TestUrls(TestCase):
    
    def test_url_is_resolved(self):
        url = reverse('coordenadores:adicionarTarefa')
        self.assertEquals(resolve(url).func, views.adicionartarefa)

        url = reverse('coordenadores:alterarTarefa', kwargs={'id':1})
        self.assertEquals(resolve(url).func, views.adicionartarefa)

        url = reverse('coordenadores:consultarTarefa')
        self.assertEquals(resolve(url).func.__name__, views.ConsultarTarefas.__name__)

        url = reverse('coordenadores:sessoesAtividade')
        self.assertEquals(resolve(url).func, views.sessoesAtividade)

        url = reverse('coordenadores:diasAtividade')
        self.assertEquals(resolve(url).func, views.diasAtividade)

        url = reverse('coordenadores:colaboradores')
        self.assertEquals(resolve(url).func, views.colaboradores)
        
        url = reverse('coordenadores:tipoTarefa')
        self.assertEquals(resolve(url).func, views.tipoTarefa)

        url = reverse('coordenadores:grupoInfo')
        self.assertEquals(resolve(url).func, views.grupoInfo)

        url = reverse('coordenadores:diasGrupo')
        self.assertEquals(resolve(url).func, views.diasGrupo)

        url = reverse('coordenadores:horarioGrupo')
        self.assertEquals(resolve(url).func, views.horarioGrupo)

        url = reverse('coordenadores:locaisOrigem')
        self.assertEquals(resolve(url).func, views.locaisOrigem)

        url = reverse('coordenadores:locaisDestino')
        self.assertEquals(resolve(url).func, views.locaisDestino)

        url = reverse('coordenadores:eliminarTarefa', kwargs={'id':1})
        self.assertEquals(resolve(url).func, views.eliminartarefa)

        url = reverse('coordenadores:atribuirColaborador', kwargs={'id':1})
        self.assertEquals(resolve(url).func, views.atribuirColaborador)
