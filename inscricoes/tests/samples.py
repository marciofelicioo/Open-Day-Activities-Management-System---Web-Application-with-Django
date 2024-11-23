from configuracao.models import Campus, Diaaberto, Edificio, Espaco, Horario, Transporte, Transportehorario, Transporteuniversitario
from datetime import datetime, date, time
import pytz
from atividades.models import Atividade, Sessao, Tema
from utilizadores.tests.test_models import create_Administrador_0, create_ProfessorUniversitario_0


def create_Diaaberto_0():
    return Diaaberto.objects.get_or_create(
        precoalunos=2,
        precoprofessores=2,
        enderecopaginaweb='web.com',
        descricao='Dia Aberto',
        emaildiaaberto='web@web.com',
        ano=datetime.now().year,
        datadiaabertoinicio=datetime(1970, 1, 1, 9, 30, tzinfo=pytz.UTC),
        datadiaabertofim=datetime(2040, 1, 2, 9, 30, tzinfo=pytz.UTC),
        datainscricaoatividadesinicio=datetime(
            1970, 1, 1, 9, 30, tzinfo=pytz.UTC),
        datainscricaoatividadesfim=datetime(
            2040, 1, 2, 9, 30, tzinfo=pytz.UTC),
        datapropostasatividadesincio=datetime(
            1970, 1, 1, 9, 30, tzinfo=pytz.UTC),
        dataporpostaatividadesfim=datetime(2040, 1, 2, 9, 30, tzinfo=pytz.UTC),
        administradorutilizadorid=create_Administrador_0(),
        escalasessoes='00:30',
    )[0]


def create_Campus_0():
    return Campus.objects.get_or_create(nome='Penha')[0]


def create_Edificio_0():
    return Edificio.objects.get_or_create(
        nome='C1',
        campus=create_Campus_0(),
        image='images/edifi/gambelas.jpg',
    )[0]


def create_Espaco_0():
    return Espaco.objects.get_or_create(
        nome='2.13',
        edificio=create_Edificio_0(),
        andar='0',
        descricao='Uma sala normal',
    )[0]


def create_Tema_0():
    return Tema.objects.get_or_create(tema="Farmacia")[0]


def create_Atividade_0():
    return Atividade.objects.get_or_create(
        nome="Java",
        descricao="Aprendendo Java",
        publicoalvo="Ciencias e Tecnologia",
        nrcolaboradoresnecessario=0,
        tipo='Palestra',
        estado='Aceite',
        professoruniversitarioutilizadorid=create_ProfessorUniversitario_0(),
        duracaoesperada=30,
        participantesmaximo=30,
        diaabertoid=create_Diaaberto_0(),
        espacoid=create_Espaco_0(),
        tema=create_Tema_0(),
    )[0]


def create_Horario_0():
    return Horario.objects.get_or_create(
        inicio=time(11, 0),
        fim=time(11, 30),
    )[0]


def create_Horario_1():
    return Horario.objects.get_or_create(
        inicio=time(11, 10),
        fim=time(12, 0),
    )[0]


def create_Horario_2():
    return Horario.objects.get_or_create(
        inicio=time(8, 0),
        fim=time(9, 30),
    )[0]


def create_Sessao_0():
    return Sessao.objects.get_or_create(
        ninscritos=0,
        vagas=35,
        atividadeid=create_Atividade_0(),
        dia=date(2021, 5, 29),
        horarioid=create_Horario_0(),
    )[0]


def create_Sessao_1():
    return Sessao.objects.get_or_create(
        ninscritos=0,
        vagas=25,
        atividadeid=create_Atividade_0(),
        dia=date(2021, 5, 29),
        horarioid=create_Horario_1(),
    )[0]


def create_Sessao_2():
    return Sessao.objects.get_or_create(
        ninscritos=0,
        vagas=30,
        atividadeid=create_Atividade_0(),
        dia=date(2021, 5, 29),
        horarioid=create_Horario_2(),
    )[0]


def create_Transporte_0():
    return Transporte.objects.get_or_create(
        identificador='01-00',
        diaaberto=create_Diaaberto_0(),
        dia=date(1970, 1, 1),
    )[0]


def create_Transportehorario_0():
    return Transportehorario.objects.get_or_create(
        origem='Penha',
        chegada='Terminal',
        horaPartida=time(11, 0),
        horaChegada=time(11, 30),
        transporte=create_Transporte_0(),
    )[0]
