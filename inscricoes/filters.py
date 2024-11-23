import django_filters
from .models import *
from django.db.models import Exists, OuterRef
from configuracao.models import Diaaberto


def filter_departamento(queryset, name, value):
    return queryset.filter(
        Exists(Inscricaosessao.objects.filter(
            inscricao=OuterRef('pk'),
            sessao__atividadeid__professoruniversitarioutilizadorid__departamento_id=value
        ))
    )


def filter_nome_responsavel(queryset, name, value):
    return queryset.filter(
        Exists(Responsavel.objects.filter(
            inscricao=OuterRef('pk'),
            nome__icontains=value
        ))
    )


class InscricaoFilter(django_filters.FilterSet):
    areacientifica = django_filters.CharFilter(
        field_name="areacientifica", lookup_expr='icontains')
    min_alunos = django_filters.NumberFilter(
        field_name="nalunos", lookup_expr='gte')
    max_alunos = django_filters.NumberFilter(
        field_name="nalunos", lookup_expr='lte')
    departamento = django_filters.CharFilter(method=filter_departamento)
    participante = django_filters.CharFilter(
        method=filter_nome_responsavel)

    class Meta:
        model = Inscricao
        fields = '__all__'

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.form.initial['diaaberto'] = Diaaberto.objects.filter(
            ano__lte=datetime.now().year).order_by('-ano').first().id

class PresencasFilter(django_filters.FilterSet):
    ano = django_filters.NumberFilter(method='filter_by_ano')
    dia = django_filters.DateFilter(field_name='data_evento', lookup_expr='exact')

    def filter_by_ano(self, queryset, name, value):
        return queryset.filter(data_evento__year=value)

    class Meta:
        model = Inscricao
        fields = ['ano', 'dia']