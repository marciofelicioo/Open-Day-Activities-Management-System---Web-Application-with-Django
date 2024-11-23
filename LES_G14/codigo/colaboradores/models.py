
from django.db import models
#from .views import get_dia_choices


class ColaboradorHorario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    colab = models.ForeignKey('utilizadores.Colaborador', models.CASCADE, db_column='ColaboradorUtilizadorID',null=True,blank=True) 
    dia = models.DateField()
    inicio = models.TimeField(db_column='Inicio') 
    fim = models.TimeField(db_column='Fim') 


    class Meta:
        db_table = 'ColaboradorHorario'

    def check_horario(self, dia, inicio, fim):
        return self.colab.get_tarefas(dia, inicio, fim)
        

class Preferencia(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    colab = models.ForeignKey('utilizadores.Colaborador', models.CASCADE, db_column='ColaboradorUtilizadorID',null=True,blank=True) 
    tipoTarefa = models.CharField(db_column='Tipo', max_length=64) 
    class Meta:
        db_table = 'Preferencia'


class PreferenciaAtividade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    preferencia = models.ForeignKey(Preferencia, models.CASCADE, db_column='PreferenciaID',null=True,blank=True) 
    atividade = models.ForeignKey('atividades.Atividade', models.CASCADE, db_column='Atividade',null=True,blank=True) 

    class Meta:
        db_table = 'PreferenciaAtividade'        