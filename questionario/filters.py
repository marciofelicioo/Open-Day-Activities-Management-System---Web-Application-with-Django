import django_filters
from .models import Questionario, Estado
from django.db.models import Q

def filter_by_estado(queryset, name, value):
    return queryset.filter(estado__estado=value)
        
class QuestionarioFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(method='filter_titulo')
    estado = django_filters.ChoiceFilter(choices=Estado.ESTADO_CHOICES, method=filter_by_estado)

    def filter_titulo(self, queryset, name, value):
        for term in value.split():
            queryset = queryset.filter(Q(titulo__icontains=term))
        return queryset

    class Meta:
        model = Questionario
        fields = ['titulo', 'estado']
