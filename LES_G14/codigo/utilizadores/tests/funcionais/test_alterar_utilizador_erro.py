
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from django.urls import reverse
from notificacoes.tests.test_models import create_MensagemRecebida_0
from selenium.webdriver.support.wait import WebDriverWait
from utilizadores.models import Administrador
from utilizadores.tests.test_models import create_Administrador_0
from django.core.management import call_command
from django.contrib.auth.models import Group
from dia_aberto.utils import get_driver


class CriarParticipante(StaticLiveServerTestCase):
    """ Testes funcionais alterar utilizador - Erro """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = get_driver()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        call_command('create_groups')
        self.my_group = Group.objects.get(name='Administrador')
        self.administrador = create_Administrador_0()
        self.administrador.valido = "True"
        self.administrador.set_password('andre123456')
        self.administrador.save()
        self.my_group.user_set.add(self.administrador)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_criar_participante_ok(self):
        """ Testes funcionais alterar utilizador - Erro """
        self.driver.get('%s%s' % (self.live_server_url, reverse('home')))
        self.driver.find_element(
            By.CSS_SELECTOR, ".button > span:nth-child(2)").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(
            self.administrador.username)
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("andre123456")
        self.driver.find_element(By.CSS_SELECTOR, ".is-success > span").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".mdi-account-circle").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".is-disabled:nth-child(1) > strong").click()
        self.driver.find_element(By.ID, "id_contacto").click()
        self.driver.find_element(By.ID, "id_contacto").send_keys("967321393")
        self.driver.find_element(By.CSS_SELECTOR, ".is-success > span").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".message-body")
        assert len(elements) > 0
