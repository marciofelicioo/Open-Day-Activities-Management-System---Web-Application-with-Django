from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from django.urls import reverse
from utilizadores.models import Colaborador
from utilizadores.tests.test_models import create_Colaborador_0
from notificacoes.tests.test_models import create_MensagemRecebida_0
from selenium.webdriver.support.wait import WebDriverWait
from django.core.management import call_command
from django.contrib.auth.models import Group
from dia_aberto.utils import get_driver


class TestConsultarTarefas(StaticLiveServerTestCase):
    """ Testes funcionais consultar tarefas de um colaborador - Sucesso """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = get_driver()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        call_command('create_groups')
        self.my_group = Group.objects.get(name='Colaborador')
        self.colaborador = create_Colaborador_0()
        self.colaborador.set_password('andre123456')
        self.colaborador.valido = "True"
        self.colaborador.save()
        self.my_group.user_set.add(self.colaborador)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_login_ok(self):
        """ Teste funcional consultar tarefas de um colaborador - sucesso """
        self.driver.get('%s%s' % (self.live_server_url, reverse('home')))
        self.driver.find_element(
            By.CSS_SELECTOR, ".button > span:nth-child(2)").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(
            self.colaborador.username)
        self.driver.find_element(By.ID, "id_password").send_keys("andre123456")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        assert self.driver.find_element(
            By.CSS_SELECTOR, ".message-body strong").text == f"Bem vindo(a) {self.colaborador.first_name}"
        self.driver.find_element(
            By.CSS_SELECTOR, "a:nth-child(1) > .button").click()
        self.driver.find_element(By.LINK_TEXT, "Minhas Tarefas").click()
        self.driver.find_element(By.CSS_SELECTOR, ".menu-label").click()
