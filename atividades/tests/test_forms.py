from django.test import TestCase
from configuracao.forms import *
from configuracao.models import *
from atividades.tests.test_models import create_material,create_atividade,create_tema
from utilizadores.tests.test_models import create_Coordenador_0, create_ProfessorUniversitario_0
from configuracao.tests.test_models import create_campus, create_dep, create_edificio, create_horario, create_menu, create_open_day, create_sala, create_transporteH, create_transporteU, create_uo

from datetime import date,time
from atividades.forms import AtividadeForm, MateriaisForm


class TestForms(TestCase):

    def setUp(self):
        self.tema=create_tema()
        self.professor= create_ProfessorUniversitario_0()
        self.espaco= create_sala(create_edificio(create_campus()))
        self.diaaberto= create_open_day()
        self.atividade=create_atividade(self.professor, self.diaaberto, self.espaco,self.tema)
        self.material=create_material(self.atividade)
        


    def test_AtividadeForm(self):
        form = AtividadeForm(data={
            'nome': 'Java',
            'tipo': 'Palestra',
            'descricao': 'Apreendendo Java',
            'publicoalvo': 'Economia',
            'nrcolaboradoresnecessario': 0,
            'participantesmaximo': 30,
            'duracaoesperada': 25,
            'tema': self.tema.id,
        })
        self.assertTrue(form.is_valid())

        form = AtividadeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),8)


    def test_AtividadeForm_1(self):
        form = AtividadeForm(data={
            'nome': 'Phyton',
            'tipo': 'Palestra',
            'descricao': 'Apreendendo Phyton',
            'publicoalvo': 'Economia',
            'nrcolaboradoresnecessario':1,
            'participantesmaximo': 35,
            'duracaoesperada': 25,
            'tema': self.tema.id,
        })
        self.assertTrue(form.is_valid())

        form = AtividadeForm(data={
            'nome': 'Phyton',
            'tipo': 'Palestra',
            'descricao': 'Apreendendo Phyton'})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),5)


    def test_MateriaisForm(self):
        form = MateriaisForm(data={
            'nomematerial': 'Ratos'
        })
        self.assertTrue(form.is_valid())

