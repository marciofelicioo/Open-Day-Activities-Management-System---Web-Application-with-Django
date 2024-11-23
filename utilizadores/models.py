from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from atividades import models as amodels
from colaboradores.models import ColaboradorHorario,PreferenciaAtividade,Preferencia
from coordenadores import models as coordmodels
from django.db.models import Q
from datetime import datetime,timedelta
class Utilizador(User):
    contacto = PhoneNumberField(max_length=20, blank=False, null=False)
    valido = models.CharField(max_length=255, blank=False, null=False)

    def getProfiles(self):
        type = ''
        if Administrador.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Administrador')
        if Participante.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Participante')
        if ProfessorUniversitario.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='ProfessorUniversitario')
        if Coordenador.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Coordenador')
        if Colaborador.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Colaborador')
        return type

    def concat(self, type, string):
        if type == '':
            type = string
        else:
            type += ', '+string
        return type

    @property
    def firstProfile(self):
        return self.getProfiles().split(' ')[0]

    def getUser(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name = "Coordenador").exists():
            result = Coordenador.objects.get(id=self.id)
        elif user.groups.filter(name = "Administrador").exists():
            result = Administrador.objects.get(id=self.id)
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            result = ProfessorUniversitario.objects.get(id=self.id)
        elif user.groups.filter(name = "Colaborador").exists():
            result = Colaborador.objects.get(id=self.id)
        elif user.groups.filter(name = "Participante").exists():
            result = Participante.objects.get(id=self.id)
        else:
            result = None
        return result   


    def getProfile(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name = "Coordenador").exists():
            result = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            result = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            result = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            result = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            result = "Participante"
        else:
            result = None
        return result 

    def emailValidoUO(self,uo):
        user = User.objects.get(email=self.email)
        if user.groups.filter(name = "Coordenador").exists():
            utilizador = Coordenador.objects.get(email=self.email)
        elif user.groups.filter(name = "Administrador").exists():
            return True
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            utilizador = ProfessorUniversitario.objects.get(email=self.email)
        elif user.groups.filter(name = "Colaborador").exists():
            utilizador = Colaborador.objects.get(email=self.email)
        else:
            return False
        if utilizador.faculdade == uo:
            return True
        else:
            return False   

    def emailValidoParticipante(self):
        user = User.objects.get(email=self.email)
        if user.groups.filter(name = "Administrador").exists():
            return True
        else:
            return False    
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    class Meta:
        db_table = 'Utilizador'


class Administrador(Utilizador):
    gabinete = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'Administrador'


class Participante(Utilizador):
    class Meta:
        db_table = 'Participante'


class ProfessorUniversitario(Utilizador):
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=False, null=False)

    faculdade = models.ForeignKey(
        'configuracao.Unidadeorganica', models.CASCADE)

    departamento = models.ForeignKey(
        'configuracao.Departamento', models.CASCADE)

    def __str__(self):
        return str(self.gabinete) + ' ' + str(self.faculdade) + ' ' + str(self.departamento)
    class Meta:
        db_table = 'ProfessorUniversitario'


class Coordenador(Utilizador):
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=False, null=False)

    faculdade = models.ForeignKey(
        'configuracao.Unidadeorganica', models.CASCADE, db_column='FaculdadeID')

    departamento = models.ForeignKey(
        'configuracao.Departamento', models.CASCADE, db_column='DepartamentoID')

    class Meta:
        db_table = 'Coordenador'

    def __str__(self):
        return self.first_name


class Colaborador(Utilizador):
    curso = models.ForeignKey(
        'configuracao.Curso', models.CASCADE)

    faculdade = models.ForeignKey(
        'configuracao.Unidadeorganica', models.CASCADE)

    departamento = models.ForeignKey(
        'configuracao.Departamento', models.CASCADE)

    class Meta:
        db_table = 'Colaborador'

    @staticmethod
    def get_free_colabs(coord,dia,horario,tipo,sessao=None):
        free_colabs=[]
        colabs = Colaborador.objects.filter(faculdade = coord.faculdade,utilizador_ptr_id__valido=True)
        free = True
        for colab in colabs: 
            tarefas = coordmodels.Tarefa.objects.filter(colab = colab.id,horario=horario,dia=dia)

            if tarefas.exists():
                continue

            if not ColaboradorHorario.objects.filter(colab=colab.id).exists():
                continue

            elif sessao is not None and (Preferencia.objects.filter(colab = colab.id, tipoTarefa='tarefaAuxiliar').exists() or not Preferencia.objects.filter(colab = colab.id).exists()):
                s = amodels.Sessao.objects.get(id=int(sessao))
                inicio = s.horarioid.inicio
                fim = s.horarioid.fim
                
                if not ColaboradorHorario.objects.filter(colab = colab.id,dia=dia)\
                    .filter(inicio__lte=horario,fim__gte=horario).exists(): 
                    continue

                if coordmodels.Tarefa.objects.filter(colab = colab.id,dia=dia,horario__gt=inicio).filter(horario__lt=fim).exists(): 
                    continue
                if coordmodels.TarefaAuxiliar.objects.filter(tarefaid__colab = colab.id,tarefaid__dia=dia,sessao__horarioid__inicio__lt=inicio,sessao__horarioid__fim__gt=inicio).exists():
                    continue
                if PreferenciaAtividade.objects.filter(preferencia__colab=colab.id).exists() and not PreferenciaAtividade.objects.filter(preferencia__colab=colab.id,atividade = s.atividadeid.id).exists():
                    continue

                tarefas = coordmodels.Tarefa.objects.filter(colab = colab.id,dia=dia)

                for t in tarefas:
                    hinicio = datetime.strptime(str(inicio),'%H:%M:%S') 
                    hfim =   datetime.strptime(str(fim),'%H:%M:%S')  
                    if t.tipo != 'tarefaAuxiliar' and (datetime.strptime(str(t.horario),'%H:%M:%S') - hinicio >  timedelta(hours=0,minutes=15,seconds=0) or hfim - datetime.strptime(str(t.horario),'%H:%M:%S') < timedelta(days=-1,hours=23,minutes=45)) :
                        free=False     
                if free == True:
                    free_colabs.append(colab)
            elif sessao is None:
                
                if not Preferencia.objects.filter(colab = colab.id, tipoTarefa=tipo).exists():
                    continue
                
                free=True
                tarefas = coordmodels.Tarefa.objects.filter(colab = colab.id,dia=dia)

                for t in tarefas:
                    if len(horario) == 5:
                        h = datetime.strptime(horario,'%H:%M')
                    if len(horario)==8:
                        h = datetime.strptime(horario,'%H:%M:%S')
                    if datetime.strptime(str(t.horario),'%H:%M:%S') - h >  timedelta(days=-1,hours=23,minutes=45) and h - datetime.strptime(str(t.horario),'%H:%M:%S') <  timedelta(minutes=15):
                        free=False     
                if coordmodels.TarefaAuxiliar.objects.filter(tarefaid__colab = colab.id,tarefaid__dia=dia)\
                    .filter(sessao__horarioid__inicio__lte=horario,sessao__horarioid__fim__gte=horario).exists(): 
                    continue
                if not ColaboradorHorario.objects.filter(colab = colab.id,dia=dia)\
                    .filter(inicio__lte=horario,fim__gte=horario).exists(): 
                    continue
                if free == True:
                    free_colabs.append(colab)
        return free_colabs



    def get_horarios_disponiveis(self):
        return ColaboradorHorario.objects.filter(colab=self.id)

    def get_preferencia_atividade(self):
        horarios = self.get_horarios_disponiveis()
        atividades = []
        for horario in horarios:
            sessoes= amodels.Sessao.objects.filter(horarioid__fim__gte=horario.inicio,horarioid__fim__lte=horario.fim,atividadeid__estado="Aceite",atividadeid__professoruniversitarioutilizadorid__faculdade=self.faculdade, dia=horario.dia)
        
        for sessao in sessoes:
            atividades.append(sessao.atividadeid)
        atividades = list(dict.fromkeys(atividades))
        return list_to_queryset(amodels.Atividade,atividades)

    def get_atividades_escolhidas(self):
        return PreferenciaAtividade.objects.filter(preferencia__colab=self)    

    def get_atividades_escolhidas_tabela(self):
        atividades = []
        for escolha in self.get_atividades_escolhidas():
            atividades.append(escolha.atividade)
        atividades = list(dict.fromkeys(atividades))
        return list_to_queryset(amodels.Atividade,atividades)

    def get_tarefas(self, dia, inicio, fim):
        if len(coordmodels.Tarefa.objects.filter(colab=self, horario__gte = inicio, horario__lte = fim, dia = dia))>0:
            return True
        elif len(coordmodels.TarefaAuxiliar.objects.filter(tarefaid__colab=self, sessao__horarioid__gte = inicio, sessao__horarioid__lte = fim, sessao__dia = dia))>0:     
            return True
        else:
            return False    

def list_to_queryset(model, data):
    from django.db.models.base import ModelBase
    if not isinstance(model, ModelBase):
        raise ValueError(
            "%s must be Model" % model
        )
    if not isinstance(data, list):
        raise ValueError(
            "%s must be List Object" % data
        )
    pk_list = [obj.pk for obj in data]
    return model.objects.filter(pk__in=pk_list)