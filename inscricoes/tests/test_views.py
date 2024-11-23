from django.test import Client, TestCase
from utilizadores.models import Administrador, Participante
from inscricoes.models import Escola, Inscricao
from configuracao.models import Campus, Diaaberto
from django.utils.datetime_safe import date, datetime
from django.urls import reverse
from utilizadores.tests.test_models import create_Administrador_0, create_Colaborador_0, create_Coordenador_0, create_Participante_0, create_Participante_1, create_ProfessorUniversitario_0, create_Utilizador_0
from unittest import mock
import pytz
from unittest.mock import Mock
from inscricoes.tests.test_models import create_Escola_0, create_Inscricao_0, create_Inscricao_1, create_Inscricaoprato_0, create_Inscricaosessao_0, create_Inscricaosessao_1, create_Inscricaotransporte_0, create_Responsavel_0
from dia_aberto.views import error404
from inscricoes.tests.samples import create_Atividade_0, create_Campus_0, create_Diaaberto_0, create_Sessao_0, create_Sessao_1, create_Sessao_2
from django.contrib.auth.models import Group
from django.core.management import call_command


class TestInscricaoPDFView(TestCase):
    """ Teste suite da view "InscricaoPDF" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_InscricaoPDF_GET_inscricaoNaoExiste(self):
        """ Teste de método GET quando inscrição não existe """
        self.client.force_login(create_Coordenador_0())
        pk = 2
        while Inscricao.objects.filter(pk=pk).count() > 0:
            pk += 1
        response = self.client.get(
            reverse('inscricoes:inscricao-pdf', kwargs={'pk': pk}))
        self.assertRedirects(response, reverse(
            'utilizadores:mensagem', args=[404]))

    def test_InscricaoPDF_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:inscricao-pdf', kwargs={'pk': self.inscricao.pk}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_InscricaoPDF_GET_naoParticipanteCoordenadorAdministradorColaborador(self):
        """ Teste de método GET sem ser participante """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:inscricao-pdf', kwargs={'pk': self.inscricao.pk}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_InscricaoPDF_GET_inscricaoDeOutroParticipante(self):
        """ Teste de método GET logado como outro Participante """
        self.client.force_login(create_Participante_1())
        response = self.client.get(
            reverse('inscricoes:inscricao-pdf', kwargs={'pk': self.inscricao.pk}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para aceder a esta página!')

    def test_InscricaoPDF_GET_ok(self):
        """ Teste de método GET sucesso """
        create_Diaaberto_0()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:inscricao-pdf', kwargs={'pk': self.inscricao.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'inscricoes/pdf.html')
        self.assertIsNotNone(response.context['request'])
        self.assertEquals(response.context['inscricao'], self.inscricao)
        self.assertEquals(
            response.context['ano'], self.inscricao.diaaberto.ano)


class TestAtividadesAPIView(TestCase):
    """ Teste suite da view "AtividadesAPI" da app "inscricoes" """

    def test_AtividadesAPI_GET_vazia(self):
        """ Teste de método GET com a API vazia """
        response = self.client.get(reverse('inscricoes:api-atividades'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'count': 0,
            'next': None,
            'previous': None,
            'results': [],
        })

    def test_AtividadesAPI_GET_atividade(self):
        """ Teste de método GET com uma atividade """
        sessao = create_Sessao_0()
        atividade = sessao.atividadeid
        response = self.client.get(
            reverse('inscricoes:api-atividades'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)


class TestCriarInscricaoView(TestCase):
    """ Teste suite da view "CriarInscricao" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.campus = create_Campus_0()

    def test_CriarInscricao_GET_semLogin(self):
        """ Teste de método GET sem login """
        create_Diaaberto_0()
        response = self.client.get(reverse('inscricoes:criar-inscricao'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_CriarInscricao_GET_naoParticipante(self):
        """ Teste de método GET sem ser participante """
        create_Diaaberto_0()
        utilizadores = [create_Utilizador_0(),
                        create_Coordenador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0(),
                        create_Administrador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(reverse('inscricoes:criar-inscricao'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_CriarInscricao_GET_naoHaDiaAberto(self):
        """ Teste de método GET sem ser participante """
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Ainda não é permitido criar inscrições')

    @mock.patch('inscricoes.views.datetime', Mock(now=Mock(return_value=datetime(2020, 1, 1, 9, 30, tzinfo=pytz.UTC))))
    def test_CriarInscricao_GET_antesDoPeriodoDeInscricoes(self):
        """ Teste de método GET antes do período de inscricões """
        diaaberto = create_Diaaberto_0()
        diaaberto.datainscricaoatividadesinicio = datetime(
            2021, 1, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.datainscricaoatividadesfim = datetime(
            2021, 3, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.save()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], f'Período de abertura das inscrições: 01/01/2021 até 01/03/2021')

    @mock.patch('inscricoes.views.datetime', Mock(now=Mock(return_value=datetime(2021, 4, 1, 9, 30, tzinfo=pytz.UTC))))
    def test_CriarInscricao_GET_depoisDoPeriodoDeInscricoes(self):
        """ Teste de método GET depois do período de inscricões """
        diaaberto = create_Diaaberto_0()
        diaaberto.datainscricaoatividadesinicio = datetime(
            2021, 1, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.datainscricaoatividadesfim = datetime(
            2021, 3, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.save()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], f'Período de abertura das inscrições: 01/01/2021 até 01/03/2021')

    def test_CriarInscricao_GET_ok(self):
        """ Teste de método GET sucesso """
        create_Diaaberto_0()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(reverse('inscricoes:criar-inscricao'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_info.html')
        self.assertIsNotNone(response.context['wizard'])

    def test_CriarInscricao_POST_semLogin(self):
        """ Teste de método POST sem login """
        create_Diaaberto_0()
        response = self.client.post(reverse('inscricoes:criar-inscricao'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_CriarInscricao_POST_naoParticipante(self):
        """ Teste de método POST sem ser participante """
        create_Diaaberto_0()
        utilizadores = [create_Utilizador_0(),
                        create_Coordenador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0(),
                        create_Administrador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.post(reverse('inscricoes:criar-inscricao'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_CriarInscricao_POST_naoHaDiaAberto(self):
        """ Teste de método POST sem ser participante """
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Ainda não é permitido criar inscrições')

    @mock.patch('inscricoes.views.datetime', Mock(now=Mock(return_value=datetime(2020, 1, 1, 9, 30, tzinfo=pytz.UTC))))
    def test_CriarInscricao_POST_antesDoPeriodoDeInscricoes(self):
        """ Teste de método POST antes do período de inscricões """
        diaaberto = create_Diaaberto_0()
        diaaberto.datainscricaoatividadesinicio = datetime(
            2021, 1, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.datainscricaoatividadesfim = datetime(
            2021, 3, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.save()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], f'Período de abertura das inscrições: 01/01/2021 até 01/03/2021')

    @mock.patch('inscricoes.views.datetime', Mock(now=Mock(return_value=datetime(2021, 4, 1, 9, 30, tzinfo=pytz.UTC))))
    def test_CriarInscricao_POST_depoisDoPeriodoDeInscricoes(self):
        """ Teste de método POST depois do período de inscricões """
        diaaberto = create_Diaaberto_0()
        diaaberto.datainscricaoatividadesinicio = datetime(
            2021, 1, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.datainscricaoatividadesfim = datetime(
            2021, 3, 1, 9, 30, tzinfo=pytz.UTC)
        diaaberto.save()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], f'Período de abertura das inscrições: 01/01/2021 até 01/03/2021')

    def test_CriarInscricao_POST_semVariaveis(self):
        """ Teste de método POST sem variáveis POST """
        create_Diaaberto_0()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], f'Erro no servidor')

    def test_CriarInscricao_POST_info_ok(self):
        """ Teste de método POST sucesso """
        create_Diaaberto_0()
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.post(reverse('inscricoes:criar-inscricao'), {
                                    'criar_inscricao-current_step': ['info'], 'info-individual': ['True']}, follow=True)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_responsaveis.html')
        self.assertIsNotNone(response.context['wizard'])

    def test_CriarInscricao_POST_info_individual_ok(self):
        """ Teste de método POST passo "info" > "responsaveis" individual sucesso """
        create_Diaaberto_0()
        participante = create_Participante_0()
        self.client.force_login(participante)
        POST = {
            'criar_inscricao-current_step': ['info'],
            'info-individual': ['True']
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_responsaveis.html')
        self.assertIsNotNone(response.context['wizard'])
        self.assertFalse(response.context['form'].errors)

        def test_CriarInscricao_POST_info_naoIndividual_ok(self):
            """ Teste de método POST passo "info" > "responsaveis" não individual sucesso """
            create_Diaaberto_0()
            participante = create_Participante_0()
            self.client.force_login(participante)
            POST = {
                'criar_inscricao-current_step': ['info'],
            }
            response = self.client.post(
                reverse('inscricoes:criar-inscricao'), POST)
            self.assertTemplateUsed(
                response, 'inscricoes/inscricao_wizard_responsaveis.html')
            self.assertIsNotNone(response.context['wizard'])
            self.assertFalse(response.context['form'].errors)

    def test_CriarInscricao_POST_responsaveis_erroCamposVazios(self):
        """ Teste de método POST passo "responsaveis" > "escola" erro campos vazios """
        self.test_CriarInscricao_POST_info_individual_ok()
        POST = {
            'criar_inscricao-current_step': ['responsaveis'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_responsaveis.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_responsaveis_erroEmailInvalido(self):
        """ Teste de método POST passo "responsaveis" > "escola" erro email inválido """
        self.test_CriarInscricao_POST_info_individual_ok()
        POST = {
            'criar_inscricao-current_step': ['responsaveis'],
            'responsaveis-nome': ['Rafael Ricardo'],
            'responsaveis-email': ['email@invalido'],
            'responsaveis-tel': ['+351931231234'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_responsaveis.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_responsaveis_erroTelInvalido(self):
        """ Teste de método POST passo "responsaveis" > "escola" erro tel inválido """
        self.test_CriarInscricao_POST_info_individual_ok()
        POST = {
            'criar_inscricao-current_step': ['responsaveis'],
            'responsaveis-nome': ['Rafael Ricardo'],
            'responsaveis-email': ['email@valido.com'],
            'responsaveis-tel': ['981231234'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_responsaveis.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_responsaveis_ok(self):
        """ Teste de método POST passo "responsaveis" > "escola" sucesso """
        self.test_CriarInscricao_POST_info_individual_ok()
        POST = {
            'criar_inscricao-current_step': ['responsaveis'],
            'responsaveis-nome': ['Rafael Ricardo'],
            'responsaveis-email': ['email@valido.com'],
            'responsaveis-tel': ['931231234'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_escola.html')
        self.assertFalse(response.context['form'].errors)
        self.assertIsNotNone(response.context['escolas'])
        self.assertIsNotNone(response.context['inicio'])
        self.assertIsNotNone(response.context['fim'])

    def test_CriarInscricao_POST_escola_erroCamposVazios(self):
        """ Teste de método POST passo "escola" > "transporte" erro campos vazios """
        self.test_CriarInscricao_POST_responsaveis_ok()
        POST = {
            'criar_inscricao-current_step': ['escola'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_escola.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_escola_diaInvalido(self):
        """ Teste de método POST passo "escola" > "transporte" dia inválido """
        self.test_CriarInscricao_POST_responsaveis_ok()
        diaaberto = Diaaberto.current()
        diaaberto.datadiaabertofim = datetime(2021, 5, 27, tzinfo=pytz.UTC)
        diaaberto.save()
        POST = {
            'criar_inscricao-current_step': ['escola'],
            'escola-dia': ['29/05/2021'],
            'escola-nalunos': ['7'],
            'escola-nome_escola': ['Escola Secundária de Loulé'],
            'escola-local': ['Loulé'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_escola.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_escola_nalunosInvalido(self):
        """ Teste de método POST passo "escola" > "transporte" nº de alunos inválido """
        self.test_CriarInscricao_POST_responsaveis_ok()
        POST = {
            'criar_inscricao-current_step': ['escola'],
            'escola-dia': ['29/05/2021'],
            'escola-nalunos': ['0'],
            'escola-nome_escola': ['Escola Secundária de Loulé'],
            'escola-local': ['Loulé'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_escola.html')
        self.assertTrue(response.context['form'].errors)
        POST.update({
            'escola-nalunos': ['300'],
        })
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_escola.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_escola_ok(self):
        """ Teste de método POST passo "escola" > "transporte" sucesso """
        self.test_CriarInscricao_POST_responsaveis_ok()
        POST = {
            'criar_inscricao-current_step': ['escola'],
            'escola-dia': ['29/05/2021'],
            'escola-nalunos': ['30'],
            'escola-nome_escola': ['Escola Secundária de Loulé'],
            'escola-local': ['Loulé'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_transporte.html')
        self.assertFalse(response.context['form'].errors)

    def test_CriarInscricao_POST_transporte_erroCamposVazios(self):
        """ Teste de método POST passo "transporte" > "almoco" erro campos vazios """
        self.test_CriarInscricao_POST_escola_ok()
        POST = {
            'criar_inscricao-current_step': ['transporte'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_transporte.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_transporte_ok(self):
        """ Teste de método POST passo "transporte" > "almoco" sucesso """
        self.test_CriarInscricao_POST_escola_ok()
        POST = {
            'criar_inscricao-current_step': ['transporte'],
            'transporte-meio': ['autocarro'],
            'transporte-hora_chegada': ['8:55'],
            'transporte-local_chegada': ['Terminal Rodoviário de Faro'],
            'transporte-entrecampi': ['']
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_almoco.html')
        self.assertFalse(response.context['form'].errors)
        self.assertIsNotNone(response.context['precoalunos'])
        self.assertIsNotNone(response.context['precoprofessores'])
        self.assertIsNotNone(response.context['campi'])
        self.assertIsNotNone(response.context['pratos_info'])
        self.assertIsNotNone(response.context['nalunos'])
        self.assertIsNotNone(response.context['nresponsaveis'])

    def test_CriarInscricao_POST_almoco_erroCampusEscolhidoMasSemPessoas(self):
        """ Teste de método POST passo "almoco" > "sessoes" erro campus escolhido sem pessoas """
        self.test_CriarInscricao_POST_transporte_ok()
        POST = {
            'criar_inscricao-current_step': ['almoco'],
            'almoco-campus': [f'{self.campus.id}'],
            'almoco-npratosalunos': ['0'],
            'almoco-npratosdocentes': ['0'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_almoco.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_almoco_erroEscolhidasPessoasMasSemCampus(self):
        """ Teste de método POST passo "almoco" > "sessoes" erro escolhidas pessoas sem campus """
        self.test_CriarInscricao_POST_transporte_ok()
        POST = {
            'criar_inscricao-current_step': ['almoco'],
            'almoco-campus': [''],
            'almoco-npratosalunos': ['2'],
            'almoco-npratosdocentes': ['0'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_almoco.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_almoco_erroAlmocosExcedemInscritos(self):
        """ Teste de método POST passo "almoco" > "sessoes" erro nº de almoços excede nº de inscritos """
        self.test_CriarInscricao_POST_transporte_ok()
        POST = {
            'criar_inscricao-current_step': ['almoco'],
            'almoco-campus': [''],
            'almoco-npratosalunos': ['40'],
            'almoco-npratosdocentes': ['2'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_almoco.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_almoco_ok(self):
        """ Teste de método POST passo "almoco" > "sessoes" sucesso """
        self.test_CriarInscricao_POST_transporte_ok()
        POST = {
            'criar_inscricao-current_step': ['almoco'],
            'almoco-campus': [f'{self.campus.id}'],
            'almoco-npratosalunos': ['3'],
            'almoco-npratosdocentes': ['0'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertFalse(response.context['form'].errors)
        self.assertIsNotNone(response.context['campus'])
        self.assertIsNotNone(response.context['unidades_organicas'])
        self.assertIsNotNone(response.context['departamentos'])
        self.assertIsNotNone(response.context['tipos'])
        self.assertIsNotNone(response.context['publicos_alvo'])
        self.assertIsNotNone(response.context['nalunos'])
        self.assertIsNotNone(response.context['dia'])

    def test_CriarInscricao_POST_sessoes_erroSemVariáveis(self):
        """ Teste de método POST passo "sessoes" > "submissao" nenhuma variável enviada """
        self.test_CriarInscricao_POST_almoco_ok()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_sessoes_erroVariáveisInválidas(self):
        """ Teste de método POST passo "sessoes" > "submissao" variáveis inválidas """
        self.test_CriarInscricao_POST_almoco_ok()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
            'sessoes-sessoes': ['{<script>alert("Script Injection")</script>}'],
            'sessoes-sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_sessoes_erroNenhumaSessao(self):
        """ Teste de método POST passo "sessoes" > "submissao" nenhuma sessão """
        self.test_CriarInscricao_POST_almoco_ok()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
            'sessoes-sessoes': ['{}'],
            'sessoes-sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_sessoes_erroSessaoNaoExiste(self):
        """ Teste de método POST passo "sessoes" > "submissao" sessão não existe """
        self.test_CriarInscricao_POST_almoco_ok()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
            'sessoes-sessoes': ['{"1": 2}'],
            'sessoes-sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_sessoes_erroAtividadeNaoValidada(self):
        """ Teste de método POST passo "sessoes" > "submissao" atividade não validada """
        self.test_CriarInscricao_POST_almoco_ok()
        sessao = create_Sessao_0()
        sessao.atividadeid.estado = "Pendente"
        sessao.atividadeid.save()
        sessao.save()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
            'sessoes-sessoes': ['{"'+str(sessao.id)+'": 2}'],
            'sessoes-sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_sessoes_erroSessaoDeOutroDia(self):
        """ Teste de método POST passo "sessoes" > "submissao" sessão de outro dia """
        self.test_CriarInscricao_POST_almoco_ok()
        # dia escolhido: 29/05/2021
        sessao = create_Sessao_0()
        sessao.dia = date(2021, 5, 28)
        sessao.save()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
            'sessoes-sessoes': ['{"'+str(sessao.id)+'": 2}'],
            'sessoes-sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_sessoes_erroMaisInscritosQueVagas(self):
        """ Teste de método POST passo "sessoes" > "submissao" mais inscritos que vagas """
        self.test_CriarInscricao_POST_almoco_ok()
        sessao = create_Sessao_0()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
            'sessoes-sessoes': ['{"'+str(sessao.id)+'": '+str(sessao.vagas + 1)+'}'],
            'sessoes-sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_sessoes_erroMaisIncritosQueDisponiveis(self):
        """ Teste de método POST passo "sessoes" > "submissao" mais alunos inscritos em sessões que disponíveis na inscrição """
        self.test_CriarInscricao_POST_almoco_ok()
        # inscritos: 30
        sessao = create_Sessao_0()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
            'sessoes-sessoes': ['{"'+str(sessao.id)+'": 31}'],
            'sessoes-sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_sessoes_erroHorariosSobrepostos(self):
        """ Teste de método POST passo "sessoes" > "submissao" sessões com horários sobrepostos """
        self.test_CriarInscricao_POST_almoco_ok()
        # inscritos: 30
        sessao0 = create_Sessao_0()
        sessao1 = create_Sessao_1()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
            'sessoes-sessoes': ['{"'+str(sessao0.id)+'": 20,"'+str(sessao1.id)+'": 20}'],
            'sessoes-sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/inscricao_wizard_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_CriarInscricao_POST_sessoes_ok(self):
        """ Teste de método POST passo "sessoes" > "submissao" sucesso """
        self.test_CriarInscricao_POST_almoco_ok()
        # inscritos: 30
        sessao0 = create_Sessao_0()
        sessao1 = create_Sessao_1()
        POST = {
            'criar_inscricao-current_step': ['sessoes'],
            'sessoes-sessoes': ['{"'+str(sessao0.id)+'": 10,"'+str(sessao1.id)+'": 20}'],
            'sessoes-sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:criar-inscricao'), POST, follow=True)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_submissao.html')


class TestConsultarAlterarInscricaoView(TestCase):
    """ Teste suite da view "ConsultarInscricao" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        call_command('create_groups')
        cls.inscricao = create_Inscricao_0()
        group = Group.objects.get(name='Participante')
        group.user_set.add(cls.inscricao.participante)
        group.save()
        cls.inscricao.participante.save()
        for info in [
            create_Responsavel_0(),
            create_Inscricaoprato_0(),
            create_Inscricaotransporte_0(),
            create_Inscricaosessao_0(),
            create_Inscricaosessao_1(),
        ]:
            info.inscricao = cls.inscricao
            info.save()
        cls.inscricao.save()

    def test_ConsultarInscricao_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ConsultarInscricao_GET_inscricaoNaoExiste(self):
        """ Teste de método GET quando inscrição não existe """
        self.client.force_login(self.inscricao.participante)
        pk = 2
        while Inscricao.objects.filter(pk=pk).count() > 0:
            pk += 1
        response = self.client.get(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': pk}))
        self.assertRedirects(response, reverse(
            'utilizadores:mensagem', args=[404]))

    def test_ConsultarInscricao_GET_naoParticipanteCoordenadorAdministrador(self):
        """ Teste de método GET sem ser participante, coordenador ou administrador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_ConsultarInscricao_GET_outroParticipante(self):
        """ Teste de método GET sendo outro participante """
        self.client.force_login(create_Participante_1())
        response = self.client.get(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para aceder a esta página!')

    def test_ConsultarInscricao_GET_ok(self):
        """ Teste de método GET sucesso """
        participante = create_Participante_0()
        self.client.force_login(participante)
        response = self.client.get(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_responsaveis.html')

    def test_ConsultarInscricao_POST_semLogin(self):
        """ Teste de método POST sem login """
        response = self.client.post(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ConsultarInscricao_POST_inscricaoNaoExiste(self):
        """ Teste de método POST quando inscrição não existe """
        self.client.force_login(self.inscricao.participante)
        pk = 2
        while Inscricao.objects.filter(pk=pk).count() > 0:
            pk += 1
        response = self.client.post(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': pk}))
        self.assertRedirects(response, reverse(
            'utilizadores:mensagem', args=[404]))

    def test_ConsultarInscricao_POST_naoParticipanteCoordenadorAdministrador(self):
        """ Teste de método POST sem ser participante, coordenador ou administrador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.post(
                reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_ConsultarInscricao_POST_outroParticipante(self):
        """ Teste de método POST sendo outro participante """
        self.client.force_login(create_Participante_1())
        response = self.client.post(
            reverse('inscricoes:consultar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para aceder a esta página!')

    @mock.patch('inscricoes.views.datetime', Mock(now=Mock(return_value=datetime(2021, 4, 1, 9, 30, tzinfo=pytz.UTC))))
    def test_AlterarInscricao_POST_depoisDoPeriodoDeInscricoes(self):
        """ Teste de método POST depois do período de inscricões """
        self.inscricao.diaaberto.datainscricaoatividadesinicio = datetime(
            2021, 1, 1, 9, 30, tzinfo=pytz.UTC)
        self.inscricao.diaaberto.datainscricaoatividadesfim = datetime(
            2021, 3, 1, 9, 30, tzinfo=pytz.UTC)
        self.inscricao.diaaberto.save()
        self.inscricao.save()
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 0,
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), follow=True)
        self.assertTemplateUsed(
            response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context[-1]['m'], f'Não pode alterar a inscrição fora do período: 01/01/2021 até 01/03/2021')

    def test_AlterarInscricao_POST_responsaveis_erroCamposVazios(self):
        """ Teste de método POST passo "responsaveis" erro campos vazios """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 0,
        }
        POST = {
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_responsaveis.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_responsaveis_erroEmailInvalido(self):
        """ Teste de método POST passo "responsaveis" erro email inválido """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 0,
        }
        POST = {
            'nome': ['Rafael Ricardo'],
            'email': ['email@invalido'],
            'tel': ['+351931231234'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_responsaveis.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_responsaveis_erroTelInvalido(self):
        """ Teste de método POST passo "responsaveis" erro tel inválido """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 0,
        }
        POST = {
            'nome': ['Rafael Ricardo'],
            'email': ['email@valido.com'],
            'tel': ['981231234'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_responsaveis.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_responsaveis_ok(self):
        """ Teste de método POST passo "responsaveis" sucesso """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 0,
        }
        POST = {
            'nome': ['Rafael Ricardo'],
            'email': ['email@valido.com'],
            'tel': ['931231234'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST, follow=True)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_responsaveis.html')
        self.assertFalse(response.context['form'].errors)

    def test_AlterarInscricao_POST_escola_erroCamposVazios(self):
        """ Teste de método POST passo "escola" erro campos vazios """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 1,
        }
        POST = {
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_escola.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_escola_inscricaoEscolaEInfoTurmaVazia(self):
        """ Teste de método POST passo "escola" inscrição de escola e info da turma vazia """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 1,
        }
        POST = {
            'dia': ['29/05/2021'],
            'nalunos': ['7'],
            'nome_escola': ['Escola Secundária de Loulé'],
            'local': ['Loulé'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_escola.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_escola_nalunosInvalido(self):
        """ Teste de método POST passo "escola" > "transporte" nº de alunos inválido """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 1,
        }
        POST = {
            'dia': ['29/05/2021'],
            'nalunos': ['0'],
            'nome_escola': ['Escola Secundária de Loulé'],
            'local': ['Loulé'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_escola.html')
        self.assertTrue(response.context['form'].errors)
        POST.update({
            'nalunos': ['300'],
        })
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_escola.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_escola_ok(self):
        """ Teste de método POST passo "escola" sucesso """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 1,
        }
        POST = {
            'nalunos': ['30'],
            'nome_escola': ['Escola Secundária de Loulé'],
            'local': ['Loulé'],
            'ano': ['12'],
            'turma': ['B'],
            'areacientifica': ['Ciências e Tecnologia'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST, follow=True)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_escola.html')
        self.assertFalse(response.context['form'].errors)

    def test_AlterarInscricao_POST_transporte_erroCamposVazios(self):
        """ Teste de método POST passo "transporte" erro campos vazios """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 2,
        }
        POST = {
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_transporte.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_transporte_ok(self):
        """ Teste de método POST passo "transporte" sucesso """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 2,
        }
        POST = {
            'meio': ['autocarro'],
            'hora_chegada': ['8:55'],
            'local_chegada': ['Terminal Rodoviário de Faro'],
            'entrecampi': ['']
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST, follow=True)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_transporte.html')
        self.assertFalse(response.context['form'].errors)

    def test_AlterarInscricao_POST_almoco_erroCampusEscolhidoMasSemPessoas(self):
        """ Teste de método POST passo "almoco" erro campus escolhido sem pessoas """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 3,
        }
        POST = {
            'campus': [f'{create_Campus_0().id}'],
            'npratosalunos': ['0'],
            'npratosdocentes': ['0'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_almoco.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_almoco_erroEscolhidasPessoasMasSemCampus(self):
        """ Teste de método POST passo "almoco" erro escolhidas pessoas sem campus """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 3,
        }
        POST = {
            'campus': [''],
            'npratosalunos': ['2'],
            'npratosdocentes': ['0'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_almoco.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_almoco_erroAlmocosExcedemInscritos(self):
        """ Teste de método POST passo "almoco" erro nº de almoços excede nº de inscritos """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 3,
        }
        POST = {
            'campus': [''],
            'npratosalunos': ['40'],
            'npratosdocentes': ['2'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_almoco.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_almoco_ok(self):
        """ Teste de método POST passo "almoco" sucesso """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 3,
        }
        POST = {
            'campus': [f'{create_Campus_0().id}'],
            'npratosalunos': ['3'],
            'npratosdocentes': ['0'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST, follow=True)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_almoco.html')
        self.assertFalse(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_erroSemVariáveis(self):
        """ Teste de método POST passo "sessoes" nenhuma variável enviada """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        POST = {
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_erroVariáveisInválidas(self):
        """ Teste de método POST passo "sessoes" variáveis inválidas """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        POST = {
            'sessoes': ['{<script>alert("Script Injection")</script>}'],
            'sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_erroNenhumaSessao(self):
        """ Teste de método POST passo "sessoes" nenhuma sessão """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        POST = {
            'sessoes': ['{}'],
            'sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_erroSessaoNaoExiste(self):
        """ Teste de método POST passo "sessoes" sessão não existe """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        POST = {
            'sessoes': ['{"1": 2}'],
            'sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_erroAtividadeNaoValidada(self):
        """ Teste de método POST passo "sessoes" atividade não validada """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        sessao = create_Sessao_0()
        sessao.atividadeid.estado = "Pendente"
        sessao.atividadeid.save()
        sessao.save()
        POST = {
            'sessoes': ['{"'+str(sessao.id)+'": 2}'],
            'sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_erroSessaoDeOutroDia(self):
        """ Teste de método POST passo "sessoes" sessão de outro dia """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        # dia escolhido: 21/08/2020
        sessao = create_Sessao_0()
        sessao.dia = date(2021, 5, 28)
        sessao.save()
        POST = {
            'sessoes': ['{"'+str(sessao.id)+'": 2}'],
            'sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_erroMaisInscritosQueVagas(self):
        """ Teste de método POST passo "sessoes" mais inscritos que vagas """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        sessao = create_Sessao_0()
        POST = {
            'sessoes': ['{"'+str(sessao.id)+'": '+str(sessao.vagas + 1)+'}'],
            'sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_erroMaisIncritosQueDisponiveis(self):
        """ Teste de método POST passo "sessoes" > "submissao" mais alunos inscritos em sessões que disponíveis na inscrição """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        # inscritos: 20
        sessao = create_Sessao_0()
        POST = {
            'sessoes': ['{"'+str(sessao.id)+'": 31}'],
            'sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_erroHorariosSobrepostos(self):
        """ Teste de método POST passo "sessoes" sessões com horários sobrepostos """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        # inscritos: 20
        sessao0 = create_Sessao_0()
        sessao1 = create_Sessao_1()
        POST = {
            'sessoes': ['{"'+str(sessao0.id)+'": 20,"'+str(sessao1.id)+'": 20}'],
            'sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertTrue(response.context['form'].errors)

    def test_AlterarInscricao_POST_sessoes_ok(self):
        """ Teste de método POST passo "sessoes" sucesso """
        self.client.force_login(self.inscricao.participante)
        GET = {
            'pk': self.inscricao.pk,
            'step': 4,
        }
        # inscritos: 20
        sessao0 = create_Sessao_0()
        sessao1 = create_Sessao_2()
        sessao0.dia = self.inscricao.dia
        sessao1.dia = self.inscricao.dia
        sessao0.save()
        sessao1.save()
        POST = {
            'sessoes': ['{"'+str(sessao0.id)+'": 10,"'+str(sessao1.id)+'": 20}'],
            'sessoes_info': ['[]'],
        }
        response = self.client.post(
            reverse('inscricoes:alterar-inscricao', kwargs=GET), POST, follow=True)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricao_sessoes.html')
        self.assertFalse(response.context['form'].errors)


class TestMinhasInscricoesView(TestCase):
    """ Teste suite da view "MinhasInscricoes" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_MinhasInscricoes_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-participante'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_MinhasInscricoes_GET_naoParticipante(self):
        """ Teste de método GET sem ser participante """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Administrador_0(),
                        create_Coordenador_0(),
                        create_Colaborador_0(), ]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:consultar-inscricoes-participante'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_MinhasInscricoes_GET_ok(self):
        """ Teste de método GET sucesso """
        self.client.force_login(self.inscricao.participante)
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-participante'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricoes_participante.html')
        self.assertIsNotNone(response.context['table'])


class TestInscricoesDepartamentoView(TestCase):
    """ Teste suite da view "InscricoesDepartamento" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_InscricoesDepartamento_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-coordenador'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_InscricoesDepartamento_GET_naoCoordenador(self):
        """ Teste de método GET sem ser coordenador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Administrador_0(),
                        create_Participante_0(),
                        create_Colaborador_0(), ]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:consultar-inscricoes-coordenador'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_InscricoesDepartamento_GET_ok(self):
        """ Teste de método GET sucesso """
        self.client.force_login(create_Coordenador_0())
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-coordenador'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricoes_coordenador.html')
        self.assertIsNotNone(response.context['table'])


class TestInscricoesAdminView(TestCase):
    """ Teste suite da view "InscricoesAdmin" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_InscricoesAdmin_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-admin'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_InscricoesAdmin_GET_naoAdministrador(self):
        """ Teste de método GET sem ser administrador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Coordenador_0(),
                        create_Participante_0(),
                        create_Colaborador_0(), ]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:consultar-inscricoes-admin'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_InscricoesAdmin_GET_ok(self):
        """ Teste de método GET sucesso """
        self.client.force_login(create_Administrador_0())
        response = self.client.get(
            reverse('inscricoes:consultar-inscricoes-admin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'inscricoes/consultar_inscricoes_admin.html')
        self.assertIsNotNone(response.context['table'])


class TestApagarInscricaoView(TestCase):
    """ Teste suite da view "ApagarInscricao" da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()

    def test_ApagarInscricao_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.post(
            reverse('inscricoes:apagar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ApagarInscricao_GET_inscricaoNaoExiste(self):
        """ Teste de método GET quando inscrição não existe """
        self.client.force_login(self.inscricao.participante)
        pk = 2
        while Inscricao.objects.filter(pk=pk).count() > 0:
            pk += 1
        response = self.client.get(
            reverse('inscricoes:apagar-inscricao', kwargs={'pk': pk}))
        self.assertRedirects(response, reverse(
            'utilizadores:mensagem', args=[404]))

    def test_ApagarInscricao_GET_naoParticipanteCoordenadorAdministrador(self):
        """ Teste de método GET sem ser participante, coordenador ou administrador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Colaborador_0()]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('inscricoes:apagar-inscricao', kwargs={'pk': self.inscricao.pk}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_ApagarInscricao_GET_outroParticipante(self):
        """ Teste de método GET sendo outro participante """
        self.client.force_login(create_Participante_1())
        response = self.client.get(
            reverse('inscricoes:apagar-inscricao', kwargs={'pk': self.inscricao.pk}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para aceder a esta página!')

    def test_ApagarInscricao_GET_ok(self):
        """ Teste de método GET sucesso """
        inscricao = create_Inscricao_1()
        self.client.force_login(create_Administrador_0())
        response = self.client.get(
            reverse('inscricoes:apagar-inscricao', kwargs={'pk': inscricao.pk}))
        self.assertTrue(not Inscricao.objects.filter(pk=inscricao.pk).exists())
