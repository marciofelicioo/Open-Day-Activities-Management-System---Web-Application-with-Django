import django_filters
from django.db.models import Exists, OuterRef
import datetime
from configuracao.models import *
from atividades.models import Tema
from django.forms.widgets import TextInput
from questionario.models import TemaQuestionario 

class TemaFilter(django_filters.FilterSet):
    tema = django_filters.CharFilter(
        field_name="tema", lookup_expr='icontains')

    class Meta:
        model = Tema
        fields = '__all__'

def get_faculdades(queryset, name, value):
    return queryset.filter(
        Exists(Curso.objects.filter(
            id=OuterRef('pk'),
            unidadeorganicaid=value
        ))
    )
############### TEMAS QUESTIONARIO  ############################
class TemaQuestionarioFilter(django_filters.FilterSet):
    tema = django_filters.CharFilter(
        field_name="tema", lookup_expr='icontains')

    class Meta:
        model = TemaQuestionario
        fields = '__all__'


class CursoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    sigla = django_filters.CharFilter(
        field_name="sigla", lookup_expr='icontains')
    unidadeorganicaid = django_filters.CharFilter(method=get_faculdades)

    class Meta:
        model = Curso
        fields = '__all__'

def get_faculdades_dep(queryset, name, value):
    return queryset.filter(
        Exists(Departamento.objects.filter(
            id=OuterRef('pk'),
            unidadeorganicaid=value
        ))
    )

class DepartamentoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    sigla = django_filters.CharFilter(
        field_name="sigla", lookup_expr='icontains')
    unidadeorganicaid = django_filters.CharFilter(method=get_faculdades_dep)

    class Meta:
        model = Departamento
        fields = '__all__'

def get_campi(queryset, name, value):
    return queryset.filter(
        Exists(Edificio.objects.filter(
            id=OuterRef('pk'),
            campus_id=value
        ))
    )

class EdificioFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    campus = django_filters.CharFilter(method=get_campi)

    class Meta:
        model = Edificio
        fields = ['nome', 'campus']


class UOFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(
        field_name="nome", lookup_expr='icontains')
    sigla = django_filters.CharFilter(
        field_name="sigla", lookup_expr='icontains')   
    campusis = django_filters.CharFilter(method=get_campi)

    class Meta:
        model = Unidadeorganica
        fields = ['nome','sigla', 'campusid']

def get_campi_menu(queryset,name,value):
    return queryset.filter(
        Exists(Menu.objects.filter(
            id=OuterRef('pk'),
            campus=value
        ))
    )    
class MenuFilter(django_filters.FilterSet):
    dia = django_filters.DateFilter(field_name="dia")
    campus = django_filters.CharFilter(method=get_campi)

    class Meta:
        model = Menu
        fields = ['campus', 'dia']

class TransporteFilter(django_filters.FilterSet):
    identificador = django_filters.CharFilter(
        field_name="transporte__identificador", lookup_expr='icontains')
    de = django_filters.CharFilter(
        field_name="origem", lookup_expr='icontains')
    para = django_filters.CharFilter(
        field_name="chegada", lookup_expr='icontains')     

    class Meta:
        model = Transportehorario
        fields = '__all__'

def get_dia(queryset, name, value):
        return queryset.filter(
            Exists(Diaaberto.objects.filter(
                id=OuterRef('pk'),
                datadiaabertoinicio__date=value
            ))
        )   
def get_dia_end(queryset, name, value):
        return queryset.filter(
            Exists(Diaaberto.objects.filter(
                id=OuterRef('pk'),
                datadiaabertofim__date=value
            ))
        )   

class DiaAbertoFilter(django_filters.FilterSet):
    ano = django_filters.CharFilter(field_name="ano",lookup_expr='icontains')
    diainicio = django_filters.DateFilter(method=get_dia,label="Inicio")
    diafim = django_filters.DateFilter(method=get_dia_end,label="Fim")
    class Meta:
        model = Diaaberto
        fields = '__all__'

# precoalunos = models.FloatField(db_column='PrecoAlunos')
#    precoprofessores = models.FloatField(
#        db_column='PrecoProfessores', blank=True, null=True)
#    id = models.AutoField(db_column='ID', primary_key=True)
#    enderecopaginaweb = models.CharField(
#        db_column='EnderecoPaginaWeb', max_length=255)
#    descricao = models.TextField(db_column='Descricao')
#    emaildiaaberto = models.CharField(
#        db_column='EmailDiaAberto', max_length=255)
#    ano = models.IntegerField(db_column='Ano')  # Field name made lowercase.
#    datadiaabertoinicio = models.DateTimeField(db_column='DataDiaAbertoInicio')
#    datadiaabertofim = models.DateTimeField(db_column='DataDiaAbertoFim')
#    datainscricaoatividadesinicio = models.DateTimeField(
#        db_column='DataInscricaoAtividadesInicio')  
#    datainscricaoatividadesfim = models.DateTimeField(
#        db_column='DataInscricaoAtividadesFim')
#    datapropostasatividadesincio = models.DateTimeField(
#        db_column='DataPropostasAtividadesIncio')
#    dataporpostaatividadesfim = models.DateTimeField(
#        db_column='DataPorpostaAtividadesFim')
#    administradorutilizadorid = models.ForeignKey(
#        'utilizadores.Administrador', models.SET_NULL, db_column='AdministradorUtilizadorID',null=True)
#    escalasessoes = models.TimeField(db_column='EscalaSessoes')
