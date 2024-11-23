from atividades.models import Atividade, Sessao, Roteiro
import django_filters
from django.db.models import Exists, OuterRef
from datetime import datetime
from django.forms.widgets import CheckboxSelectMultiple


def filter_sessoes(queryset, name, value):
    dia_vagas_de_ate = value.split('_')
    dia = dia_vagas_de_ate[0] if dia_vagas_de_ate[0] else datetime.date.today().strftime("%Y-%m-%d")
    vagas = dia_vagas_de_ate[1] if dia_vagas_de_ate[1] else 0
    de = dia_vagas_de_ate[2] if dia_vagas_de_ate[2] else '00:00'
    ate = dia_vagas_de_ate[3] if dia_vagas_de_ate[3] else '23:55'
    print(f"De: {de} | Até: {ate}")
    return queryset.filter(
        Exists(Sessao.objects.filter(
            atividadeid=OuterRef('id'),
            dia=dia,
            vagas__gte=vagas,
            horarioid__inicio__gte=de,
            horarioid__fim__lte=ate,
        ))
    )


class AtividadeFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    unidade_organica_id = django_filters.NumberFilter(
        field_name="professoruniversitarioutilizadorid__faculdade__id")
    departamento_id = django_filters.NumberFilter(
        field_name="professoruniversitarioutilizadorid__departamento__id")
    campus_id = django_filters.NumberFilter(
        field_name="espacoid__edificio__campus__id")
    sessoes = django_filters.CharFilter(method=filter_sessoes)
    
    class Meta:
        model = Atividade
        fields = '__all__'



class CoordAtividadesFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    departamento_id = django_filters.NumberFilter(
        field_name="professoruniversitarioutilizadorid__departamento__id")
    campus_id = django_filters.NumberFilter(
        field_name="espacoid__edificio__campus__id")
    sessoes = django_filters.CharFilter(method=filter_sessoes)
    estado = django_filters.MultipleChoiceFilter(field_name='estado', choices=[('Aceite','Aceite'),('Pendente','Pendente'),('Recusada','Recusada')], widget=CheckboxSelectMultiple())

    class Meta:
        model = Atividade
        fields = '__all__'

class ProfAtividadesFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    departamento_id = django_filters.NumberFilter(
        field_name="professoruniversitarioutilizadorid__departamento__id")
    campus_id = django_filters.NumberFilter(
        field_name="espacoid__edificio__campus__id")
    sessoes = django_filters.CharFilter(method=filter_sessoes)
    estado = django_filters.MultipleChoiceFilter(field_name='estado', choices=[('Aceite','Aceite'),('Pendente','Pendente'),('Recusada','Recusada')], widget=CheckboxSelectMultiple())

    class Meta:
        model = Atividade
        fields = '__all__'


class AdminAtividadesFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    departamento_id = django_filters.NumberFilter(
        field_name="professoruniversitarioutilizadorid__departamento__id")
    campus_id = django_filters.NumberFilter(
        field_name="espacoid__edificio__campus__id")
    sessoes = django_filters.CharFilter(method=filter_sessoes)
    estado = django_filters.MultipleChoiceFilter(field_name='estado', choices=[('Aceite','Aceite'),('Pendente','Pendente'),('Recusada','Recusada')], widget=CheckboxSelectMultiple())
    uo_id = django_filters.NumberFilter(field_name="professoruniversitarioutilizadorid__faculdade__id")

    class Meta:
        model = Atividade
        fields = '__all__'


class RoteiroFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name="nome", lookup_expr='icontains')
    ano = django_filters.ChoiceFilter(
        field_name="ano",
        label="Ano",
        method="filter_by_ano",
        choices=[],  # As opções serão preenchidas dinamicamente
    )

    def filter_by_ano(self, queryset, name, value):
        if value == 'Todos':
            return queryset  # Retorna todos os roteiros sem filtrar por ano
        return queryset.filter(ano=value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Preencha dinamicamente as opções para o campo de filtro de ano
        anos_distintos = Roteiro.objects.values_list('ano', flat=True).distinct()
        choices = [('Todos', 'Todos')]
        for ano in anos_distintos:
            choices.append((str(ano), str(ano)))
        self.filters['ano'].extra['choices'] = choices

    class Meta:
        model = Roteiro
        fields = ['nome', 'ano']
