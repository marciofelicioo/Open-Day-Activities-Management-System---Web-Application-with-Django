# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core import validators
from datetime import datetime,timedelta, timezone
import time
from time import mktime
from datetime import datetime,timedelta, timezone, time as datetime_time
from utilizadores.models import Coordenador
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.urls.base import reverse
from django.utils.html import escape
from django.core.exceptions import NON_FIELD_ERRORS
class Transporte(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    identificador = models.CharField(db_column='Identificador', max_length=32)
    diaaberto = models.ForeignKey(
        'Diaaberto', models.CASCADE, db_column='diaAberto')
    dia = models.DateField(db_column="Dia", blank=False, null=False)
    def __str__(self):
        return str(self.identificador)
    class Meta:
        db_table = 'Transporte'

class Transportehorario(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    choices = {
        ('Penha','Penha'),
        ('Terminal','Terminal'),
        ('Gambelas','Gambelas'),
    }
    origem = models.CharField(db_column='Origem', max_length=32, blank=True, null=False, choices=choices)
    # Field name made lowercase.
    chegada = models.CharField(db_column='Chegada', max_length=32, blank=True, null=False, choices=choices)
    # Field name made lowercase.

    horaPartida = models.TimeField(db_column="HoraPartida", blank=False, null=False)
    horaChegada = models.TimeField(db_column="HoraChegada", blank=False, null=False)

    transporte = models.ForeignKey(
        Transporte, models.CASCADE, db_column='Transporte')

    def __str__(self):
        return self.origem + " - " + self.chegada + ' Horas: ' + str(self.horaChegada) + ' - ' + str(self.horaPartida) + ' ' + str(self.transporte)
    @property
    def get_identifier(self):
        return self.transporte.identificador

    @property
    def get_capacidade(self):
        return Transporteuniversitario.objects.get(transporte=self.transporte).capacidade

    @property
    def get_trip_time(self):
        return datetime_time.strftime(self.horaPartida, "%H:%M") + ' - ' + datetime_time.strftime(self.horaChegada, "%H:%M")
    
    def trip(self):
        return str(self.origem) + ' - ' + str(self.chegada)
    class Meta:
        db_table = 'TransporteHorario'

class Transporteuniversitario(models.Model):
    # Field name made lowercase.
    transporte = models.OneToOneField(
        Transporte, models.CASCADE, db_column='Transporte', primary_key=True)
    # Field name made lowercase.
    capacidade = models.IntegerField(db_column='Capacidade')
    def __str__(self):
        return str(self.transporte.id) + ' ' + str(self.capacidade)
    class Meta:
        db_table = 'TransporteUniversitario'


class Diaaberto(models.Model):
    # Field name made lowercase.
    precoalunos = models.FloatField(db_column='PrecoAlunos')
    # Field name made lowercase.
    precoprofessores = models.FloatField(
        db_column='PrecoProfessores', blank=True, null=True)
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    enderecopaginaweb = models.CharField(
        db_column='EnderecoPaginaWeb', max_length=255)
    # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')
    # Field name made lowercase.
    emaildiaaberto = models.CharField(
        db_column='EmailDiaAberto', max_length=255)
    ano = models.IntegerField(db_column='Ano')  # Field name made lowercase.
    # Field name made lowercase.
    datadiaabertoinicio = models.DateTimeField(db_column='DataDiaAbertoInicio')
    # Field name made lowercase.
    datadiaabertofim = models.DateTimeField(db_column='DataDiaAbertoFim')
    # Field name made lowercase.
    datainscricaoatividadesinicio = models.DateTimeField(
        db_column='DataInscricaoAtividadesInicio')  
    # Field name made lowercase.
    datainscricaoatividadesfim = models.DateTimeField(
        db_column='DataInscricaoAtividadesFim')
    # Field name made lowercase.
    datapropostasatividadesincio = models.DateTimeField(
        db_column='DataPropostasAtividadesIncio')
    # Field name made lowercase.
    dataporpostaatividadesfim = models.DateTimeField(
        db_column='DataPorpostaAtividadesFim')
    # Field name made lowercase.
    administradorutilizadorid = models.ForeignKey(
        'utilizadores.Administrador', models.SET_NULL, db_column='AdministradorUtilizadorID',null=True)
    # Field name made lowercase.
    escalasessoes = models.TimeField(db_column='EscalaSessoes')

    def session_times(self):

        start_time  = self.datadiaabertoinicio.time()
        end_time = self.datadiaabertofim.time()
        start_time_as_seconds = (start_time.hour * 60 + start_time.minute) * 60
        end_time_as_seconds = (end_time.hour * 60 + end_time.minute) * 60
        time_lunch_end = 50400
        return [
            (time.strftime('%H:%M', time.gmtime(start_time_as_seconds + (n*self.escalasessoes.minute*60))))
                for n in range(int((43200 - start_time_as_seconds)/(self.escalasessoes.minute*60)))
        ] + [
            (time.strftime('%H:%M', time.gmtime(time_lunch_end + (n*self.escalasessoes.minute*60))))
                for n in range(int((end_time_as_seconds - time_lunch_end)/(self.escalasessoes.minute*60))+1)
        ]



    def days_as_dict(self):
        data_inicio = self.datadiaabertoinicio
        data_fim = self.datadiaabertofim
        total_dias= data_fim-data_inicio+timedelta(days=1)
        return [{
                    'key':	str( (data_inicio+timedelta(days=d)).date()),
                    'value':	str((data_inicio+timedelta(days=d)).date())
                } for d in range(total_dias.days)
            ]

    def days_as_tuples(self):
        data_inicio = self.datadiaabertoinicio
        data_fim = self.datadiaabertofim
        total_dias= data_fim-data_inicio+timedelta(days=1)
        return [(
                    str( (data_inicio+timedelta(days=d)).date()),
                    str((data_inicio+timedelta(days=d)).date())
                ) for d in range(total_dias.days)
            ]
    @staticmethod
    def current():
        now = datetime.now(timezone.utc)
        qs = Diaaberto.objects.filter(ano=now.year,datadiaabertofim__gte=now)
        if qs.exists():
            return qs.first()
        else: return None

    @staticmethod
    def singup_open():
        now = datetime.now(timezone.utc)
        current = Diaaberto.current()
        if current is not None:
            return current.datainscricaoatividadesinicio <= now and current.datainscricaoatividadesfim > now
        else: return False
    @staticmethod
    def submit_activities_open():
        now = datetime.now(timezone.utc)
        current = Diaaberto.current()
        if current is not None:
            return current.datapropostasatividadesincio <= now and current.dataporpostaatividadesfim > now
        else: return False

    def days_as_array(self):
        data_inicio = self.datadiaabertoinicio
        data_fim = self.datadiaabertofim
        total_dias= data_fim-data_inicio+timedelta(days=1)
        return [(
                    (data_inicio+timedelta(days=d)).date()
                )  for d in range(total_dias.days)
            ]
            
    def __str__(self):
        return str(self.ano)
    class Meta:
        db_table = 'DiaAberto'


class Menu(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    horarioid = models.ForeignKey(
        'Horario', models.CASCADE, db_column='HorarioID')
    campus = models.ForeignKey(
        'Campus', models.CASCADE, db_column='Campus')
    diaaberto = models.ForeignKey(
        'Diaaberto', models.CASCADE, db_column='diaAberto')
    dia = models.DateField(db_column='Dia')

    def pratos_(self):
        return Prato.objects.filter(menuid=self)

    def __str__(self):
        return str(self.campus.nome) + ' ' + str(self.diaaberto.ano)
    class Meta:
        db_table = 'Menu'
        unique_together = ['campus','diaaberto','dia']





class Prato(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    prato = models.CharField(db_column='Prato',max_length=255, blank=False, null=False)
    # Field name made lowercase.
    tipos = [
        ('Carne',"Carne"),
        ('Peixe','Peixe'),
        ('Vegetariano', 'Vegetariano'),
        ('Sobremesa', 'Sobremesa'),
    ]
    tipo = models.CharField(
        choices=tipos,db_column='Tipo', max_length=255, blank=False, null=False)
    # Field name made lowercase.
    nrpratosdisponiveis = models.IntegerField(db_column='NrPratosDisponiveis',blank=False, null=False)


    # Field name made lowercase.
    menuid = models.ForeignKey(Menu, models.CASCADE, db_column='MenuID')

    def __str__(self):
        return (self.prato)
    class Meta:
        db_table = 'Prato'


class Espaco(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=False)  # Field name made lowercase.
    edificio = models.ForeignKey('Edificio', models.CASCADE, db_column='Edificio', blank=True, null=False)  # Field name made lowercase.
    andar = models.CharField(db_column='Andar', max_length=255, blank=True, null=False)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null = True)  # Field name made lowercase.

    def __str__(self):
        if self.edificio.image:
            return mark_safe('<a href=\'' + reverse('configuracao:verEdificioImagem',kwargs={'id': self.edificio.id}) + '\'>' + escape(self.nome) + '</a>')
        else: return self.nome    

    class Meta:
        db_table = 'Espaco'


class Edificio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=64)  # Field name made lowercase.
    campus = models.ForeignKey('Campus', models.CASCADE, db_column='Campus', null=False)  # Field name made lowercase.
    image = models.ImageField(upload_to='images/edifi',db_column='image', blank=True, null=True)

    def espacos_(self):
        return Espaco.objects.filter(edificio=self)

    @property
    def count_salas(self):
        return Espaco.objects.filter(edificio=self).count()

    def salas_(self):
        return Espaco.objects.filter(edificio=self)

    def __str__(self):
        if self.image:
            return mark_safe('<a href=\'' + reverse('configuracao:verEdificioImagem',kwargs={'id': self.id}) + '\'>' + escape(self.nome) + '</a>')
        else: return self.nome
    class Meta:
        db_table = 'Edificio'


class Campus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.nome
    class Meta:
        db_table = 'Campus'


class Departamento(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    sigla = models.CharField(
        db_column='Sigla', max_length=32, blank=True, null=True)
    # Field name made lowercase.
    unidadeorganicaid = models.ForeignKey(
        'Unidadeorganica', models.CASCADE, db_column='UnidadeOrganicaID')


    class Meta:
        db_table = 'Departamento'

    def __str__(self):
        return str(self.nome)

class Sala(models.Model):
    # Field name made lowercase.
    espacoid = models.ForeignKey(
        'Espaco', models.CASCADE, db_column='EspacoID')
    # Field name made lowercase.
    espacoedificio = models.CharField(
        db_column='EspacoEdificio', max_length=255)

    class Meta:
        db_table = 'Sala'


class Idioma(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    diaabertoid = models.ForeignKey(
        Diaaberto, models.CASCADE, db_column='DiaAbertoID')
    # Field name made lowercase.
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    sigla = models.CharField(
        db_column='Sigla', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Idioma'


class Horario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    inicio = models.TimeField(db_column='Inicio')  # Field name made lowercase.
    fim = models.TimeField(db_column='Fim')  # Field name made lowercase.
    
    def __str__(self):
        return str(self.inicio) + ' até ' + str(self.fim)

    class Meta:
        db_table = 'Horario'


        
class Unidadeorganica(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    sigla = models.CharField(db_column='Sigla', max_length=255)  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.CASCADE, db_column='CampusID')  # Field name made lowercase.

    class Meta:
        db_table = 'UnidadeOrganica'

    def __str__(self):
        return self.nome

    def dep_(self):
        return Departamento.objects.filter(unidadeorganicaid=self)

    def coord_(self):
        return Coordenador.objects.filter(faculdade_id=self.id).first()
class Curso(models.Model):

    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(
        db_column='Nome', max_length=255, blank=True, null=True)

    sigla = models.CharField(
        db_column='Sigla', max_length=32, blank=True, null=True)\
    
    unidadeorganicaid = models.ForeignKey(
        'Unidadeorganica', models.CASCADE, db_column='Unidadeorganica')

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'Curso'

