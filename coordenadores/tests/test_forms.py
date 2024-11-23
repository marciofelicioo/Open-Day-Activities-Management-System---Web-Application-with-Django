from django.test import TestCase
from django.test import SimpleTestCase
from coordenadores.models import *
from datetime import datetime,date, time
import pytz
from atividades.tests.test_models import create_sessao, create_atividade, create_horario, create_tema
from inscricoes.tests.test_models import create_Inscricao_2
from utilizadores.tests.test_models import create_Colaborador_0, create_Coordenador_0, create_ProfessorUniversitario_0
from configuracao.tests.test_models import create_open_day, create_campus, create_sala, create_edificio


class TestForms(TestCase):

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


    def test_AuxiliarForm(self):
        form = AuxiliarForm(data={
            'atividade': self.auxiliar.atividade, 
            'dia': self.tarefa_0,
            'sessao': self.auxiliar.sessao,
            'colab': self.tarefa_0.colab
        })

        self.assertTrue(form.is_valid())
    
    def test_AcompanharForm(self):
        form = AcompanharForm(data={
            'grupo': self.acompanhar.inscricao,
            'dia':self.tarefa_1.dia,
            'horario':self.tarefa_1.horario,
            'origem':self.acompanhar.origem,
            'destino':self.acompanhar.destino
        })

        self.assertTrue(form.is_valid())
    
    def test_OutraForm(self):
        form = OutraForm(data={
            'dia': self.tarefa_2.dia,
            'horario': self.tarefa_2.horario,
            'descricao':self.outra
        })

        self.assertTrue(form.is_valid())

