from django.test import TestCase
from configuracao.forms import *
from configuracao.models import *
from configuracao.tests.test_models import create_open_day, create_campus, create_edificio, create_transporteH, create_transporteU, create_horario, create_menu
from datetime import date,time


class TestForms(TestCase):

    def setUp(self):
        self.horarioAlmoco = create_horario(inicio=time(12,0),fim=time(14,0))
        self.diaaberto = create_open_day()
        self.campus = create_campus()
        self.edificio = create_edificio(self.campus)
        self.transporteH = create_transporteH(self.diaaberto)
        self.transporte = self.transporteH.transporte
        self.transporteU = create_transporteU(self.transporte)
        self.menu = create_menu(
            campus=self.campus,
            horario=self.horarioAlmoco,
            diaaberto=self.diaaberto
        )
        
    def tearDown(self):
        self.menu.delete()
        self.horarioAlmoco.delete()
        self.diaaberto.delete()
        self.edificio.delete()
        self.campus.delete()
        self.transporteH.delete()
        self.transporteU.delete()
        self.transporte.delete()


    def test_TemaForm(self):
        form = TemaForm(data={
            'tema': 'Informatica'
        })

        self.assertTrue(form.is_valid())

        #invalid

        form = TemaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)

    def test_EdificioForm(self):
        
        formEdificio = EdificioForm(data={
            'nome': 'C1',
            'campus': self.campus,
            'image': 'bruv.png'
        })

        self.assertTrue(formEdificio.is_valid())

        #invalid

        formEdificio = EdificioForm(data={
            'nome': 'C1',
            'campus': self.campus.nome,
            'image': 'bruv.png'
        })

        self.assertEquals(len(formEdificio.errors),1)
        formEdificio = EdificioForm(data={})
        self.assertEquals(len(formEdificio.errors),2)

    def test_EspacoForm(self):
        edificio = self.edificio

        form = EspacoForm(data={
            'nome': '2.13',
            'andar': '1',
            'descricao': 'Sala',
        })
        form.instance.edificio = edificio
        self.assertTrue(form.is_valid())

    def test_TransportForm(self):
        form = transporteForm(data={
            'dia': '1970-01-01',
            'identificador': '01-00',
        })
        self.assertTrue(form.is_valid())

        #invalid

        form = transporteForm(data={
            'dia': '2200-01-01',
            'identificador': '01-00',
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),1)

        form = transporteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)

    def test_transporteUniversitarioForm(self):
        form = transporteUniversitarioForm(data={
            'capacidade': 1
        })
        self.assertTrue(form.is_valid())

    def test_menuForm(self):
        form = menuForm(data={
            'diaaberto': Diaaberto.current().id,
            'campus': self.campus.id,
            'dia': date(1970,1,1)
        })
        self.assertTrue(form.is_valid())

        #invalid

        form = menuForm(data={
           'diaaberto': None,
           'campus': None,
           'dia': None
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),4)  #4 para o horario que e dado automaticamente
    
