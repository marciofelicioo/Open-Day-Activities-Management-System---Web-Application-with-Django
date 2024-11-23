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
from atividades.models import Atividade, Tema, Sessao, date
from inscricoes.tests.samples import create_Diaaberto_0, create_Espaco_0, create_Sessao_0, create_Sessao_1, create_Sessao_2, create_Transporte_0, create_Transportehorario_0, create_Horario_0, create_Horario_1, create_Horario_2
from notificacoes.tests.test_models import create_MensagemRecebida_0
from selenium.webdriver.support.wait import WebDriverWait
from seleniumlogin import force_login
import time
from selenium.webdriver.support.ui import Select
from dia_aberto.utils import get_driver


def create_Inscricao_0():
    return Inscricao.objects.get_or_create(
        individual=False,
        nalunos=20,
        escola=create_Escola_0(),
        ano=12,
        turma="A",
        areacientifica="Ciências e Tecnologia",
        participante=create_Participante_Rafael(),
        dia=datetime.date(2020, 8, 28),
        diaaberto=create_Diaaberto_0(),
        meio_transporte='comboio',
        hora_chegada=datetime.time(10, 30, 00),
        local_chegada="Estação de Comboios de Faro",
        entrecampi=False,
    )[0]


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


def create_Escola_0():
    return Escola.objects.get_or_create(
        nome="Judice Fialho",
        local="Portimao",
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


def create_Sessao_1():
    return Sessao.objects.get_or_create(
        ninscritos=0,
        vagas=25,
        atividadeid=create_Atividade_0(),
        dia=date(1970, 1, 2),
        horarioid=create_Horario_1(),
    )[0]


class CriarInscricaoTest(StaticLiveServerTestCase):
    """ Testes funcionais do criar inscrição """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command("create_groups")
        cls.driver = get_driver()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)

    def setUp(self):
        self.diaAberto = create_Diaaberto_0()
        self.sessao = create_Sessao_1()
        self.sessao.save()
        self.participante = create_Participante_Rafael()
        group = Group.objects.get(name='Participante')
        group.user_set.add(self.participante)
        force_login(self.participante,
                    self.driver, self.live_server_url)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_criar_inscricao_1(self):
        self.driver.get('%s%s' % (self.live_server_url, reverse('home')))
        self.driver.find_element(By.LINK_TEXT, "Criar Inscrição").click()
        assert self.driver.find_element(
            By.CSS_SELECTOR, ".button:nth-child(2) > span:nth-child(2)").text == "Escola (Turma)"
        self.driver.find_element(
            By.CSS_SELECTOR, ".button:nth-child(2) > span:nth-child(2)").click()
        assert self.driver.find_element(
            By.CSS_SELECTOR, ".column:nth-child(1) .label").text == "Nome"
        assert self.driver.find_element(
            By.CSS_SELECTOR, ".column:nth-child(2) .label").text == "E-mail"
        element = self.driver.find_element(By.ID, "id_responsaveis-nome")
        assert element.is_enabled() is True
        self.driver.find_element(
            By.CSS_SELECTOR, ".is-success > span:nth-child(1)").click()
        # escola
        button = self.driver.find_element(By.NAME, "escola-dia")
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(1)
        self.driver.find_element(
            By.CSS_SELECTOR, ".is-selectable:nth-child(6) > span").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".b-numberinput .input").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".b-numberinput .input").send_keys("2")
        self.driver.find_element(By.ID, "id_escola-nome_escola").click()
        self.driver.find_element(
            By.ID, "id_escola-nome_escola").send_keys("Judice Fialho")
        self.driver.find_element(By.ID, "id_escola-local").click()
        self.driver.find_element(
            By.ID, "id_escola-local").send_keys("Portimao")
        self.driver.find_element(By.ID, "id_escola-ano").click()
        self.driver.find_element(By.ID, "id_escola-ano").send_keys("12")
        self.driver.find_element(By.ID, "id_escola-turma").click()
        self.driver.find_element(By.ID, "id_escola-turma").send_keys("A")
        self.driver.find_element(By.ID, "id_escola-areacientifica").click()
        self.driver.find_element(
            By.ID, "id_escola-areacientifica").send_keys("Ciências e Tecnologia")
        element = self.driver.find_element(
            By.CSS_SELECTOR, ".b-numberinput .input")
        assert element.is_enabled() is True
        element = self.driver.find_element(By.NAME, "escola-dia")
        assert element.is_enabled() is True
        value = self.driver.find_element(
            By.ID, "id_escola-nome_escola").get_attribute("value")
        assert value == "Judice Fialho"
        value = self.driver.find_element(
            By.ID, "id_escola-areacientifica").get_attribute("value")
        assert value == "Ciências e Tecnologia"
        self.driver.find_element(
            By.CSS_SELECTOR, ".is-success > span:nth-child(1)").click()
        # transporte
        time.sleep(1)
        self.driver.find_element(By.NAME, "transporte-meio").click()
        dropdown = Select(self.driver.find_element(By.NAME, "transporte-meio"))
        dropdown.select_by_visible_text("Comboio")
        #self.driver.find_element(By.NAME, "transporte-meio").click()
        self.driver.find_element(By.NAME, "transporte-hora_chegada").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".control:nth-child(1) select").click()
        dropdown = Select(self.driver.find_element(
            By.CSS_SELECTOR, ".control:nth-child(1) select"))
        dropdown.select_by_visible_text("10")
        self.driver.find_element(
            By.CSS_SELECTOR, ".control:nth-child(1) select").click()
        self.driver.find_element(By.CSS_SELECTOR, ".is-empty > select").click()
        dropdown = Select(self.driver.find_element(
            By.CSS_SELECTOR, ".is-empty > select"))
        dropdown.select_by_visible_text("30")
        assert self.driver.find_element(
            By.CSS_SELECTOR, ".is-4 .label").text == "Meio de transporte"
        value = self.driver.find_element(
            By.NAME, "transporte-local_chegada").get_attribute("value")
        assert value == "Estação de Comboios de Faro"
        element = self.driver.find_element(By.NAME, "transporte-hora_chegada")
        assert element.is_enabled() is True
        self.driver.find_element(
            By.CSS_SELECTOR, ".is-success > span:nth-child(1)").click()
        # almoço
        self.driver.find_element(By.ID, "id_almoco-campus").click()
        dropdown = Select(self.driver.find_element(By.ID, "id_almoco-campus"))
        dropdown.select_by_visible_text("Gambelas")
        time.sleep(1)
        self.driver.find_element(By.ID, "id_almoco-campus").click()
        self.driver.find_element(By.NAME, "almoco-npratosalunos").click()
        self.driver.find_element(
            By.NAME, "almoco-npratosalunos").send_keys("1")
        # self.driver.find_element(By.NAME, "almoco-npratosdocentes").click()
        # self.driver.find_element(
        #     By.NAME, "almoco-npratosdocentes").send_keys("1")
        assert self.driver.find_element(
            By.CSS_SELECTOR, ".is-5 .label").text == "Campus"
        element = self.driver.find_element(By.NAME, "almoco-npratosalunos")
        assert element.is_enabled() is True
        element = self.driver.find_element(By.NAME, "almoco-npratosdocentes")
        assert element.is_enabled() is True
        self.driver.find_element(
            By.CSS_SELECTOR, ".is-success > span:nth-child(1)").click()
        # sessoes
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(2)").click()
        self.driver.find_element(
            By.CSS_SELECTOR, "tr:nth-child(1) .input").click()
        self.driver.find_element(
            By.CSS_SELECTOR, "tr:nth-child(1) > td:nth-child(3) .input").send_keys("1")
        element = self.driver.find_element(
            By.CSS_SELECTOR, "tr:nth-child(1) .input")
        assert element.is_enabled() is True
        self.driver.find_element(
            By.CSS_SELECTOR, ".is-success > span:nth-child(1)").click()
