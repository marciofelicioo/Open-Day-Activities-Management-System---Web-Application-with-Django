from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from django.urls import reverse
from utilizadores.models import Participante
from utilizadores.tests.test_models import create_Participante_0
from notificacoes.tests.test_models import create_MensagemRecebida_0
from selenium.webdriver.support.wait import WebDriverWait
from dia_aberto.utils import get_driver


class AlterarPassTestOk(StaticLiveServerTestCase):
    """ Testes funcionais alterar password - Sucesso """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = get_driver()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        self.participante = create_Participante_0()
        self.participante.set_password('andre123456')
        self.participante.save()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_alterarPass(self):
        """ Testes funcionais alterar password - Sucesso """
        self.driver.get('%s%s' % (self.live_server_url, reverse('home')))
        self.driver.find_element(By.CSS_SELECTOR, ".icon").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(
            self.participante.username)
        self.driver.find_element(By.ID, "id_password").click()
        self.driver.find_element(By.ID, "id_password").send_keys("andre123456")
        self.driver.find_element(By.CSS_SELECTOR, ".is-outlined").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".mdi-account-circle").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".dropdown-item:nth-child(2) > strong").click()
        self.driver.find_element(By.ID, "id_old_password").click()
        self.driver.find_element(
            By.ID, "id_old_password").send_keys("andre123456")
        self.driver.find_element(By.ID, "id_new_password1").click()
        self.driver.find_element(
            By.ID, "id_new_password1").send_keys("andre1234567")
        self.driver.find_element(By.ID, "id_new_password2").click()
        self.driver.find_element(
            By.ID, "id_new_password2").send_keys("andre1234567")
        self.driver.find_element(
            By.ID, "id_new_password2").send_keys(Keys.ENTER)
        assert self.driver.find_element(
            By.CSS_SELECTOR, ".message-body strong").text == "Senha alterada com sucesso!"
