import base64
from io import StringIO
import urllib
from django import template
from ..models import Inscricao
from utilizadores.models import Participante
from configuracao.models import Diaaberto
from django.db.models import Q, Sum
from atividades.models import Atividade, Sessao
from _datetime import datetime
from inscricoes.models import Inscricaoprato, Inscricaosessao

register = template.Library()


@register.filter
def inscrito(user):
    return Inscricao.objects.filter(participante=user.id).exists()


@register.filter
def get64(url):
    """
    Method returning base64 image data instead of URL
    """
    if url.startswith("http"):
        image = StringIO(urllib.urlopen(url).read())
        return 'data:image/jpg;base64,' + base64.b64encode(image.read())

    return url


@register.simple_tag
def sala(request, atividade):
    return atividade.get_sala_str(request)


@register.filter
def min_date(diaaberto):
    try:
        return Diaaberto.objects.get(id=diaaberto).datadiaabertoinicio.strftime("%d/%m/%Y")
    except:
        return ''


@register.filter
def max_date(diaaberto):
    try:
        return Diaaberto.objects.get(id=diaaberto).datadiaabertofim.strftime("%d/%m/%Y")
    except:
        return ''


@register.filter
def nparticipantes(diaaberto):
    result = diaaberto.inscricao_set.all().aggregate(Sum('nalunos'))
    return result['nalunos__sum'] if result['nalunos__sum'] is not None else 0


@register.filter
def ninscricoesindividuais(diaaberto):
    result = diaaberto.inscricao_set.filter(
        individual=True).aggregate(Sum('nalunos'))
    return result['nalunos__sum'] if result['nalunos__sum'] is not None else 0


@register.filter
def ninscricoesescola(diaaberto):
    result = diaaberto.inscricao_set.filter(
        individual=False).aggregate(Sum('nalunos'))
    return result['nalunos__sum'] if result['nalunos__sum'] is not None else 0


@register.filter
def atividadesdepartamento(departamento):
    result = Atividade.objects.filter(
        professoruniversitarioutilizadorid__departamento=departamento,
        estado="Aceite"
    ).count()
    return result


@register.filter
def sessoesdia(dia):
    dia = datetime.strptime(dia, '%d/%m/%Y')
    result = Sessao.objects.filter(
        dia=dia,
        atividadeid__estado="Aceite"
    ).count()
    return result


@register.filter
def vagasdia(dia):
    dia = datetime.strptime(dia, '%d/%m/%Y')
    result = Sessao.objects.filter(
        dia=dia,
        atividadeid__estado="Aceite",
    ).aggregate(Sum('vagas'))
    return result['vagas__sum'] if result['vagas__sum'] is not None else 0


@register.filter
def inscritossessoesdia(dia):
    dia = datetime.strptime(dia, '%d/%m/%Y')
    result = Inscricaosessao.objects.filter(
        sessao__dia=dia,
        sessao__atividadeid__estado="Aceite"
    ).aggregate(Sum('nparticipantes'))
    return result['nparticipantes__sum'] if result['nparticipantes__sum'] is not None else 0


@register.filter
def inscritosindividuaisdia(dia):
    dia = datetime.strptime(dia, '%d/%m/%Y')
    result = Inscricao.objects.filter(
        dia=dia,
        individual=True,
    ).aggregate(Sum('nalunos'))
    return result['nalunos__sum'] if result['nalunos__sum'] is not None else 0


@register.filter
def inscritosescoladia(dia):
    dia = datetime.strptime(dia, '%d/%m/%Y')
    result = Inscricao.objects.filter(
        dia=dia,
        individual=False,
    ).aggregate(Sum('nalunos'))
    return result['nalunos__sum'] if result['nalunos__sum'] is not None else 0


@register.filter
def inscritosmeio(meio, diaaberto):
    result = Inscricao.objects.filter(
        diaaberto=diaaberto,
        meio_transporte=meio,
    ).aggregate(Sum('nalunos'))
    return result['nalunos__sum'] if result['nalunos__sum'] is not None else 0


@register.filter
def transportesdia(dia):
    dia = datetime.strptime(dia, '%d/%m/%Y')
    result = Inscricao.objects.filter(
        dia=dia).filter(~Q(meio_transporte="outro"),
                        ).aggregate(Sum('nalunos'))
    return result['nalunos__sum'] if result['nalunos__sum'] is not None else 0


@register.filter
def almocosalunosdia(dia):
    dia = datetime.strptime(dia, '%d/%m/%Y')
    result = Inscricaoprato.objects.filter(
        inscricao__dia=dia
    ).aggregate(Sum('npratosalunos'))
    return result['npratosalunos__sum'] if result['npratosalunos__sum'] is not None else 0

@register.filter
def almocosdocentesdia(dia):
    dia = datetime.strptime(dia, '%d/%m/%Y')
    result = Inscricaoprato.objects.filter(
        inscricao__dia=dia
    ).aggregate(Sum('npratosdocentes'))
    return result['npratosdocentes__sum'] if result['npratosdocentes__sum'] is not None else 0

@register.filter
def almocampenha(diaaberto):
    alunos = Inscricaoprato.objects.filter(
        inscricao__diaaberto=diaaberto,
        campus__nome="Penha",
    ).aggregate(Sum('npratosalunos'))
    docentes = Inscricaoprato.objects.filter(
        inscricao__diaaberto=diaaberto,
        campus__nome="Penha",
    ).aggregate(Sum('npratosdocentes'))
    result = alunos['npratosalunos__sum'] if alunos['npratosalunos__sum'] is not None else 0
    result += docentes['npratosdocentes__sum'] if docentes['npratosdocentes__sum'] is not None else 0
    return result

@register.filter
def almocamgambelas(diaaberto):
    alunos = Inscricaoprato.objects.filter(
        inscricao__diaaberto=diaaberto,
        campus__nome="Gambelas",
    ).aggregate(Sum('npratosalunos'))
    docentes = Inscricaoprato.objects.filter(
        inscricao__diaaberto=diaaberto,
        campus__nome="Gambelas",
    ).aggregate(Sum('npratosdocentes'))
    result = alunos['npratosalunos__sum'] if alunos['npratosalunos__sum'] is not None else 0
    result += docentes['npratosdocentes__sum'] if docentes['npratosdocentes__sum'] is not None else 0
    return result
