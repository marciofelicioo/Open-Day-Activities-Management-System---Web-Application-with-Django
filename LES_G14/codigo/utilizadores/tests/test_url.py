from django.test import Client, TestCase, TestCase
from utilizadores.models import *
from django.utils.datetime_safe import datetime
import pytz
from django.urls import reverse
from utilizadores.views import *



#Create your tests here.


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



class TestUrlsConsultarUntilizadores(TestCase):
    """ Teste suite dos urls da app "utilizadores" - Caso de uso consultar utilizadores """

    @classmethod
    def setUpTestData(cls):
        cls.utilizador = create_Utilizador_0()

    def setUp(self):
        self.client.force_login(self.utilizador)
    
    
    def test_url_consultar_utilizadores(self):
        """ Testes do url "consultar-utilizadores" """
        url = self.client.get(reverse('utilizadores:consultar-utilizadores'))
        self.assertEquals(url.resolver_match.func.__name__, consultar_utilizadores.as_view().__name__)
        

class TestCriarUtilizadoresUrls(TestCase):
    """ Teste suite dos urls da app "utilizadores" - Caso de uso criar utilizador """
    @classmethod
    def setUpTestData(cls):
        cls.utilizador = create_Utilizador_0()
      

    def setUp(self):
        self.client.force_login(self.utilizador)
    
    def test_url_escolher_perfil(self):
        """ Testes do url "escolher-perfil" """
        url = self.client.get(reverse('utilizadores:escolher-perfil'))
        self.assertEquals(url.resolver_match.func, escolher_perfil)
    
    def test_url_criar_utilizador(self):    
        """ Testes do url "criar-utilizador" """
        url = self.client.get(reverse('utilizadores:criar-utilizador', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, criar_utilizador)
    
    def test_url_concluir_registo(self): 
        """ Testes do url "concluir-registo" """   
        url = self.client.get(reverse('utilizadores:concluir-registo', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, concluir_registo)


class TestAlterarPasswordUrls(TestCase):
    """ Teste suite dos urls da app "utilizadores" - Caso de uso alterar password """
    @classmethod
    def setUpTestData(cls):
        cls.utilizador = create_Utilizador_0()

                    

    def setUp(self):
        self.client.force_login(self.utilizador)
    
    def test_url_alterar_password(self):
        """ Testes do url "alterar-password" """
        url = self.client.get(reverse('utilizadores:alterar-password'))
        self.assertEquals(url.resolver_match.func, alterar_password)
        


class TestApagarUtilizadorUrls(TestCase):
    """ Teste suite dos urls da app "utilizadores" - Caso de uso apagar conta e apagar utilizador """
    @classmethod
    def setUpTestData(cls):
        cls.utilizador = create_Utilizador_0()

       

    def setUp(self):
        self.client.force_login(self.utilizador)

    def test_url_apagar_conta(self):
        """ Testes do url "apagar-conta" """
        url = self.client.get(reverse('utilizadores:apagar-conta'))
        self.assertEquals(url.resolver_match.func, apagar_proprio_utilizador)
    
    
    def test_url_apagar_utilizador(self):    
        """ Testes do url "apagar-utilizador" """
        url = self.client.get(reverse('utilizadores:apagar-utilizador', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, apagar_utilizador)
        



class TestValidarRejeitarUrls(TestCase):
    """ Teste suite dos urls da app "utilizadores" - Validar e rejeitar utilizadores """
    @classmethod
    def setUpTestData(cls):
        cls.utilizador = create_Utilizador_0()


    def setUp(self):
        self.client.force_login(self.utilizador)

    def test_url_validar(self):
        """ Testes do url "validar-utilizador" """
        url = self.client.get(reverse('utilizadores:validar-utilizador',kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, validar_utilizador)
    
    def test_url_validar(self):    
        """ Testes do url "rejeitar-utilizador" """
        url = self.client.get(reverse('utilizadores:rejeitar-utilizador',kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, rejeitar_utilizador)


class TestMensagensUrls(TestCase):

    """ Teste suite dos urls da app "utilizadores" - Mensagens """
    @classmethod
    def setUpTestData(cls):
        cls.utilizador = create_Utilizador_0()



    def setUp(self):
        self.client.force_login(self.utilizador)

    def test_url_resolved(self):
        """ Testes do url "mensagem" """
        url = self.client.get(reverse('utilizadores:mensagem', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, mensagem)


    def test_url_resolved(self):
        """ Testes do url "validar" """
        url = self.client.get(reverse('utilizadores:validar', kwargs={'nome':"andre",'id':1}))
        self.assertEquals(url.resolver_match.func, enviar_email_validar)

    def test_url_resolved(self):
        """ Testes do url "rejeitar" """
        url = self.client.get(reverse('utilizadores:rejeitar', kwargs={'nome':"andre",'id':1}))
        self.assertEquals(url.resolver_match.func, enviar_email_rejeitar)






class TestAlterarPerfilUrls(TestCase):
    
    """ Teste suite dos urls da app "utilizadores" - Caso de uso alterar perfil de utilizadores """
    @classmethod
    def setUpTestData(cls):
        cls.utilizador = create_Utilizador_0()
         

    def setUp(self):
        self.client.force_login(self.utilizador)




    def test_url_alterar_utilizador_admin(self):
        """ Testes do url "rejeitar-utilizador" """
        url = self.client.get(reverse('utilizadores:alterar-utilizador-admin', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, alterar_utilizador_admin)
    
    def test_url_alterar_utilizador(self):  
        """ Testes do url "alterar-utilizador" """
        url = self.client.get(reverse('utilizadores:alterar-utilizador'))
        self.assertEquals(url.resolver_match.func, alterar_utilizador)

    def test_url_alterar_perfil_escolha(self): 
        """ Testes do url "mudar-perfil-escolha-admin" """
        url = self.client.get(reverse('utilizadores:mudar-perfil-escolha-admin', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, mudar_perfil_escolha_admin)

    def test_url_alterar_perfil_admin(self): 
        """ Testes do url "mudar-perfil-admin" """
        url = self.client.get(reverse('utilizadores:mudar-perfil-admin', kwargs={'tipo':1,'id':1}))
        self.assertEquals(url.resolver_match.func, mudar_perfil_admin)

    def test_url_alterar_perfil_escolha(self): 
        """ Testes do url "mudar-perfil-escolha" """
        url = self.client.get(reverse('utilizadores:mudar-perfil-escolha', kwargs={'id':1}))
        self.assertEquals(url.resolver_match.func, mudar_perfil_escolha)

    def test_url_alterar_perfil_escolha(self): 
        """ Testes do url "mudar-perfil" """
        url = self.client.get(reverse('utilizadores:mudar-perfil', kwargs={'tipo':1}))
        self.assertEquals(url.resolver_match.func, mudar_perfil)





class TestLoginUrls(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.utilizador = create_Utilizador_0()
         

    def setUp(self):
        self.client.force_login(self.utilizador)


    def test_url_login(self):
        """ Testes do url "login" """
        response = self.client.get(reverse('utilizadores:login'))
        self.assertEqual(response.resolver_match.func, login_action)

    def test_url_logout(self):
        """ Testes do url "logout" de nome inscricao-pdf """
        response = self.client.get(
            reverse('utilizadores:logout'))
        self.assertEqual(response.resolver_match.func, logout_action)
