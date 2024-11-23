from django.test import TestCase
from django.test import SimpleTestCase
from coordenadores.models import *
from datetime import datetime,date, time
import pytz
from atividades.tests.test_models import create_sessao, create_atividade, create_horario, create_tema
from inscricoes.tests.test_models import create_Inscricao_2
from utilizadores.tests.test_models import create_Colaborador_0, create_Coordenador_0, create_ProfessorUniversitario_0
from configuracao.tests.test_models import create_open_day, create_campus, create_sala, create_edificio
from coordenadores.forms import *


def create_tarefa_0(coord,colab):
    return Tarefa.objects.create(
        nome = 'Auxiliar na atividade Java',
        estado = 'naoConcluida',
        coord = coord,
        colab = colab,
        dia = date(2021,4,10),
        horario= time(14,20),
    )

def create_tarefa_1(coord,colab):
    return Tarefa.objects.create(
        nome = 'Acompanhar o grupo 3',
        estado = 'Concluida',
        coord = coord,
        colab = colab,
        dia = date(2021,4,11),
        horario= time(16,10),
    )

def create_tarefa_2(coord,colab):
    return Tarefa.objects.create(
        nome = 'Fechar a sala 1.63...',
        estado = 'naoAtribuida',
        coord = coord,
        colab = colab,
        dia = date(2021,4,12),
        horario= time(10,45),
    )

def create_tarefa_auxiliar(tarefa,sessao):
    return TarefaAuxiliar.objects.create(
        tarefaid = tarefa,
        sessao = sessao
    )

def create_tarefa_acompanhar(tarefa,inscricao):
    return TarefaAcompanhar.objects.create(
        tarefaid = tarefa,
        inscricao = inscricao,
        origem = 'Check in',
        destino = '1.63',
    )

def create_tarefa_outra(tarefa):
    return TarefaOutra.objects.create(
        tarefaid = tarefa,
        descricao = 'Fechar a sala 1.63 do Edificio 1'
    )

class TestModels(TestCase):

    def setUp(self):
        #configuraçao
        self.diaaberto = create_open_day()
        self.campus = create_campus()
        self.edificio = create_edificio(self.campus)
        self.espaco = create_sala(self.edificio)

        #utilizadores
        self.coord = create_Coordenador_0()
        self.colab = create_Colaborador_0()
        self.professor= create_ProfessorUniversitario_0()

        #atividades
        self.tema= create_tema()
        self.atividade = create_atividade(self.professor,self.diaaberto,self.espaco,self.tema)
        self.horario=create_horario(inicio=time(14,0),fim=time(14,30))
        self.sessao= create_sessao(self.atividade,self.horario)

        #inscricoes
        self.inscricao = create_Inscricao_2()

        #coordenadores
        self.tarefa_0 = create_tarefa_0(self.coord,self.colab)
        self.tarefa_1 = create_tarefa_1(self.coord,self.colab)
        self.tarefa_2 = create_tarefa_2(self.coord,None)
        self.auxiliar = create_tarefa_auxiliar(self.tarefa_0,self.sessao)
        self.acompanhar = create_tarefa_acompanhar(self.tarefa_1,self.inscricao)
        self.outra = create_tarefa_outra(self.tarefa_2)


    def test_tarefa_0(self):
        tarefa = self.tarefa_0
        self.assertEquals(tarefa.nome,'Auxiliar na atividade Java')
        self.assertEquals(tarefa.estado,'naoConcluida') 
        self.assertEquals(tarefa.coord.id,self.coord.id)
        self.assertEquals(tarefa.colab.id,self.colab.id)
        self.assertEquals(tarefa.dia,date(2021,4,10))
        self.assertEquals(tarefa.horario,time(14,20))
        self.assertEquals(tarefa.tipo,'tarefaAuxiliar')
        self.assertEquals(tarefa.tipo_frontend,'Auxiliar')

        self.assertEquals(tarefa.getDescription(),'Auxiliar na atividade Java.')

    def test_tarefa_1(self):
        tarefa = self.tarefa_1
        self.assertEquals(tarefa.nome,'Acompanhar o grupo 3')
        self.assertEquals(tarefa.estado,'Concluida') 
        self.assertEquals(tarefa.coord.id,self.coord.id)
        self.assertEquals(tarefa.colab.id,self.colab.id)
        self.assertEquals(tarefa.dia,date(2021,4,11))
        self.assertEquals(tarefa.horario,time(16,10))
        self.assertEquals(tarefa.tipo,'tarefaAcompanhar')
        self.assertEquals(tarefa.tipo_frontend,'Acompanhar')

        #self.assertEquals(tarefa.getDescription(),'Acompanhar o grupo 3 da sala , no idifício ')
    
    def test_tarefa_2(self):
        tarefa = self.tarefa_2
        self.assertEquals(tarefa.nome,'Fechar a sala 1.63...')
        self.assertEquals(tarefa.estado,'naoAtribuida') 
        self.assertEquals(tarefa.coord.id,self.coord.id)
        self.assertEquals(tarefa.colab,None)
        self.assertEquals(tarefa.dia,date(2021,4,12))
        self.assertEquals(tarefa.horario,time(10,45))
        self.assertEquals(tarefa.tipo,'tarefaOutra')
        self.assertEquals(tarefa.tipo_frontend,'Outra')

        self.assertEquals(tarefa.getDescription(),'Fechar a sala 1.63 do Edificio 1')
    
    def test_auxiliar(self):
        tarefa = self.auxiliar
        self.assertEquals(tarefa.tarefaid.id,self.tarefa_0.id) 
        self.assertEquals(tarefa.sessao.id,self.sessao.id) 

    def test_auxiliar(self):
        tarefa = self.acompanhar
        self.assertEquals(tarefa.tarefaid.id,self.tarefa_1.id) 
        self.assertEquals(tarefa.inscricao.id,self.inscricao.id)

    def test_auxiliar(self):
        tarefa = self.outra
        self.assertEquals(tarefa.tarefaid.id,self.tarefa_2.id) 
        self.assertEquals(tarefa.descricao,'Fechar a sala 1.63 do Edificio 1')
  