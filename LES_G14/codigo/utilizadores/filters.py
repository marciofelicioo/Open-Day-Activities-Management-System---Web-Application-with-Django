import django_filters
from utilizadores.models import Utilizador
from django.db.models import Q

get_valido_choices = [
    ('True', 'Confirmado'),
    ('False', 'Por confirmar'),
    ('Rejeitado', 'Rejeitado'),
]


def filter_nome(queryset, name, value):
    for term in value.split():
        queryset = queryset.filter(Q(first_name__icontains=term)
                                   | Q(last_name__icontains=term))
    return queryset


class UtilizadoresFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(method=filter_nome)
    valido = django_filters.MultipleChoiceFilter(choices=get_valido_choices)

    class Meta:
        model = Utilizador
        fields = '__all__'
