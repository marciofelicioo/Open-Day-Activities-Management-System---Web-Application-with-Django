# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse
import html
from coordenadores.models import TarefaAuxiliar
from datetime import date
from coordenadores.models import Coordenador
from configuracao.models import Espaco, Horario

class Anfiteatro(models.Model):
    # Field name made lowercase.
    espacoid = models.OneToOneField(
        'configuracao.Espaco', models.CASCADE, db_column='EspacoID', primary_key=True)
    # Field name made lowercase.
    espacoedificio = models.CharField(
        db_column='EspacoEdificio', max_length=255)

    class Meta:
        db_table = 'Anfiteatro'


class Arlivre(models.Model):
    # Field name made lowercase.
    espacoid = models.OneToOneField(
        'configuracao.Espaco', models.CASCADE, db_column='EspacoID', primary_key=True)
    # Field name made lowercase.
    espacoedificio = models.CharField(
        db_column='EspacoEdificio', max_length=255)

    class Meta:
        db_table = 'ArLivre'


class Tema(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    tema = models.CharField(db_column='Tema', max_length=64)
    
    @property
    def num_activities(self):
        return Atividade.objects.filter(tema=self).count()

    def __str__(self):
        return str(self.tema)

    class Meta:
        db_table = 'Tema'


class Atividade(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)
    # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')
    publicosalvo = (("Ciencias e Tecnologia", "Ciências e Tecnologia"),
                    ("Linguas e Humanidades", "Linguas e Humanidades"), ("Economia", "Economia"))
    # Field name made lowercase.
    publicoalvo = models.CharField(
        db_column='Publicoalvo', max_length=255, choices=publicosalvo, default='')
    # Field name made lowercase.
    nrcolaboradoresnecessario = models.IntegerField(
        db_column='nrColaboradoresNecessario', default=0)
    tipos = (("Atividade Laboratorial", "Atividade Laboratorial"),
             ("Tertulia", "Tertulia"), ("Palestra", "Palestra"), ("Misto", "Misto"))
    # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=64,
                            choices=tipos, default='Palestra')
    # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=64)
    professoruniversitarioutilizadorid = models.ForeignKey(
        'utilizadores.ProfessorUniversitario', models.CASCADE, db_column='ProfessorUniversitarioUtilizadorID')  # Field name made lowercase.
    # Field name made lowercase.
    datasubmissao = models.DateTimeField(
        db_column='dataSubmissao', auto_now_add=True)
    # Field name made lowercase.
    dataalteracao = models.DateTimeField(
        db_column='dataAlteracao', auto_now=True)
    # Field name made lowercase.
    duracaoesperada = models.IntegerField(db_column='duracaoEsperada')
    # Field name made lowercase.
    participantesmaximo = models.IntegerField(db_column='participantesMaximo')
    # Field name made lowercase.
    diaabertoid = models.ForeignKey(
        'configuracao.Diaaberto', models.CASCADE, db_column='diaAbertoID')
    # Field name made lowercase.
    espacoid = models.ForeignKey(
        'configuracao.Espaco', models.CASCADE, db_column='EspacoID')
    # Field name made lowercase.
    tema = models.ForeignKey('Tema', models.CASCADE,
                             db_column='Tema', blank=False, null=False)

    class Meta:
        db_table = 'Atividade'

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Atividade._meta.fields]

    def get_dias(self):
        sessoes = Sessao.objects.filter(atividadeid=self)
        dias = [sessao.dia for sessao in sessoes]
        return [{'key': str(dia), 'value': dia} for dia in set(dias)]

    def get_dias_list(self):
        sessoes = Sessao.objects.filter(atividadeid=self)
        dias = [sessao.dia for sessao in sessoes]
        return [dia for dia in set(dias)]

    def get_campus_str(self):
        return self.espacoid.edificio.campus.nome

    def get_sala_str(self, request=None):
        if request is None:
            return mark_safe('<a href="' + reverse('configuracao:verEdificioImagem', kwargs={'id': self.espacoid.edificio.id}) + '" target="_blank">' + html.escape(self.espacoid.edificio.nome) + ' ' + html.escape(self.espacoid.nome) + ' - ' + html.escape(self.espacoid.edificio.campus.nome) + '</a>')
        img_full_url = request.build_absolute_uri(reverse(
            'configuracao:verEdificioImagem', kwargs={'id': self.espacoid.edificio.id}))
        return mark_safe('<a href="' + img_full_url + '" target="_blank">' + html.escape(self.espacoid.edificio.nome) + ' ' + html.escape(self.espacoid.nome) + ' - ' + html.escape(self.espacoid.edificio.campus.nome) + '</a>')

    def get_uo(self):
        return self.professoruniversitarioutilizadorid.faculdade

    def get_departamento(self):
        return self.professoruniversitarioutilizadorid.departamento

    def get_coord(self):
        return self.professoruniversitarioutilizadorid.faculdade.coord_()

    def get_material(self):
        return Materiais.objects.filter(atividadeid=self).first()

    def get_tema(self):
        return self.tema.tema

    def eq(self, other):
        return self.nome == other.nome and \
            self.descricao == other.descricao and \
            self.publicoalvo == other.publicoalvo and \
            self.nrcolaboradoresnecessario == other.nrcolaboradoresnecessario and \
            self.tipo == other.tipo and \
            self.professoruniversitarioutilizadorid == other.professoruniversitarioutilizadorid and \
            self.datasubmissao == other.datasubmissao and \
            self.duracaoesperada == other.duracaoesperada and \
            self.participantesmaximo == other.participantesmaximo and \
            self.diaabertoid == other.diaabertoid and \
            self.espacoid == other.espacoid and \
            self.tema == other.tema

    def ne(self, other):
        return False if self.eq(other) else True

    @staticmethod
    def tarefas_get_atividades(fac):
        atividades=[]
        print(fac)
        sessoes = Sessao.objects.filter(atividadeid__estado='Aceite',atividadeid__nrcolaboradoresnecessario__gt=0,atividadeid__professoruniversitarioutilizadorid__faculdade__id=fac)
        for sessao in sessoes:
            tarefa = TarefaAuxiliar.objects.filter(sessao=sessao.id)
            if tarefa.count() < sessao.atividadeid.nrcolaboradoresnecessario:
                if sessao.atividadeid not in atividades:
                    atividades.append(sessao.atividadeid)   
        return atividades
    
    def numero_de_sessoes(self):
        return self.sessao_set.count()
        
class Materiais(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    atividadeid = models.ForeignKey(
        Atividade, models.CASCADE, db_column='AtividadeID')
    nomematerial = models.CharField(
        db_column='nome', max_length=255, blank=True, null=True)

    def eq(self, other):
        return self.atividadeid == other.atividadeid and \
            self.nomematerial == other.nomematerial

    def ne(self, other):
        return False if self.eq(other) else True

    class Meta:
        db_table = 'Materiais'    

class Roteiro(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=255)
    descricao = models.TextField(db_column='Descricao')
    ano = models.IntegerField()
    coord = models.ForeignKey('utilizadores.Coordenador', models.CASCADE, db_column='CoordenadorUtilizadorID',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    diaabertoid = models.ForeignKey(
        'configuracao.Diaaberto', models.CASCADE, db_column='diaAbertoID')

    def __str__(self):
        return self.nome
    
    def numero_de_atividades(self):
        return self.atividaderoteiro_set.count()
    
    def numero_de_sessoes(self):
        return self.sessao_set.count()
    
    class Meta:
        db_table = 'Roteiro'   


class AtividadeRoteiro(models.Model):
    roteiro = models.ForeignKey(Roteiro, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    duracao = models.IntegerField(db_column='duracao', null=True, default=None)

    class Meta:
        db_table = 'AtividadeRoteiro' 


class Sessao(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    ninscritos = models.IntegerField(db_column='NInscritos')
    # Field name made lowercase.
    vagas = models.IntegerField(db_column='Vagas')
    # Field name made lowercase.
    atividadeid = models.ForeignKey(
        Atividade, models.CASCADE, db_column='AtividadeID', null=True, default=None)
    # Field name made lowercase.
    roteiroid = models.ForeignKey(
        Roteiro, models.CASCADE, db_column='RoteiroID', null=True, default=None)
    # Field name made lowercase.
    dia = models.DateField(db_column='Dia', blank=True, null=True)
    # Field name made lowercase.
    horarioid = models.ForeignKey(
        'configuracao.Horario', models.DO_NOTHING, db_column='HorarioID')
    nr_presentes = models.IntegerField(default=0)

    def get_colaboradores(self):
        tarefas = TarefaAuxiliar.objects.filter(sessao = self).exclude(tarefaid__estado="naoAtribuida")
        return [tarefa.tarefaid.colab for tarefa in tarefas]

    def timeRange_(self, seperator=' até '):
        return self.horarioid.inicio.strftime('%H:%M') + str(seperator) + self.horarioid.fim.strftime('%H:%M')


    
    class Meta:
        db_table = 'Sessao'

    @staticmethod
    def tarefas_get_sessoes(atividade,dia):
        tarefa_sessoes=[]
        sessoes = Sessao.objects.filter(atividadeid=atividade,dia=dia)
        #print(sessao.dia)
        for sessao in sessoes:
            tarefa = TarefaAuxiliar.objects.filter(sessao=sessao.id)
            if tarefa.count() < sessao.atividadeid.nrcolaboradoresnecessario:
                if sessao not in tarefa_sessoes:
                    tarefa_sessoes.append(sessao)        
        return tarefa_sessoes                