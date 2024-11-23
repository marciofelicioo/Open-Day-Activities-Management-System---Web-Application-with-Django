from django.test import TestCase
from utilizadores.models import *
from configuracao.models import *
from coordenadores.models import *
from atividades.models import *
from datetime import datetime,date, time
from utilizadores.tests.test_models import create_Colaborador_0,create_Colaborador_1 ,create_Coordenador_0, create_ProfessorUniversitario_0
from inscricoes.tests.test_models import create_Inscricao_2
import pytz



def create_Campus_1():
    return Campus.objects.get_or_create(nome='Gambelas')[0]


def create_Edificio_1():
    return Edificio.objects.get_or_create(
        nome = 'C2',
        campus = create_Campus_1(),
        image = 'images/edifi/gambelas.jpg'
    )[0]


def create_Sala_0():
    return Espaco.objects.get_or_create(
        nome = '2.15',
        edificio = create_Edificio_0(),
        andar = '0',
        descricao = 'Uma sala normal'
    )[0]



def create_Open_Day_0():
    return Diaaberto.objects.get_or_create(
        precoalunos = 2,
        precoprofessores = 2,
        enderecopaginaweb = 'web.com',
        descricao = 'Dia Aberto',
        emaildiaaberto = 'web@web.com',
        ano = datetime.now().year,
        datadiaabertoinicio = datetime(1975,1,1,9,30,tzinfo=pytz.UTC),
        datadiaabertofim = datetime(2045,1,2,9,30,tzinfo=pytz.UTC),
        datainscricaoatividadesinicio = datetime(1978,1,1,9,30,tzinfo=pytz.UTC),
        datainscricaoatividadesfim = datetime(2047,1,2,9,30,tzinfo=pytz.UTC),
        datapropostasatividadesincio = datetime(1975,1,1,9,30,tzinfo=pytz.UTC),
        dataporpostaatividadesfim = datetime(2048,1,2,9,30,tzinfo=pytz.UTC),
        administradorutilizadorid = None,
        escalasessoes = '00:30',
    )[0]


def create_Tema_0():
    return Tema.objects.get_or_create(tema= "Engenharia")[0]


def create_Horario_0():
    return Horario.objects.get_or_create(
        inicio=time(12,0),
        fim=time(14,30)
    )[0]


def create_Atividade_0():
    return Atividade.objects.get_or_create(
        nome= "Java2",
        descricao= "Aprendendo Java",
        publicoalvo= "Ciencias e Tecnologia",
        nrcolaboradoresnecessario= 0,
        tipo= 'Palestra',
        estado= 'Aceite',
        professoruniversitarioutilizadorid= create_ProfessorUniversitario_0(),
        duracaoesperada= 30,
        participantesmaximo= 30,
        diaabertoid= create_Open_Day_0(),
        espacoid= create_Sala_0(),
        tema= create_Tema_0()
)[0]

def create_Sessao_0():
    return Sessao.objects.get_or_create(
        ninscritos= 0,
        vagas = 30,
        atividadeid= create_Atividade_0(),
        dia= date(1975,1,1),
        horarioid= create_Horario_0()
    )[0]

def create_Tarefa_0():
    return Tarefa.objects.get_or_create(
        nome = 'Auxiliar na atividade Java',
        estado = 'naoConcluida',
        coord = create_Coordenador_0(),
        colab = create_Colaborador_0(),
        dia = date(2021,4,10),
        horario= time(14,20),
    )[0]

def create_Tarefa_1():
    return Tarefa.objects.get_or_create(
        nome = 'Acompanhar o grupo 3',
        estado = 'Concluida',
        coord = create_Coordenador_0(),
        colab = create_Colaborador_0(),
        dia = date(2021,4,11),
        horario= time(16,10),
    )[0]

def create_Tarefa_2():
    return Tarefa.objects.get_or_create(
        nome = 'Fechar a sala 1.63...',
        estado = 'naoAtribuida',
        coord = create_Coordenador_0(),
        colab = None,
        dia = date(2021,4,12),
        horario= time(10,45),
    )[0]


def create_Tarefa_Auxiliar():
    return TarefaAuxiliar.objects.get_or_create(
        tarefaid = create_Tarefa_0(),
        sessao = create_Sessao_0()
    )[0]

def create_Tarefa_Acompanhar():
    return TarefaAcompanhar.objects.get_or_create(
        tarefaid = create_Tarefa_1(),
        inscricao = create_Inscricao_2(),
        origem = 'Check in',
        destino = '1.63',
    )[0]

def create_Tarefa_Outra():
    return TarefaOutra.objects.get_or_create(
        tarefaid = create_Tarefa_2(),
        descricao = 'Fechar a sala 1.63 do Edificio 1'
    )[0]


    
class TestColaboradoresTarefasModels(TestCase):
    ''' Testes para a componente colaboradores - Tarefas '''
    
    def setUp(self):
        self.coord = create_Coordenador_0()
        self.colab0 = create_Colaborador_0()
        self.colab1 = create_Colaborador_1()
        self.tarefa0 = create_Tarefa_0()
        self.tarefa1 = create_Tarefa_1()
        self.tarefa2 = create_Tarefa_2()
    
    
    def test_iniciar_tarefa(self):
        ''' Teste que verifica se uma tarefa é iniciada corretamente '''
        tarefa0 = self.tarefa0
        tarefa1 = self.tarefa1
        tarefa0.estado="Iniciada"
        tarefa1.estado="Iniciada"
        tarefa0.save()
        tarefa1.save()
        self.assertEqual(tarefa0.estado, "Iniciada")
        self.assertEqual(tarefa1.estado, "Iniciada")



    def test_concluir_tarefa(self):
        ''' Teste que verifica se uma tarefa é concluída corretamente '''
        tarefa0 = self.tarefa0
        tarefa1 = self.tarefa1
        tarefa0.estado="Concluida"
        tarefa1.estado="Concluida"
        tarefa0.save()
        tarefa1.save()
        self.assertEqual(tarefa0.estado, "Concluida")
        self.assertEqual(tarefa1.estado, "Concluida")



    def test_cancelar_tarefa(self):
        ''' Teste que verifica se uma tarefa é cancelada corretamente '''
        tarefa0 = self.tarefa0
        tarefa1 = self.tarefa1
        tarefa0.estado="Cancelada"
        tarefa1.estado="Cancelada"
        tarefa0.save()
        tarefa1.save()
        self.assertEqual(tarefa0.estado, "Cancelada")
        self.assertEqual(tarefa1.estado, "Cancelada")


    
    def test_tarefa_atribuida(self):
        ''' Teste que verifica se uma tarefa é atribuída corretamente '''
        tarefa0 = self.tarefa0
        tarefa1 = self.tarefa1
        c0=create_Colaborador_1()
        c1=create_Colaborador_1()
        tarefa0.colab=c0
        tarefa1.colab=c1
        tarefa0.save()
        tarefa1.save()
        self.assertEquals(tarefa0.colab.id,self.colab1.id)    
        self.assertEquals(tarefa1.colab.id,self.colab1.id)



    def test_tarefa_nao_atribuida(self):
        ''' Teste que verifica se uma tarefa deixa de estar atribuída corretamente '''
        tarefa = self.tarefa2
        self.assertEquals(tarefa.colab,None)

    


    def test_coordenador_tarefa(self):
        ''' Teste que verifica se um coordenador de uma determinada tarefa é o correto '''
        tarefa0 = self.tarefa0
        coordenador = tarefa0.coord
        self.assertEqual(tarefa0.coord.id, coordenador.id)

