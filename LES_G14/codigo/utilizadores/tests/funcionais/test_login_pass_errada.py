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


class LoginTestPassErrada(StaticLiveServerTestCase):
    """ Testes funcionais do login - Password errada """

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

    def test_login_passErrada(self):
        """ Teste funcional de login password errada """
        self.driver.get('%s%s' % (self.live_server_url, reverse('home')))
        self.driver.find_element(
            By.CSS_SELECTOR, ".button > span:nth-child(2)").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys(
            self.participante.username)
        self.driver.find_element(
            By.ID, "id_password").send_keys("andre1234567")
        self.driver.find_element(
            By.ID, "id_password").send_keys(Keys.ENTER)
        assert self.driver.find_element(
            By.CSS_SELECTOR, ".message-body > p").text == "O nome de utilizador ou a palavra-passe inválidos!"
