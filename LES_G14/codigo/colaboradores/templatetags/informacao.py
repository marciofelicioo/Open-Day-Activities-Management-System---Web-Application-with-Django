from django import template
from coordenadores.models import Tarefa,TarefaAcompanhar, TarefaAuxiliar,TarefaOutra
from datetime import date, timedelta
import datetime

register = template.Library()

@register.filter(name='get_due_date_string')
def get_due_date_string(value,id):
    tarefa = Tarefa.objects.get(id=id)
    passou = tarefa.horario.strftime('%H:%M:%S') < datetime.datetime.now().strftime('%H:%M:%S')
    value = tarefa.dia
    delta = value - date.today()
    if tarefa.estado == "Cancelada":
        return "Esta tarefa foi cancelada"
    if delta.days == 0 and tarefa.estado != "Concluida":
        return "Esta tarefa é hoje!"
    elif  delta.days == 0 and tarefa.estado == "Concluida":
        return "Esta tarefa foi hoje!"
    elif delta.days < 1:
        return "Esta tarefa foi há %s %s atrás!" % (abs(delta.days),
            ("dia" if abs(delta.days) == 1 else "dias"))
    elif delta.days == 1:
        return "Esta tarefa é amanhã"
    elif delta.days > 1:
        return "Esta tarefa é daqui a %s dias" % delta.days


@register.filter(name='tarefa_passou')
def tarefa_passou(value,id):
    tarefa = Tarefa.objects.get(id=id) 
    value = tarefa.dia
    delta = value - date.today()
    if delta.days > 0:
        return False
    else:
        return tarefa.horario.strftime('%H:%M:%S') < datetime.datetime.now().strftime('%H:%M:%S')
    
  


@register.filter(name='iniciar_tarefa')
def iniciar_tarefa(value,id):
    tarefa = Tarefa.objects.get(id=id)
    value = tarefa.dia
    comecou = tarefa.horario.strftime('%H:%M:%S') < datetime.datetime.now().strftime('%H:%M:%S')
    delta = value - date.today()
    return comecou == True and delta.days == 0
 
@register.filter(name='get_tarefa_auxiliar_prof') 
def get_tarefa_auxiliar_prof(tarefa,id):
    tarefa = TarefaAuxiliar.objects.get(tarefaid=id)
    if tarefa!=None:
        return tarefa.sessao.atividadeid.professoruniversitarioutilizadorid.first_name+" "+tarefa.sessao.atividadeid.professoruniversitarioutilizadorid.last_name
    else:
        pass

@register.filter(name='get_tarefa_auxiliar_campus') 
def get_tarefa_auxiliar_campus(tarefa,id):
    tarefa = TarefaAuxiliar.objects.get(tarefaid=id)
    if tarefa!=None:    
        return tarefa.sessao.atividadeid.espacoid.edificio.campus.nome
    else:
        pass

@register.filter(name='get_tarefa_auxiliar_sala') 
def get_tarefa_auxiliar_sala(tarefa,id):
    tarefa = TarefaAuxiliar.objects.get(tarefaid=id)
    if tarefa!=None:
        return tarefa.sessao.atividadeid.espacoid.edificio.campus.nome    
    else:
        pass

@register.filter(name='get_tarefa_auxiliar_edificio') 
def get_tarefa_auxiliar_edificio(tarefa,id):
    tarefa = TarefaAuxiliar.objects.get(tarefaid=id)
    if tarefa!=None:
        return tarefa.sessao.atividadeid.espacoid.edificio.nome
    else:
        pass

@register.filter(name='get_tarefa_auxiliar_espaco') 
def get_tarefa_auxiliar_espaco(tarefa,id):
    tarefa = TarefaAuxiliar.objects.get(tarefaid=id)
    if tarefa!=None:
        return tarefa.sessao.atividadeid.espacoid.nome
    else:
        pass
###


@register.filter(name='get_tarefa_acompanhar_origem') 
def get_tarefa_acompanhar_origem(tarefa,id):
    tarefa = TarefaAcompanhar.objects.get(tarefaid=id)
    if tarefa!=None:
        return tarefa.origem
    else:
        pass
@register.filter(name='get_tarefa_acompanhar_destino') 
def get_tarefa_acompanhar_destino(tarefa,id):
    tarefa = TarefaAcompanhar.objects.get(tarefaid=id)
    if tarefa!=None:
        return tarefa.destino
    else:
        pass 

###


@register.filter(name='get_tarefa_outra_descricao') 
def get_tarefa_outra_descricao(tarefa,id):
    tarefa = TarefaOutra.objects.get(tarefaid=id)
    if tarefa!=None:
        return tarefa.descricao
    else:
        pass    

