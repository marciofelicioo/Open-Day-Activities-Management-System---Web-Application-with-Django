from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import *
from configuracao.models import *
from utilizadores.models import *
from colaboradores.models import *
from coordenadores.models import *
from notificacoes.models import *
from atividades.models import *
from inscricoes.models import *
from configuracao.tests.test_models import create_campus, create_edificio, create_horario, create_open_day, create_sala, create_transporteH
from utilizadores.tests.test_models import create_Administrador_0, create_Colaborador_0, create_Coordenador_0, create_Coordenador_1, create_Participante_0, create_ProfessorUniversitario_0, create_ProfessorUniversitario_1, create_Utilizador_0
import json
import urllib
from atividades.tests.test_models import create_atividade, create_material, create_sessao, create_tema

def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.parse.urlencode(kwargs) # for Python 3, use urllib.parse.urlencode instead

class TestConsultarAtividadesProfView(TestCase):
    

    @classmethod
    def setUp(self):
        self.professor = create_ProfessorUniversitario_0()

    def test_ProfAtividades_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('atividades:minhasAtividades'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ConsultarAtividadesProf_GET_naoProfessor(self):
        utilizadores = [create_Utilizador_0(),
                        create_Colaborador_0(),
                        create_Administrador_0(),
                        create_Coordenador_0(),
                        create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:minhasAtividades'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

        def test_ConsultarAtividadesProf_GET_ok(self):
            self.client.force_login(self.professor)
            response = self.client.get(
                reverse('atividades:minhasAtividades'))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'atividades/minhasAtividades.html')
            self.assertIsNotNone(response.context['table'])


class TestConsultarAtividadesCoordView(TestCase):
    

    @classmethod
    def setUp(self):
        self.coord = create_Coordenador_0()

    def test_ProfAtividades_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('atividades:atividadesUOrganica'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ConsultarAtividadesCoord_GET_naoCoord(self):
        utilizadores = [create_Utilizador_0(),
                        create_Colaborador_0(),
                        create_Administrador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:atividadesUOrganica'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

        def ConsultarAtividadesCoord_GET_ok(self):
            self.client.force_login(self.coord)
            response = self.client.get(
                reverse('atividades:atividadesUOrganica'))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'atividades/atividadesUOrganica')
            self.assertIsNotNone(response.context['table'])


class TestConsultarAtividadesProfView(TestCase):
    

    @classmethod
    def setUp(self):
        self.admin = create_Administrador_0()

    def test_ProfAtividades_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('atividades:atividadesAdmin'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ConsultarAtividadesProf_GET_naoProfessor(self):
        utilizadores = [create_Utilizador_0(),
                        create_Colaborador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Coordenador_0(),
                        create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:atividadesAdmin'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

        def test_ConsultarAtividadesProf_GET_ok(self):
            self.client.force_login(self.professor)
            response = self.client.get(
                reverse('atividades:minhasAtividades'))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'atividades/atividadesAdmin.html')
            self.assertIsNotNone(response.context['table'])


class TestProporAtividadesView(TestCase):
    

    def setUp(self):
        self.professor = create_ProfessorUniversitario_0()

    def test_ProfAtividades_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('atividades:proporAtividade'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ProporAtividadesView_GET_naoProfessor(self):
        utilizadores = [create_Utilizador_0(),
                        create_Colaborador_0(),
                        create_Administrador_0(),
                        create_Coordenador_0(),
                        create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:minhasAtividades'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

        def test_ProporAtividade_GET_ok(self):
            self.client.force_login(self.professor)
            response = self.client.get(
                reverse('atividades:proporAtividade'))
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'atividades/proporAtividadeAtividade.html')


class TestAlterarAtividadeView(TestCase):

    def setUp(self):
        self.diaaberto= create_open_day()
        self.tema= create_tema()
        self.espaco= create_sala(create_edificio(create_campus()))
        self.professor= create_ProfessorUniversitario_0()
        self.atividade = create_atividade( self.professor,
                                         self.diaaberto,
                                        self.espaco ,
                                        self.tema)


    def test_AlterarAtividade_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('atividades:alterarAtividade', kwargs={'id': self.atividade.id}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_AlterarAtividade_GET_naoProfessor(self):
        utilizadores = [create_Utilizador_0(),
                create_Colaborador_0(),
                create_Administrador_0(),
                create_Coordenador_0(),
                create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:alterarAtividade', kwargs={'id': self.atividade.id}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()
#
    def test_AlterarAtividade_GET_DeOutroProfessor(self):
        self.client.force_login(create_ProfessorUniversitario_1())
        response = self.client.get(
            reverse('atividades:alterarAtividade', kwargs={'id': self.atividade.id}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para esta ação!')



class TestInserirSessaoView(TestCase):
    
    def setUp(self):
        self.diaaberto= create_open_day()
        self.tema= create_tema()
        self.espaco= create_sala(create_edificio(create_campus()))
        self.professor= create_ProfessorUniversitario_0()
        self.atividade = create_atividade( self.professor,
                                         self.diaaberto,
                                        self.espaco ,
                                        self.tema)
        self.horario= create_horario(inicio=time(14,0),fim=time(14,30))
        self.sessao= create_sessao(self.atividade, self.horario)

    def test_InserirSessao_GET_semLogin(self):
        response = self.client.get(
            reverse('atividades:inserirSessao', kwargs={'id': self.atividade.id}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_InserirSessao_GET_naoProfessor(self):
        utilizadores = [create_Utilizador_0(),
                create_Colaborador_0(),
                create_Administrador_0(),
                create_Coordenador_0(),
                create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:inserirSessao', kwargs={'id': self.atividade.id}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()
#
    def test_InserirSessao_GET_DeOutroProfessor(self):
        self.client.force_login(create_ProfessorUniversitario_1())
        response = self.client.get(
            reverse('atividades:inserirSessao', kwargs={'id': self.atividade.id}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para esta ação!')


class TestEliminarAtividadeView(TestCase):
    
    def setUp(self):
        self.diaaberto= create_open_day()
        self.tema= create_tema()
        self.espaco= create_sala(create_edificio(create_campus()))
        self.professor= create_ProfessorUniversitario_0()
        self.atividade = create_atividade( self.professor,
                                         self.diaaberto,
                                        self.espaco ,
                                        self.tema)
        self.horario= create_horario(inicio=time(14,0),fim=time(14,30))
        self.sessao= create_sessao(self.atividade, self.horario)

    def test_EliminarAtividade_GET_semLogin(self):
        response = self.client.get(
            reverse('atividades:eliminarAtividade', kwargs={'id': self.atividade.id}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_EliminarAtividade_GET_naoProfessor(self):
        utilizadores = [create_Utilizador_0(),
                create_Colaborador_0(),
                create_Administrador_0(),
                create_Coordenador_0(),
                create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:eliminarAtividade', kwargs={'id': self.atividade.id}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()
#
    def test_EliminarAtividade_GET_DeOutroProfessor(self):
        self.client.force_login(create_ProfessorUniversitario_1())
        response = self.client.get(
            reverse('atividades:eliminarAtividade', kwargs={'id': self.atividade.id}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para esta ação!')

    
class TestEliminarSessaoView(TestCase):
    
    def setUp(self):
        self.diaaberto= create_open_day()
        self.tema= create_tema()
        self.espaco= create_sala(create_edificio(create_campus()))
        self.professor= create_ProfessorUniversitario_0()
        self.atividade = create_atividade( self.professor,
                                         self.diaaberto,
                                        self.espaco ,
                                        self.tema)
        self.horario= create_horario(inicio=time(14,0),fim=time(14,30))
        self.sessao= create_sessao(self.atividade, self.horario)

    def test_EliminarSessao_GET_semLogin(self):
        response = self.client.get(
            reverse('atividades:eliminarSessao', kwargs={'id': self.sessao.id}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_EliminarSessao_GET_naoProfessor(self):
        utilizadores = [create_Utilizador_0(),
                create_Colaborador_0(),
                create_Administrador_0(),
                create_Coordenador_0(),
                create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:eliminarSessao', kwargs={'id': self.sessao.id}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()
#
    def test_EliminarSessao_GET_DeOutroProfessor(self):
        self.client.force_login(create_ProfessorUniversitario_1())
        response = self.client.get(
            reverse('atividades:eliminarSessao', kwargs={'id': self.sessao.id}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para esta ação!')


class TestValidarAtividadeView(TestCase):
    
    def setUp(self):
        self.diaaberto= create_open_day()
        self.tema= create_tema()
        self.espaco= create_sala(create_edificio(create_campus()))
        self.coord= create_Coordenador_0()
        self.professor= create_ProfessorUniversitario_0()
        self.atividade = create_atividade( self.professor,
                                         self.diaaberto,
                                        self.espaco ,
                                        self.tema)

    def test_ValidarAtividade_GET_semLogin(self):
        response = self.client.get(
            reverse('atividades:validarAtividade', kwargs={'id': self.atividade.id, 'action': 1}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ValidarAtividade_GET_naoCoord(self):
        utilizadores = [create_Utilizador_0(),
                create_Colaborador_0(),
                create_Administrador_0(),
                create_ProfessorUniversitario_0(),
                create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:validarAtividade', kwargs={'id': self.atividade.id,  'action': 1}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()



class TestverResumoView(TestCase):
    
    def setUp(self):
        self.diaaberto= create_open_day()
        self.tema= create_tema()
        self.espaco= create_sala(create_edificio(create_campus()))
        self.professor= create_ProfessorUniversitario_0()
        self.atividade = create_atividade( self.professor,
                                         self.diaaberto,
                                        self.espaco ,
                                        self.tema)

    def test_verResumo_GET_semLogin(self):
        response = self.client.get(
            reverse('atividades:verResumo', kwargs={'id': self.atividade.id}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_verResumo_GET_naoProfessor(self):
        utilizadores = [create_Utilizador_0(),
                create_Colaborador_0(),
                create_Administrador_0(),
                create_Coordenador_0(),
                create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:verResumo', kwargs={'id': self.atividade.id}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()
#
    def test_verResumo_GET_DeOutroProfessor(self):
        self.client.force_login(create_ProfessorUniversitario_1())
        response = self.client.get(
            reverse('atividades:verResumo', kwargs={'id': self.atividade.id}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para esta ação!')


class TestconfirmarResumoView(TestCase):
    
    def setUp(self):
        self.diaaberto= create_open_day()
        self.tema= create_tema()
        self.espaco= create_sala(create_edificio(create_campus()))
        self.professor= create_ProfessorUniversitario_0()
        self.atividade = create_atividade( self.professor,
                                         self.diaaberto,
                                        self.espaco ,
                                        self.tema)

    def test_verResumo_GET_semLogin(self):
        response = self.client.get(
            reverse('atividades:confirmarResumo', kwargs={'id': self.atividade.id}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_confirmarResumo_GET_naoProfessor(self):
        utilizadores = [create_Utilizador_0(),
                create_Colaborador_0(),
                create_Administrador_0(),
                create_Coordenador_0(),
                create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('atividades:confirmarResumo', kwargs={'id': self.atividade.id}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()
#
    def test_confirmarResumo_GET_DeOutroProfessor(self):
        self.client.force_login(create_ProfessorUniversitario_1())
        response = self.client.get(
            reverse('atividades:confirmarResumo', kwargs={'id': self.atividade.id}))
        self.assertTemplateUsed(response, 'mensagem.html')
        self.assertEquals(response.context['tipo'], 'error')
        self.assertEquals(
            response.context['m'], 'Não tem permissões para esta ação!')


class TestAtribuicaoTransporteView(TestCase):
    

    @classmethod
    def setUp(self):
        self.admin = create_Administrador_0()
        self.diaaberto= create_open_day()
        self.transporteH = create_transporteH(self.diaaberto)

    def test_AtribuicaoTransporte_GET_semLogin(self):
        response = self.client.get(
            reverse('configuracao:atribuirTransporte', kwargs={'id': self.transporteH.id}))
        self.assertRedirects(response, reverse('utilizadores:login'))

    
    def test_AtribuicaoTransporte_GET_naoAdmin(self):
        utilizadores = [create_Utilizador_0(),
                create_Colaborador_0(),
                create_Participante_0(),
                create_Coordenador_0(),
                create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('configuracao:atribuirTransporte', kwargs={'id': self.transporteH.id}))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(
                response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()