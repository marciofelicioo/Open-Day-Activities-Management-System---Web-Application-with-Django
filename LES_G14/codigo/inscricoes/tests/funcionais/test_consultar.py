from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from django.urls import reverse
from utilizadores.models import Participante, ProfessorUniversitario
from configuracao.models import Campus, Unidadeorganica, Departamento
from django.contrib.auth.models import Group
from django.core.management import call_command
from inscricoes.models import Inscricao, Escola, Responsavel
import datetime
from utilizadores.tests.test_models import create_Participante_0
from atividades.models import Atividade, Tema
from inscricoes.tests.samples import create_Diaaberto_0, create_Espaco_0, create_Sessao_0, create_Sessao_1, create_Sessao_2, create_Transporte_0, create_Transportehorario_0, create_Horario_0, create_Horario_1, create_Horario_2
from notificacoes.tests.test_models import create_MensagemRecebida_0
from selenium.webdriver.support.wait import WebDriverWait
from seleniumlogin import force_login
from dia_aberto.utils import get_driver


def create_Inscricao_1():
    return Inscricao.objects.get_or_create(
        individual=True,
        nalunos=12,
        escola=create_Escola_1(),
        participante=create_Participante_Rafael(),
        dia=datetime.date(2020, 8, 24),
        diaaberto=create_Diaaberto_0(),
        meio_transporte='autocarro',
        hora_chegada=datetime.time(8, 40, 0),
        local_chegada="Terminal Rodoviário de Faro",
        entrecampi=True,
    )[0]


def create_Escola_1():
    return Escola.objects.get_or_create(
        nome="Escola Básica e Secundária do Cadaval",
        local="Cadaval",
    )[0]


def create_ProfessorUniversitario_0():
    return ProfessorUniversitario.objects.get_or_create(
        username="professor",
        first_name="José",
        last_name="Mário",
        password="andre123456",
        email="jose@jose.com",
        contacto="+351910897456",
        valido="True",
        gabinete="1.69",
        faculdade=create_UO_0(create_Campus_0()),
        departamento=create_Departamento_0(create_UO_0(create_Campus_0()))
    )[0]


def create_Participante_Rafael():
    return Participante.objects.get_or_create(
        username="participante",
        first_name="Rafael",
        last_name="Duarte",
        password="andre123456",
        email="rafael@rafael.com",
        contacto="+351910777888",
        valido="True"
    )[0]


def create_Responsavel_0():
    return Responsavel.objects.get_or_create(
        inscricao=create_Inscricao_1(),
        nome="Rafael Duarte",
        email="rafael@rafael.com",
        tel="+351910777888",
    )[0]


def create_Departamento_0(uo):
    return Departamento.objects.get_or_create(
        nome='Departamento de Engenharia Informatica e Eletronica',
        sigla='DEEI',
        unidadeorganicaid=uo
    )[0]


def create_Campus_0():
    return Campus.objects.get_or_create(nome='Gambelas')[0]


def create_UO_0(campus):
    return Unidadeorganica.objects.get_or_create(
        nome='Faculdade de Ciencias e Tecnologias',
        sigla='FCT',
        campusid=campus
    )[0]


def create_Tema_0():
    return Tema.objects.get_or_create(tema="Informatica")[0]


def create_Atividade_0():
    return Atividade.objects.get_or_create(
        nome="Java",
        descricao="Aprendendo Java",
        publicoalvo="Ciencias e Tecnologia",
        nrcolaboradoresnecessario=0,
        tipo='Palestra',
        estado='Aceite',
        professoruniversitarioutilizadorid=create_ProfessorUniversitario_0(),
        duracaoesperada=30,
        participantesmaximo=30,
        diaabertoid=create_Diaaberto_0(),
        espacoid=create_Espaco_0(),
        tema=create_Tema_0(),
    )[0]


class ConsultarInscricaoTest(StaticLiveServerTestCase):
    """ Testes funcionais do consultar inscrição """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command("create_groups")
        cls.driver = get_driver()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        self.inscricao = create_Inscricao_1()
        self.inscricao.save()
        self.atividade = create_Atividade_0()
        self.atividade.save()
        self.responsavel = create_Responsavel_0()
        self.responsavel.save()
        group = Group.objects.get(name='Participante')
        group.user_set.add(self.inscricao.participante)
        force_login(self.inscricao.participante,
                    self.driver, self.live_server_url)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_consultar_inscricoes(self):
        self.driver.get('%s%s' % (self.live_server_url, reverse('home')))
        self.driver.set_window_size(1918, 1027)
        self.driver.find_element(By.LINK_TEXT, "Minhas Inscrições").click()
        self.driver.find_element(By.NAME, "areacientifica").click()
        self.driver.find_element(
            By.NAME, "areacientifica").send_keys("Ciencias")
        self.driver.find_element(
            By.CSS_SELECTOR, ".is-primary > span:nth-child(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".is-light").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".is-expanded > .is-primary").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".even > td:nth-child(2)").click()
        assert self.driver.find_element(
            By.CSS_SELECTOR, ".even > td:nth-child(2)").text == "1"
        assert self.driver.find_element(
            By.CSS_SELECTOR, "td:nth-child(5)").text == "Escola Básica e Secundária do Cadaval - Cadaval"
        assert self.driver.find_element(
            By.CSS_SELECTOR, "tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)").text == "Rafael Duarte"
