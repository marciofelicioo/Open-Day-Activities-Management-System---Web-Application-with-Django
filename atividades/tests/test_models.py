from django.test import TestCase
from django.test import SimpleTestCase
from atividades.models import *
from datetime import datetime,date, time
import pytz
from utilizadores.tests.test_models import create_Coordenador_0, create_ProfessorUniversitario_0
from configuracao.tests.test_models import create_campus, create_dep, create_edificio, create_horario, create_menu, create_open_day, create_sala, create_transporteH, create_transporteU, create_uo


def create_material(atividade):
    return Materiais.objects.create(
        atividadeid= atividade,
        nomematerial= "PC"
    )


def create_material_1(atividade):
    return Materiais.objects.create(
        atividadeid= atividade,
        nomematerial= "Rato"
    )




def create_tema():
    return Tema.objects.create(tema= "Farmacia")

def create_tema_1():
    return Tema.objects.create(tema= "Informatica")



def create_atividade(professor, diaaberto, espaco,tema):
    return Atividade.objects.create(
    nome= "Java",
    descricao= "Aprendendo Java",
    publicoalvo= "Ciencias e Tecnologia",
    nrcolaboradoresnecessario= 0,
    tipo= 'Palestra',
    estado= 'Aceite',
    professoruniversitarioutilizadorid= professor,
    duracaoesperada= 30,
    participantesmaximo= 30,
    diaabertoid= diaaberto,
    espacoid= espaco,
    tema= tema
)


def create_atividade_1(professor, diaaberto, espaco,tema):
    return Atividade.objects.create(
    nome= "Phyton",
    descricao= "Aprendendo Phyton",
    publicoalvo= "Ciencias e Tecnologia",
    nrcolaboradoresnecessario= 1,
    tipo= 'Palestra',
    estado= 'Pendente',
    professoruniversitarioutilizadorid= professor,
    duracaoesperada= 30,
    participantesmaximo= 20,
    diaabertoid= diaaberto,
    espacoid= espaco,
    tema= tema
)




def create_sessao(atividade, horario):
    return Sessao.objects.create(
        ninscritos= 0,
        vagas = 30,
        atividadeid= atividade,
        dia= date(1970,1,1),
        horarioid= horario
    )


class TestModels(TestCase):
    def setUp(self):
        self.diaaberto= create_open_day()
        self.tema= create_tema()
        self.tema_1= create_tema_1()
        self.espaco= create_sala(create_edificio(create_campus()))
        self.professor= create_ProfessorUniversitario_0()
        self.atividade = create_atividade( self.professor,
                                         self.diaaberto,
                                        self.espaco ,
                                        self.tema)
        self.atividade_1 = create_atividade_1( self.professor,
                                         self.diaaberto,
                                        self.espaco ,
                                        self.tema)
        self.horario=create_horario(inicio=time(14,0),fim=time(14,30))
        self.sessao= create_sessao(
            self.atividade,
            self.horario
        )
        self.material= create_material(self.atividade)
        self.material_1= create_material_1(self.atividade)

    
    
    def test_atividades(self):
        atividade = self.atividade
        self.assertEquals(atividade.nome,"Java")
        self.assertEquals(atividade.descricao, "Aprendendo Java")
        self.assertEquals(atividade.publicoalvo, "Ciencias e Tecnologia")
        self.assertEquals(atividade.nrcolaboradoresnecessario, 0)
        self.assertEquals(atividade.tipo, 'Palestra')
        self.assertEquals(atividade.estado, 'Aceite')
        self.assertEquals(atividade.professoruniversitarioutilizadorid, self.professor)
        self.assertEquals(atividade.duracaoesperada,30)
        self.assertEquals(atividade.participantesmaximo, 30)
        self.assertEquals(atividade.diaabertoid, self.diaaberto)
        self.assertEquals(atividade.espacoid, self.espaco)
        self.assertEquals(atividade.tema, self.tema)


    def test_atividades_1(self):
        atividade = self.atividade_1
        self.assertEquals(atividade.nome,"Phyton")
        self.assertEquals(atividade.descricao, "Aprendendo Phyton")
        self.assertEquals(atividade.publicoalvo, "Ciencias e Tecnologia")
        self.assertEquals(atividade.nrcolaboradoresnecessario, 1)
        self.assertEquals(atividade.tipo, 'Palestra')
        self.assertEquals(atividade.estado, 'Pendente')
        self.assertEquals(atividade.professoruniversitarioutilizadorid, self.professor)
        self.assertEquals(atividade.duracaoesperada,30)
        self.assertEquals(atividade.participantesmaximo, 20)
        self.assertEquals(atividade.diaabertoid, self.diaaberto)
        self.assertEquals(atividade.espacoid, self.espaco)
        self.assertEquals(atividade.tema, self.tema)


    def test_tema(self):
        tema= self.tema
        self.assertEquals(tema.tema, "Farmacia")
    
    def test_tema_1(self):
        tema= self.tema_1
        self.assertEquals(tema.tema, "Informatica")


    def test_sessao(self):
        sessao= self.sessao
        self.assertEquals(sessao.ninscritos, 0)
        self.assertEquals(sessao.vagas,30)
        self.assertEquals(sessao.atividadeid, self.atividade)
        self.assertEquals(sessao.dia, date(1970,1,1) )
        self.assertEquals(sessao.horarioid, self.horario)

    def test_material(self):
        material= self.material
        self.assertEquals(material.atividadeid, self.atividade)
        self.assertEquals(material.nomematerial, "PC")

    def test_material_1(self):
        material= self.material_1
        self.assertEquals(material.atividadeid, self.atividade)
        self.assertEquals(material.nomematerial, "Rato")