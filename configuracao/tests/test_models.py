from django.test import TestCase
from django.test import SimpleTestCase
from configuracao.models import *
from datetime import datetime,date, time
import pytz

def create_open_day():
    return Diaaberto.objects.create(
        precoalunos = 2,
        precoprofessores = 2,
        enderecopaginaweb = 'web.com',
        descricao = 'Dia Aberto',
        emaildiaaberto = 'web@web.com',
        ano = datetime.now().year,
        datadiaabertoinicio = datetime(1970,1,1,9,30,tzinfo=pytz.UTC),
        datadiaabertofim = datetime(2040,1,2,9,30,tzinfo=pytz.UTC),
        datainscricaoatividadesinicio = datetime(1970,1,1,9,30,tzinfo=pytz.UTC),
        datainscricaoatividadesfim = datetime(2040,1,2,9,30,tzinfo=pytz.UTC),
        datapropostasatividadesincio = datetime(1970,1,1,9,30,tzinfo=pytz.UTC),
        dataporpostaatividadesfim = datetime(2040,1,2,9,30,tzinfo=pytz.UTC),
        administradorutilizadorid = None,
        escalasessoes = '00:30',
    )

def create_campus():
    return Campus.objects.create(nome='Penha')

def create_uo(campus):
    return Unidadeorganica.objects.create(
        nome = 'Faculdade de Ciencias e Tecnologias',
        sigla = 'FCT',
        campusid = campus
        )

def create_dep(uo):
    return Departamento.objects.create(
        nome = 'Departamento de Engenharia Informatica e Eletronica',
        sigla = 'DEEI',
        unidadeorganicaid = uo
    )

def create_curso(uo):
    return Curso.objects.create(
        nome = 'Licensiatura Engenharia Informatica',
        sigla = 'LEI',
        unidadeorganicaid = uo
    )

def create_horario(inicio=time(11,0),fim=time(11,30)):
    return Horario.objects.create(
        inicio=inicio,
        fim=fim
    )

def create_menu(campus,horario,diaaberto):
    return Menu.objects.create(
        horarioid = horario,
        campus = campus,
        diaaberto = diaaberto,
        dia = date(1970,1,1)
    )

def create_prato(menu):
    return Prato.objects.create(
        prato = 'Feijoada',
        tipo = 'Carne',
        nrpratosdisponiveis = 20,
        menuid=menu
    )

def create_edificio(campus):
    return Edificio.objects.create(
        nome = 'C1',
        campus = campus,
        image = 'images/edifi/gambelas.jpg'
    )

def create_sala(edificio):
    return Espaco.objects.create(
        nome = '2.13',
        edificio = edificio,
        andar = '0',
        descricao = 'Uma sala normal'
    )

def create_transporteH(diaaberto):
    transporte =  Transporte.objects.create(
        identificador = '01-00',
        diaaberto = diaaberto,
        dia = date(1970,1,1)
    )
    return  Transportehorario.objects.create(
        origem = 'Penha',
        chegada = 'Terminal',
        horaPartida = time(11,0),
        horaChegada = time(11,30),
        transporte = transporte
    )
def create_transporteU(transporte):
    return Transporteuniversitario.objects.create(
        transporte = transporte,
        capacidade = 20
    )


class TestModels(TestCase):

    def setUp(self):
        self.diaaberto = create_open_day()
        self.campus = create_campus()
        self.uo = create_uo(self.campus)
        self.dep = create_dep(self.uo)
        self.curso = create_curso(self.uo)
        self.lunchTime = create_horario(inicio=time(12,0),fim=time(14,0))
        self.menu = create_menu(
            campus=self.campus,
            horario=self.lunchTime,
            diaaberto=self.diaaberto
        )
        self.prato = create_prato(menu=self.menu)
        self.edificio = create_edificio(self.campus)
        self.espaco = create_sala(self.edificio)
        self.transporteH = create_transporteH(self.diaaberto)
        self.transporte = self.transporteH.transporte
        self.transporteU = create_transporteU(self.transporte)

    def tearDown(self):
        self.diaaberto.delete()
        self.dep.delete()
        self.curso.delete()
        self.uo.delete()
        self.prato.delete()
        self.menu.delete()
        self.lunchTime.delete()
        self.espaco.delete()
        self.edificio.delete()
        self.campus.delete()
        self.transporte.delete()
        

    def test_dia_aberto(self):
        diaaberto = self.diaaberto
        self.assertEquals(Diaaberto().singup_open(),True)
        self.assertEquals(Diaaberto().submit_activities_open(), True)
        #fields
        self.assertEquals(Diaaberto.current().id,diaaberto.id)
        self.assertEquals(str(diaaberto),str(datetime.now().year))
        self.assertEquals(diaaberto.precoalunos,2)
        self.assertEquals(diaaberto.precoprofessores, 2)
        self.assertEquals(diaaberto.enderecopaginaweb, 'web.com')
        self.assertEquals(diaaberto.descricao, 'Dia Aberto')
        self.assertEquals(diaaberto.emaildiaaberto, 'web@web.com')
        self.assertEquals(diaaberto.datadiaabertoinicio, datetime(1970,1,1,9,30,tzinfo=pytz.UTC),)
        self.assertEquals(diaaberto.datadiaabertofim, datetime(2040,1,2,9,30,tzinfo=pytz.UTC))
        self.assertEquals(diaaberto.datainscricaoatividadesinicio, datetime(1970,1,1,9,30,tzinfo=pytz.UTC),)
        self.assertEquals(diaaberto.datainscricaoatividadesfim, datetime(2040,1,2,9,30,tzinfo=pytz.UTC))
        self.assertEquals(diaaberto.datapropostasatividadesincio, datetime(1970,1,1,9,30,tzinfo=pytz.UTC),)
        self.assertEquals(diaaberto.dataporpostaatividadesfim, datetime(2040,1,2,9,30,tzinfo=pytz.UTC))
        self.assertEquals(diaaberto.administradorutilizadorid, None)
        self.assertEquals(diaaberto.escalasessoes, '00:30')

    def test_campus(self):
        campus = self.campus
        self.assertEquals(campus.nome, 'Penha')
        self.assertEquals(campus.nome, str(campus))

    def test_uo(self):
        uo = self.uo
        self.assertEquals(str(uo),uo.nome)
        self.assertEquals(uo.nome,'Faculdade de Ciencias e Tecnologias')
        self.assertEquals(uo.sigla,'FCT')
        self.assertEquals(uo.campusid,self.campus)

        #methods
        
        self.assertEqual(uo.dep_().first().id, \
            Departamento.objects.filter(unidadeorganicaid=self.uo).first().id)

    def test_dep(self):
        dep = self.dep

        self.assertEquals(dep.nome,'Departamento de Engenharia Informatica e Eletronica')
        self.assertEquals(str(dep),dep.nome)
        self.assertEquals(dep.sigla,'DEEI')
        self.assertEquals(dep.unidadeorganicaid.id,self.uo.id)

    def test_curso(self):
        curso = self.curso

        self.assertEquals(curso.nome,'Licensiatura Engenharia Informatica')
        self.assertEquals(curso.sigla,'LEI')
        self.assertEquals(str(curso),curso.nome)
        self.assertEquals(curso.unidadeorganicaid.id,self.uo.id)   

    def test_horario(self):
        horario = self.lunchTime

        self.assertEquals(horario.inicio,time(12,0))
        self.assertEquals(horario.fim,time(14,0))
        self.assertEquals(str(horario), '12:00:00 até 14:00:00')

    def test_menu(self):
        menu = self.menu

        self.assertEquals(self.lunchTime, menu.horarioid)
        self.assertEquals(self.campus, menu.campus)
        self.assertEquals(self.diaaberto, menu.diaaberto)
        self.assertEquals(date(1970,1,1), menu.dia)

        # methods

        self.assertEquals(menu.pratos_().first().id, \
            Prato.objects.filter(menuid=menu).first().id)
    
    def test_prato(self):
        prato = self.prato

        self.assertEquals(prato.prato, str(prato))
        self.assertEquals(prato.tipo,'Carne')
        self.assertEquals(prato.nrpratosdisponiveis, 20)
        self.assertEquals(prato.menuid.id, self.menu.id)

    def test_edificio(self):
        edifi = self.edificio

        self.assertEquals(edifi.nome, 'C1')
        self.assertEquals(edifi.campus, self.campus)

        #methods

        self.assertEquals(str(edifi),"<a href='/configuracao/imagens/edificio/" + str(edifi.id) + "'>C1</a>")
        self.assertEquals(edifi.salas_().first().id, self.espaco.id)
        self.assertEquals(edifi.count_salas,1)

    def test_sala(self):
        sala = self.espaco

        self.assertEquals(sala.nome,'2.13')
        self.assertEquals(sala.edificio.id,self.edificio.id)
        self.assertEquals(sala.andar,'0')
        self.assertEquals(sala.descricao,'Uma sala normal')

    
    def test_transport(self):
        transport = self.transporte

        self.assertEquals(transport.identificador, '01-00')
        self.assertEquals(str(transport), '01-00')
        self.assertEquals(transport.diaaberto.id, self.diaaberto.id)
        self.assertEquals(transport.dia, date(1970,1,1))
        
    def test_transportH(self):
        transportH = self.transporteH

        self.assertEquals(transportH.origem,'Penha')
        self.assertEquals(transportH.chegada,'Terminal')
        self.assertEquals(transportH.horaPartida, time(11,0))
        self.assertEquals(transportH.horaChegada, time(11,30))
        self.assertEquals(transportH.transporte.id, self.transporte.id)

        # methods

        self.assertEquals(transportH.get_identifier, str(self.transporte))
        self.assertEquals(transportH.get_capacidade, self.transporteU.capacidade)
        self.assertEquals(transportH.get_trip_time, '11:00 - 11:30')
        self.assertEquals(transportH.trip(), 'Penha - Terminal')




#def create_transporteU(transporte):
#    return Transporteuniversitario.objects.create(
#        transporte = transporte,
#        capacidade = 20
#    )