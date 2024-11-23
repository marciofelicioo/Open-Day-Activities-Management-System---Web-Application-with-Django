from django.test import Client, TestCase, TestCase
from notificacoes.models import *
from django.utils.datetime_safe import datetime
import pytz
from django.urls import reverse
from notificacoes.views import *



def create_Utilizador_0():
    return Utilizador.objects.get_or_create(
        username="andre0",
        first_name="André",
        last_name="Barrocas", 
        password="andre123456", 
        email="teste@teste.pt",
        contacto="+351967321393",
        valido="False"
    )[0]




class TestNotificacoesUrls(TestCase):
    """ Teste suite dos urls da app "notificacoes" """
    @classmethod
    def setUpTestData(cls):
        cls.utilizador = create_Utilizador_0()
      

    def setUp(self):
        self.client.force_login(self.utilizador)
    
    def test_url_sem_notificacoes(self):
        """ Testes do url "sem-notificacoes" """
        url = self.client.get(reverse('notificacoes:sem-notificacoes', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, sem_notificacoes)
    
    def test_url_categorias_notificacao_automatica(self):    
        """ Testes do url "categorias-notificacao-automatica" """
        url = self.client.get(reverse('notificacoes:categorias-notificacao-automatica', kwargs={'id':1,'nr':1}))
        self.assertEquals(url.resolver_match.func, categorias_notificacao_automatica)
    
    def test_url_apagar_notificacao_automatica(self): 
        """ Testes do url "apagar-notificacao-automatica" """   
        url = self.client.get(reverse('notificacoes:apagar-notificacao-automatica', kwargs={'id':1,'nr':1}))
        self.assertEquals(url.resolver_match.func, apagar_notificacao_automatica)

    def test_url_limpar_notificacoes(self):
        """ Testes do url "limpar-notificacoes" """
        url = self.client.get(reverse('notificacoes:limpar-notificacoes', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, limpar_notificacoes)
    
    def test_url_marcar_como_lida(self):    
        """ Testes do url "ler-notificacoes" """
        url = self.client.get(reverse('notificacoes:ler-notificacoes'))
        self.assertEquals(url.resolver_match.func, marcar_como_lida)
    
    def test_url_escolher_tipo(self): 
        """ Testes do url "enviar-notificacao" """   
        url = self.client.get(reverse('notificacoes:enviar-notificacao'))
        self.assertEquals(url.resolver_match.func, escolher_tipo)

    def test_url_criar_mensagem(self):
        """ Testes do url "escrever-mensagem" """
        url = self.client.get(reverse('notificacoes:escrever-mensagem', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, criar_mensagem)
    
    def test_url_criar_mensagem_uo(self):    
        """ Testes do url "criar-mensagem-uo" """
        url = self.client.get(reverse('notificacoes:criar-mensagem-uo', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, criar_mensagem_uo)
    
    def test_url_criar_mensagem_admin(self): 
        """ Testes do url "criar-mensagem-admin" """   
        url = self.client.get(reverse('notificacoes:criar-mensagem-admin', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, criar_mensagem_admin)

    def test_url_criar_mensagem_participante(self):
        """ Testes do url "criar-mensagem-participante" """
        url = self.client.get(reverse('notificacoes:criar-mensagem-participante', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, criar_mensagem_participante)
    
    def test_url_sem_mensagens(self):    
        """ Testes do url "sem-mensagens" """
        url = self.client.get(reverse('notificacoes:sem-mensagens', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, sem_mensagens)
    
    def test_url_concluir_envio(self): 
        """ Testes do url "concluir-envio" """   
        url = self.client.get(reverse('notificacoes:concluir-envio'))
        self.assertEquals(url.resolver_match.func, concluir_envio)


    def test_url_detalhes_mensagens(self):
        """ Testes do url "detalhes-mensagem" """
        url = self.client.get(reverse('notificacoes:detalhes-mensagem', kwargs={'id':1,'nr':1}))
        self.assertEquals(url.resolver_match.func, detalhes_mensagens)
    
    def test_url_apagar_mensagem(self):    
        """ Testes do url "apagar-mensagem" """
        url = self.client.get(reverse('notificacoes:apagar-mensagem', kwargs={'id':1,'nr':1}))
        self.assertEquals(url.resolver_match.func, apagar_mensagem)
    
    def test_url_limpar_mensagens(self): 
        """ Testes do url "limpar-mensagens" """   
        url = self.client.get(reverse('notificacoes:limpar-mensagens', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, limpar_mensagens)

    def test_url_mensagem_como_lida(self):
        """ Testes do url "ler-mensagens" """
        url = self.client.get(reverse('notificacoes:ler-mensagens', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, mensagem_como_lida)
