# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime, date,timezone,time
from django.db.models.signals import pre_delete, post_delete
from configuracao.models import *
class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    estado = models.CharField(max_length=64)
    coord = models.ForeignKey('utilizadores.Coordenador', models.CASCADE, db_column='CoordenadorUtilizadorID',null=True)  # Field name made lowercase.
    colab = models.ForeignKey('utilizadores.Colaborador', models.SET_NULL, db_column='ColaboradorUtilizadorID',null=True,blank=True)  # Field name made lowercase.
    created_at = models.DateTimeField(auto_now_add=True)
    dia = models.DateField()
    horario = models.TimeField(blank=False, null=False)
    diaaberto = models.ForeignKey('configuracao.Diaaberto', models.CASCADE, db_column='Diaaberto')  # Field name made lowercase.

    def save(self,*args, **kwargs):
        self.diaaberto = Diaaberto.current()
        super(Tarefa, self).save(*args, **kwargs)

    @property
    def tipo(self):
        if TarefaAcompanhar.objects.filter(tarefaid=self.id):
           return "tarefaAcompanhar"
        elif TarefaAuxiliar.objects.filter(tarefaid=self.id):
            return "tarefaAuxiliar"
        elif TarefaOutra.objects.filter(tarefaid=self.id): 
            return "tarefaOutra" 
        return None 


    @property
    def tipo_frontend(self):
        if TarefaAcompanhar.objects.filter(tarefaid=self.id):
           return "Acompanhar"
        elif TarefaAuxiliar.objects.filter(tarefaid=self.id):
            return "Auxiliar"
        elif TarefaOutra.objects.filter(tarefaid=self.id): 
            return "Outra"  

    class Meta:
        db_table = 'Tarefa'
        ordering = ['dia']

    @property
    def eliminar(self):
        if (self.estado == 'Iniciada' and self.dia < date.today()) or\
            self.estado == 'naoConcluida' or\
            self.estado == 'Concluida' or\
            self.estado == 'Cancelada' or\
            self.estado == 'naoAtribuida':
            return True
        return False
        
        
    def getDescription(self):
        if self.tipo == "tarefaAcompanhar":
            tmp = TarefaAcompanhar.objects.get(tarefaid=self.id)
        elif self.tipo == "tarefaAuxiliar":   
            tmp = TarefaAuxiliar.objects.get(tarefaid=self.id)
        else:
            tmp = TarefaOutra.objects.get(tarefaid=self.id)
        return tmp.getDescription()

    def get_tarefa_especifica(self):
        if self.tipo == "tarefaAcompanhar":
            tmp = TarefaAcompanhar.objects.get(tarefaid=self.id)
        elif self.tipo == "tarefaAuxiliar":   
            tmp = TarefaAuxiliar.objects.get(tarefaid=self.id)
        else:
            tmp = TarefaOutra.objects.get(tarefaid=self.id)
        return tmp

    def get_outra_descricao(self):
        tarefa = TarefaOutra.objects.get(tarefaid=self.id)
        if tarefa is not None:
            return tarefa.descricao
        else:
            return ""



class TarefaAcompanhar(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    origem = models.CharField(max_length=255, db_column='origem', blank=False, null=False)
    destino = models.CharField(max_length=255, db_column='destino', blank=False, null=False) 
    inscricao = models.ForeignKey('inscricoes.Inscricao', models.CASCADE, db_column='inscricao')
    
    class Meta:
        db_table = 'TarefaAcompanhar'

    def getDescription(self):
        if self.origem != 'Check in':
            local = Espaco.objects.get(id=int(self.origem))
            origem = local.nome
            extra = " da sala "+origem+", no edifício "+ local.edificio.nome
        else:
            extra = " do "+self.origem
        destino = Espaco.objects.get(id=int(self.destino))
        msg = self.tarefaid.nome+extra+" á sala "+destino.nome+", no edifício "+ destino.edificio.nome+", no dia "+self.tarefaid.dia.strftime('%d/%m/%y')\
        +" às "+self.tarefaid.horario.strftime('%H horas e %M minutos')+"."
        return msg


 
    def get_origem(self):
        if self.origem != 'Check in':
            local = Espaco.objects.get(id=int(self.origem))
            origem = local.nome
            return "Sala "+origem+", edifício "+ local.edificio.nome
        else:
            return self.origem

    def get_destino(self):
        destino = Espaco.objects.get(id=int(self.destino))          
        return destino.nome+", edifício "+ destino.edificio.nome


class TarefaAuxiliar(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    sessao = models.ForeignKey('atividades.Sessao', models.CASCADE, db_column='sessao')

    class Meta:
        db_table = 'TarefaAuxiliar'
    
    def getDescription(self):
        msg = self.tarefaid.nome+"."
        return msg

def remove_parent(sender,instance, **kwargs):
    tarefaid = instance.tarefaid
    sender.objects.raw('DELETE FROM '+str(sender.__name__) +' WHERE tarefaid ='+str(tarefaid.id))
    Tarefa.objects.get(id=tarefaid.id).delete()

post_delete.connect(remove_parent,sender=TarefaAuxiliar)
post_delete.connect(remove_parent,sender=TarefaAcompanhar)

class TarefaOutra(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    descricao = models.TextField(db_column='descricao', blank=False, null=False)

    class Meta:
        db_table = 'TarefaOutra'

    def getDescription(self):
        msg = self.descricao
        return msg
