from inscricoes.tests.test_models import create_Inscricao_0
from django.test import TestCase
from django.urls import reverse
from utilizadores.tests.test_models import create_Administrador_0, create_Colaborador_0, create_Coordenador_0, create_Participante_0, create_ProfessorUniversitario_0, create_Utilizador_0

class TestConsultarTarefasView(TestCase):
    """ Teste suite da view "consultar_tarefas" da app "colaboradores" """

    @classmethod
    def setUpTestData(cls):
        cls.colaborador = create_Colaborador_0()

    def test_ConsultarTarefas_GET_semLogin(self):
        """ Teste de método GET sem login """
        response = self.client.get(
            reverse('colaboradores:consultar-tarefas'))
        self.assertRedirects(response, reverse('utilizadores:login'))

    def test_ConsultarTarefas_GET_naoColaborador(self):
        """ Teste de método GET sem ser colaborador """
        utilizadores = [create_Utilizador_0(),
                        create_ProfessorUniversitario_0(),
                        create_Administrador_0(),
                        create_Coordenador_0(),
                        create_Participante_0(),]
        for utilizador in utilizadores:
            self.client.force_login(utilizador)
            response = self.client.get(
                reverse('colaboradores:consultar-tarefas'))
            self.assertTemplateUsed(response, 'mensagem.html')
            self.assertEquals(response.context['tipo'], 'error')
            self.assertEquals(response.context['m'], 'Não tem permissões para aceder a esta página!')
            self.client.logout()

    def test_ConsultarTarefas_GET_ok(self):
        """ Teste de método GET sucesso """
        self.client.force_login(self.colaborador)
        response = self.client.get(
            reverse('colaboradores:consultar-tarefas'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'colaboradores/consultar_tarefas.html')
        self.assertIsNotNone(response.context['table'])