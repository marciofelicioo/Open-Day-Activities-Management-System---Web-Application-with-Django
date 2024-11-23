from django.test import Client, SimpleTestCase, TestCase
from utilizadores.models import Administrador, Participante
from inscricoes.models import Escola, Inscricao
from configuracao.models import Diaaberto
from django.utils.datetime_safe import datetime
import pytz
from django.urls import reverse
from inscricoes.views import InscricaoPDF, CriarInscricao, MinhasInscricoes, InscricoesUO, InscricoesAdmin, ConsultarInscricao, ApagarInscricao
from utilizadores.tests.test_models import create_Participante_0
from inscricoes.tests.test_models import create_Inscricao_0


def create_open_day():
    return Diaaberto.objects.create(
        precoalunos=2,
        precoprofessores=2,
        enderecopaginaweb='web.com',
        descricao='Dia Aberto',
        emaildiaaberto='web@web.com',
        ano='2020',
        datadiaabertoinicio=datetime(1970, 1, 1, 9, 30, tzinfo=pytz.UTC),
        datadiaabertofim=datetime(2040, 1, 2, 9, 30, tzinfo=pytz.UTC),
        datainscricaoatividadesinicio=datetime(
            1970, 1, 1, 9, 30, tzinfo=pytz.UTC),
        datainscricaoatividadesfim=datetime(
            2040, 1, 2, 9, 30, tzinfo=pytz.UTC),
        datapropostasatividadesincio=datetime(
            1970, 1, 1, 9, 30, tzinfo=pytz.UTC),
        dataporpostaatividadesfim=datetime(2040, 1, 2, 9, 30, tzinfo=pytz.UTC),
        administradorutilizadorid=None,
        escalasessoes='00:30',
    )


class TestInscricoesUrls(TestCase):
    """ Teste suite dos urls da app "inscricoes" """
    @classmethod
    def setUpTestData(cls):
        cls.participante = create_Participante_0()
        cls.diaaberto = create_open_day()

    def setUp(self):
        self.client.force_login(self.participante)

    def test_url_criar_inscricao(self):
        """ Testes do url "criar-inscrição" """
        response = self.client.get(reverse('inscricoes:criar-inscricao'))
        self.assertEqual(response.resolver_match.func.__name__,
                         CriarInscricao.as_view().__name__)

    def test_url_inscricao_pdf(self):
        """ Testes do url "<int:pk>/pdf" de nome inscricao-pdf """
        inscricao = create_Inscricao_0()
        response = self.client.get(
            reverse('inscricoes:inscricao-pdf', kwargs={"pk": inscricao.pk}))
        self.assertEqual(response.resolver_match.func, InscricaoPDF)

    def test_url_minhas_inscricoes(self):
        """ Testes do url "minhasinscricoes" """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-participante'))
        self.assertEqual(response.resolver_match.func.__name__,
                         MinhasInscricoes.as_view().__name__)

    def test_url_inscricoes_departamento(self):
        """ Testes do url "inscricoesdepartamento" """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-coordenador'))
        self.assertEqual(response.resolver_match.func.__name__,
                         InscricoesUO.as_view().__name__)

    def test_url_inscricoes_admin(self):
        """ Testes do url "inscricoesadmin" """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-admin'))
        self.assertEqual(response.resolver_match.func.__name__,
                         InscricoesAdmin.as_view().__name__)

    def test_url_consultar_inscricao(self):
        """ Testes do url "<int:pk>" de nome consultar-inscricao """
        inscricao = create_Inscricao_0()
        response = self.client.get(
            reverse('inscricoes:consultar-inscricao', kwargs={"pk": inscricao.pk}))
        self.assertEqual(response.resolver_match.func.__name__,
                         ConsultarInscricao.as_view().__name__)

    def test_url_consultar_inscricao_2(self):
        """ Testes do url <int:pk>/<int:step> de nome consultar-inscricao" """
        inscricao = create_Inscricao_0()
        response = self.client.get(reverse(
            'inscricoes:consultar-inscricao', kwargs={"pk": inscricao.pk, "step": 0}))
        self.assertEqual(response.resolver_match.func.__name__,
                         ConsultarInscricao.as_view().__name__)

    def test_url_alterar_inscricao(self):
        """ Testes do url alterar/<int:pk> de nome alterar-inscricao" """
        inscricao = create_Inscricao_0()
        response = self.client.get(
            reverse('inscricoes:alterar-inscricao', kwargs={"pk": inscricao.pk}))
        self.assertEqual(response.resolver_match.func.__name__,
                         ConsultarInscricao.as_view().__name__)

    def test_url_alterar_inscricao_2(self):
        """ Testes do url alterar/<int:pk>/<int:step> de nome alterar-inscricao" """
        inscricao = create_Inscricao_0()
        response = self.client.get(
            reverse('inscricoes:alterar-inscricao', kwargs={"pk": inscricao.pk, "step": 0}))
        self.assertEqual(response.resolver_match.func.__name__,
                         ConsultarInscricao.as_view().__name__)

    def test_url_apagar_inscricao(self):
        """ Testes do url apagar/<int:pk> de nome apagar-inscricao" """
        inscricao = create_Inscricao_0()
        response = self.client.get(
            reverse('inscricoes:apagar-inscricao', kwargs={"pk": inscricao.pk}))
        self.assertEqual(response.resolver_match.func, ApagarInscricao)
