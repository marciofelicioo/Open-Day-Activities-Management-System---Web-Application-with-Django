from django import template
from django.core.exceptions import ObjectDoesNotExist
register = template.Library()
from configuracao.models import Espaco
from utilizadores.models import Colaborador
from coordenadores.models import *
from django.utils.html import format_html
from atividades.models import Sessao
from datetime import datetime,timedelta
from colaboradores.models import ColaboradorHorario,PreferenciaAtividade,Preferencia

@register.filter
def colab_none(colab):
    if colab is None or str(colab) == 'None':
        return 'N/A'
    else:
        return colab.full_name

@register.filter
def local(id):
    if id != 'Check in':
        espaco = Espaco.objects.get(id=int(id))
        return "Sala "+str(espaco)+", Edifício " + espaco.edificio.__str__()
    else:
        return 'Check in'

@register.simple_tag
def free_colabs(coord,dia,horario,tipo,sessao=None):
        html = ''
        free_colabs=[]
        colabs = Colaborador.objects.filter(faculdade = coord.faculdade,utilizador_ptr_id__valido=True)
        free = True
        for colab in colabs: 
            tarefas = Tarefa.objects.filter(colab = colab.id,horario=horario,dia=dia)

            if not ColaboradorHorario.objects.filter(colab=colab.id).exists():
                continue

            if tarefas.exists():
                continue

            elif sessao is not None and (Preferencia.objects.filter(colab = colab.id, tipoTarefa='tarefaAuxiliar').exists() or not Preferencia.objects.filter(colab = colab.id).exists()):
                s = Sessao.objects.get(id=int(sessao))
                inicio = s.horarioid.inicio
                fim = s.horarioid.fim

                if not ColaboradorHorario.objects.filter(colab = colab.id,dia=dia)\
                    .filter(inicio__lte=horario,fim__gte=horario).exists(): 
                    continue

                if Tarefa.objects.filter(colab = colab.id,dia=dia,horario__gte=inicio).filter(horario__lte=fim).exists(): 
                    continue
                if TarefaAuxiliar.objects.filter(tarefaid__colab = colab.id,tarefaid__dia=dia,sessao__horarioid__inicio__lte=inicio,sessao__horarioid__fim__gte=inicio).exists():
                    continue
                if PreferenciaAtividade.objects.filter(preferencia__colab=colab.id).exists() and not PreferenciaAtividade.objects.filter(preferencia__colab=colab.id,atividade = s.atividadeid.id).exists():
                    continue
                tarefas = Tarefa.objects.filter(colab = colab.id,dia=dia)
                for t in tarefas:
                    hinicio = datetime.strptime(str(inicio),'%H:%M:%S') 
                    hfim =   datetime.strptime(str(fim),'%H:%M:%S')  
                    if datetime.strptime(str(t.horario),'%H:%M:%S') - hinicio >  timedelta(hours=0,minutes=15,seconds=0) or hfim - datetime.strptime(str(t.horario),'%H:%M:%S') < timedelta(days=-1,hours=23,minutes=45) :
                        free=False     
                if free == True:
                    free_colabs.append(colab)
            elif sessao is None :
                if not Preferencia.objects.filter(colab = colab.id, tipoTarefa=tipo).exists():
                    continue
                free=True
                tarefas = Tarefa.objects.filter(colab = colab.id,dia=dia)
                for t in tarefas:
                    h = datetime.strptime(str(horario),'%H:%M:%S')     
                    if datetime.strptime(str(t.horario),'%H:%M:%S') - h <  timedelta(hours=0,minutes=15,seconds=0) and h - datetime.strptime(str(t.horario),'%H:%M:%S') > timedelta(days=-1,hours=23,minutes=45) :
                        free=False     
                if TarefaAuxiliar.objects.filter(tarefaid__colab = colab.id,tarefaid__dia=dia)\
                    .filter(sessao__horarioid__inicio__lte=horario,sessao__horarioid__fim__gte=horario).exists(): 
                    continue
                if not ColaboradorHorario.objects.filter(colab = colab.id,dia=dia)\
                    .filter(inicio__lte=horario,fim__gte=horario).exists(): 
                    continue
                if free == True:
                    free_colabs.append(colab)
        if len(free_colabs) == 0:
            html = "<option disabled value="" hidden selected>Não existe colaboradores disponíveis</option>"
        else:
            html += "<option disabled value="" hidden selected>Colaborador a atribuir...</option>"
            for colab in free_colabs:
                html += "<option value="+str(colab.id)+">"+colab.full_name+"</option>"
        return format_html(html)


