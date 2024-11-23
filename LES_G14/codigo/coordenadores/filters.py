import django_filters
from django.db.models import Exists, OuterRef
import datetime
from coordenadores.models import Tarefa
from configuracao.models import *

from django.forms.widgets import TextInput, CheckboxSelectMultiple

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

def get_sub_tarefa(queryset, name, value):
    tarefa =[]
    for t in queryset:
        if t.tipo in value:
            tarefa.append(t)
    return list_to_queryset(model=Tarefa,data=tarefa)

class TarefaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name="nome", lookup_expr='icontains')
    estado = django_filters.MultipleChoiceFilter(field_name='estado', choices=[('naoAtribuida','Não Atribuida'),('Concluida','Concluída'),
        ('Cancelada','Cancelada'),('Iniciada','Iniciada'),('naoConcluida','Não Concluída')], widget=CheckboxSelectMultiple())
    tipo = django_filters.MultipleChoiceFilter(field_name='tipo', choices=[('tarefaAuxiliar','Auxiliar'),('tarefaAcompanhar','Acompanhar'),
        ('tarefaOutra','Outra')], widget=CheckboxSelectMultiple(),method=get_sub_tarefa)
    dia = django_filters.DateFilter(label="Dia")
    colab = django_filters.NumberFilter(label="colab",field_name="colab__utilizador_ptr_id")
    class Meta:
        model = Tarefa
        fields = '__all__'

