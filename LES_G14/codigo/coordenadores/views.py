from django.shortcuts import render, redirect  
from .models import *
from .forms import *
from inscricoes.models import *
from configuracao.models import Horario
from utilizadores.models import ProfessorUniversitario, Coordenador
from configuracao.models import Diaaberto, Horario, Campus, Edificio, Espaco
from django.http import HttpResponseRedirect
from datetime import datetime, date,timezone,time
from _datetime import timedelta
from django.db.models import Q
from coordenadores.forms import *
from notificacoes import views
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters.views import FilterView
from coordenadores.tables import TarefaTable
from coordenadores.filters import TarefaFilter
from utilizadores.views import user_check
from django.http.response import HttpResponse
from atividades.models import Sessao

def adicionartarefa(request,id=None):
    user_check_var = user_check(request=request, user_profile=[Coordenador])
    if not user_check_var.get('exists'): return user_check_var.get('render')
    if Diaaberto.current() is None: return redirect('coordenadores:consultarTarefa')
    if id:
        tarefa = Tarefa.objects.get(id=id)
    else:
        tarefa = None

    if request.method == 'POST':
        if request.POST['tipo']=='tarefaAuxiliar':
            form = TarefaAuxiliarForm(data=request.POST,facul=user_check_var.get('firstProfile').faculdade.id)
        elif request.POST['tipo']=='tarefaAcompanhar':
            form = TarefaAcompanharForm(data=request.POST,facul=user_check_var.get('firstProfile').faculdade.id)
        elif request.POST['tipo']=='tarefaOutra':
            form = TarefaOutraForm(request.POST)
        if form.is_valid():
            coord = Coordenador.objects.get(id=request.user.id)
            save=form.save(user=coord,id=id)
            if id:
                views.enviar_notificacao_automatica(request,sigla="tarefaAlterada",id=id)
            else:
                views.enviar_notificacao_automatica(request,sigla="tarefaAtribuida",id=save)
            return redirect('coordenadores:consultarTarefa')
    return render(request = request,template_name='coordenadores/criarTarefa.html',context={
        'tarefa':tarefa,
    })

def tipoTarefa(request):  
    user_check_var = user_check(request=request, user_profile=[Coordenador])

    template =''
    form = ''
    atividades = None
    ativ = None
    if request.method == 'POST':
        tipo = request.POST['tipo']
        if tipo == 'tarefaAuxiliar':
            template = 'coordenadores/tarefaAuxiliar.html'
            if request.POST.get('id'):
                tarefa = TarefaAuxiliar.objects.get(tarefaid=int(request.POST['id']))
                form = TarefaAuxiliarForm(initial={'atividade':tarefa.sessao.atividadeid.id,'dia':tarefa.tarefaid.dia,
                                                    'horario':tarefa.tarefaid.horario,'sessao':tarefa.sessao},
                                                    facul=user_check_var.get('firstProfile').faculdade.id)
                atividades = Atividade.tarefas_get_atividades(user_check_var.get('firstProfile').faculdade.id)
                ativ = tarefa.sessao.atividadeid
            else:
                form = TarefaAuxiliarForm(facul=user_check_var.get('firstProfile').faculdade.id)       
        elif tipo == 'tarefaAcompanhar':
            template = 'coordenadores/tarefaAcompanhar.html'
            if request.POST.get('id'):
                tarefa = TarefaAcompanhar.objects.get(tarefaid=int(request.POST['id']))
                form = TarefaAcompanharForm(initial={'grupo':tarefa.inscricao.id,'dia':tarefa.tarefaid.dia},facul=user_check_var.get('firstProfile').faculdade.id)
            else:
                 form = TarefaAcompanharForm(facul=user_check_var.get('firstProfile').faculdade.id)           
        elif tipo == 'tarefaOutra':
            template = 'coordenadores/tarefaOutra.html'
            if request.POST.get('id'):
                tarefa = TarefaOutra.objects.get(tarefaid=int(request.POST['id']))
                form = TarefaOutraForm(initial={'dia':tarefa.tarefaid.dia,'horario':tarefa.tarefaid.horario,'descricao':tarefa.descricao,'colab':tarefa.tarefaid.colab})      
            else:
                  form = TarefaOutraForm() 
    if template != '':         
        return render(request=request,template_name=template,context={'form':form,'options':atividades,'ativ':ativ})
    else: return HttpResponse()

def diasAtividade(request):
    dias=[] 
    default = {
        'key': '',
        'value': 'Escolha o dia'
    }
    atividade = request.POST.get('atividadeid')
    if request.method == 'POST':
        if 'tarefa' in request.POST and request.POST['tarefa']!='':
            if TarefaAuxiliar.objects.get(tarefaid=int(request.POST['tarefa'])).sessao.atividadeid.id == Atividade.objects.get(id=atividade).id:
                tarefa = TarefaAuxiliar.objects.get(tarefaid=int(request.POST['tarefa']))
                default={
                    'key': str(tarefa.tarefaid.dia),
                    'value': tarefa.tarefaid.dia
                }
        if atividade !='': 
            atividade = Atividade.objects.get(id=atividade)   
            dias = atividade.get_dias()  
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':dias, 'default': default}
            )

def sessoesAtividade(request):
    atividade= request.POST['atividadeid']
    dia = str(request.POST['dia'])
    default = {
                'key': '',
                'value': 'Escolha a sessão'
            }
    options=[]
    if request.method == 'POST':

        if 'tarefa' in request.POST and request.POST['tarefa']!='':
            tarefa =TarefaAuxiliar.objects.get(tarefaid=int(request.POST['tarefa']))
            if tarefa.sessao.atividadeid.id == Atividade.objects.get(id=atividade).id\
                and (tarefa.sessao.dia == dia or dia == ''):
                atividade = tarefa.sessao.atividadeid.id
                dia = str(tarefa.tarefaid.dia)
                default={
                    'key': str(tarefa.sessao.id),
                    'value': str(tarefa.sessao.horarioid.inicio) + ' até ' + str(tarefa.sessao.horarioid.fim)
                }

        if dia !='':
            sessoes = Sessao.tarefas_get_sessoes(atividade=atividade,dia=dia)
    
            options = [{
                    'key':	str(sessao.id),
                    'value':	sessao.horarioid.inicio.strftime('%H:%M') +' até '+ sessao.horarioid.fim.strftime('%H:%M')
                } for sessao in sessoes
            ]
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options': options, 'default': default}
            )

def colaboradores(request):
    default=[]
    horario = ''
    sessao= None
    options=[]
    default = {
        'key': '',
        'value': 'Não atribuir'
    }
    
    if request.method == 'POST':
        if 'tarefa' in request.POST and request.POST['tarefa']!='':
            tarefa = Tarefa.objects.get(id=int(request.POST['tarefa']))
            tipo = tarefa.tipo
            if tarefa.tipo == 'tarefaAuxiliar':
                sessao=tarefa.tarefaauxiliar.sessao.id

            dia = tarefa.dia
            horario = tarefa.horario

            if tarefa.colab is not None:
                default={
                    'key': str(tarefa.colab.utilizador_ptr_id),
                    'value': str(tarefa.colab.full_name)
                } 
        else:
            if request.POST.get('sessao') !='' or request.POST.get('sessao'):
                s = Sessao.objects.get(id=int(request.POST.get('sessao')))
                sessao = s.id
                horario = s.horarioid.inicio
            if request.POST.get('horario') !='' or request.POST.get('horario'):
                horario = request.POST.get('horario')
                sessao = None
            dia = request.POST.get('dia')
            tipo = request.POST.get('tipo')
        coordenador = Coordenador.objects.get(id = request.user.id)
        if horario != '' and dia != '':
            colabs = Colaborador.get_free_colabs(coord = coordenador,dia = dia, horario=horario,tipo = tipo, sessao = sessao)
            if len(colabs)==0:
                default = {
                    'key': '',
                    'value': 'Não existem colaboradores disponíveis'
                }
            else:
                options = [{
                            'key': '',
                            'value': 'Não atribuir'
                        }]+[{
                            'key':	str(colab.utilizador_ptr_id),
                            'value':	str(colab.full_name)
                        } for colab in colabs
                    ]
            
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':options, 'default': default}
            )

def grupoInfo(request):
    info = ''
    responsavel = ''
    if request.method == 'POST':
        if 'tarefa' in request.POST and request.POST.get('tarefa') != '':
            tarefa = TarefaAcompanhar.objects.get(tarefaid=request.POST.get('tarefa'))
            info = Inscricao.objects.get(id=tarefa.inscricao.id)
        elif request.POST['grupo_id'] != '':   
            info = Inscricao.objects.get(id=request.POST['grupo_id'])
            responsavel = Responsavel.objects.get(inscricao=info.id)
    return render(request=request,
                template_name='coordenadores/grupoInfo.html',
                context={'info': info,'responsavel':responsavel}
            )

def diasGrupo(request):
    dias=[]
    default=[]
    grupo = request.POST['grupo_id']
    default = {
        'key': '',
        'value': 'Escolha o dia'
    }
    if 'tarefa' in request.POST and request.POST.get('tarefa')!='':
        tarefa = TarefaAcompanhar.objects.get(tarefaid=request.POST.get('tarefa'))
        if int(tarefa.inscricao.id) == int(grupo) or grupo=='':
            default={
                'key': str(tarefa.tarefaid.dia),
                'value': tarefa.tarefaid.dia
            }
            

    inscricao = Inscricao.objects.get(id=grupo)
    dias = inscricao.get_dias()
     
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':dias, 'default': default}
            )

def horarioGrupo(request):
    horario = []
    dia = request.POST['dia']
    default = {
        'key': '',
        'value': 'Escolha o horário'
    }
    grupo = request.POST.get('grupo_id')
    if request.method == 'POST':    
        if 'tarefa' in request.POST and request.POST.get('tarefa')!='':
            tarefa = TarefaAcompanhar.objects.get(tarefaid=request.POST.get('tarefa'))
            if (tarefa.tarefaid.dia == dia or dia == ''):
            
                grupo = tarefa.inscricao.id
                dia = str(tarefa.tarefaid.dia)
                default={
                    'key': str(tarefa.tarefaid.horario),
                    'value': tarefa.tarefaid.horario
                 } 
        if dia!='' and dia is not None: 
            inscricao = Inscricao.objects.get(id=grupo)
            horario = inscricao.get_horarios(dia)
    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':horario, 'default': default}
            )

def locaisOrigem(request):
    origens = []
    dia = request.POST['dia']
    horario = request.POST.get('horario')
    default = {
        'key': '',
        'value': 'Escolha o local de encontro'
    }
    grupo = request.POST.get('grupo_id')
    if request.method == 'POST':    
        if 'tarefa' in request.POST and request.POST.get('tarefa')!='':
            tarefa = TarefaAcompanhar.objects.get(tarefaid=request.POST.get('tarefa'))
            if tarefa.tarefaid.horario == horario or horario == '':
                grupo = tarefa.inscricao.id
                horario = tarefa.tarefaid.horario
                dia = str(tarefa.tarefaid.dia)
                if tarefa.origem != 'Check in':
                    local = Espaco.objects.get(id=int(tarefa.origem))
                    local_nome = local.nome
                    local = local.id
                else: 
                    local = "Check in"
                    local_nome = "Check in"
                default={
                    'key': str(local),
                    'value': local_nome
                }
        if horario !='' and horario is not None and dia!='' and dia is not None:        
            inscricao = Inscricao.objects.get(id=grupo)
            origens =  inscricao.get_origem(dia,horario)

    return render(request=request,
                template_name='configuracao/dropdown.html',
                context={'options':origens, 'default': default}
            )  

def locaisDestino(request):
    grupo = request.POST.get('grupo_id')
    dia = request.POST['dia']
    
    horario = request.POST.get('horario')
    default = {
        'key': '',
        'value': 'Escolha o local de destino'
    }
    destinos = []
    if request.method == 'POST':    
        if 'tarefa' in request.POST and request.POST.get('tarefa')!='':
            tarefa = TarefaAcompanhar.objects.get(tarefaid=request.POST.get('tarefa'))
            if tarefa.tarefaid.horario == horario or horario == '':
                grupo = tarefa.inscricao.id
                horario = tarefa.tarefaid.horario
                dia = str(tarefa.tarefaid.dia)
                origem = Espaco.objects.get(id=int(tarefa.origem))
                local = Espaco.objects.get(id=int(tarefa.destino))
                default={
                    'key': tarefa.destino,
                    'value': local.nome
                }         
        if horario !='' and horario is not None and dia!='' and dia is not None: 
            if request.POST['origem'] == 'Check in':
                origem = request.POST['origem']
            else:
                origem = Espaco.objects.get(id=int(request.POST['origem']))
            inscricao = Inscricao.objects.get(id=grupo)
            destinos =  inscricao.get_destino(dia,horario,origem)

    return render(request=request,template_name='configuracao/dropdown.html',context={'options':destinos, 'default': default})  

class ConsultarTarefas(SingleTableMixin, FilterView):
    table_class = TarefaTable
    template_name = 'coordenadores/consultartarefa.html'
    filterset_class = TarefaFilter
    table_pagination = {
		'per_page': 10
	}

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[Coordenador])
        if not user_check_var.get('exists'): return user_check_var.get('render')
        self.user = user_check_var.get('firstProfile')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Tarefa.objects.filter(coord=self.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        context["colabs"] = list(map(lambda x: (x.id, x.full_name), Colaborador.objects.filter(faculdade = self.user.faculdade,utilizador_ptr_id__valido=True)))
        context["is_open"] = True if Diaaberto.current() is not None else False
        table.colabs = list(map(lambda x: (x.id, x.full_name), Colaborador.objects.filter(faculdade = self.user.faculdade,utilizador_ptr_id__valido=True)))
        context[self.get_context_table_name(table)] = table
        return context

def eliminartarefa(request,id):
    user_check_var = user_check(request=request, user_profile=[Coordenador])
    if not user_check_var.get('exists'): return user_check_var.get('render')
    
    tarefa = ''
    if Tarefa.objects.filter(id=id,coord=user_check_var.get('firstProfile')).exists():
        tarefa = Tarefa.objects.get(id=id,coord=user_check_var.get('firstProfile'))
        if tarefa.eliminar == True:
            if tarefa.colab is not None:
                views.enviar_notificacao_automatica(request,"tarefaApagada",id)
            tarefa.delete()    
            return redirect('coordenadores:consultarTarefa')
    return redirect('coordenadores:consultarTarefa')

def atribuirColaborador(request,id):
    user_check_var = user_check(request=request, user_profile=[Coordenador])
    if not user_check_var.get('exists'): return user_check_var.get('render')
    if request.method == 'POST':
        colab = Colaborador.objects.get(id = int(request.POST.get('colab')))
        Tarefa.objects.filter(id=id).update(colab=colab,estado='naoConcluida')
        views.enviar_notificacao_automatica(request,"tarefaAtribuida",id)
    return redirect('coordenadores:consultarTarefa')

