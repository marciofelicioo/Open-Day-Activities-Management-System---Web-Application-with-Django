from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from utilizadores.models import *
from configuracao.models import *
from atividades.models import Atividade
from coordenadores.models import *
from colaboradores.models import *
from notificacoes.models import *
from django.shortcuts import redirect
from .forms import *
from .tables import *
from .filters import *
from django.contrib.auth import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from django.core.paginator import Paginator

from notificacoes import views
from django.utils.datetime_safe import date
from utilizadores.views import user_check
from django.forms.models import modelformset_factory



class consultar_tarefas(SingleTableMixin, FilterView):
	''' Funcionalidade de consultar tarefas do colaborador atual, funcionalidades de filtros para a a consulta das tarefas '''
	template_name = 'colaboradores/consultar_tarefas.html'
	table_class = TarefasTable
	filterset_class = TarefasFilter
	paginate_by = 10

	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(
			request=request, user_profile=[Colaborador])
		if not user_check_var.get('exists'):
			return user_check_var.get('render')
		return super().dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return Tarefa.objects.filter(colab=self.request.user)



class AtividadesColaborador(SingleTableMixin, FilterView):
	''' Página onde o colaborador escolhe quais são as atividades pelo qual está interessado'''
	table_class = ColaboradorAtividadesTable
	template_name = 'colaboradores/escolher_atividades.html'
	filterset_class = ColaboradorAtividadeFilter
	table_pagination = {
		'per_page': 10
	}
	
	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Colaborador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		self.user_check_var = user_check_var
		return super().dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return self.user_check_var.get('firstProfile').get_preferencia_atividade()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		table = self.get_table(**self.get_table_kwargs())
		context["deps"] = list(map(lambda x: (x.id, x.nome), Departamento.objects.filter(unidadeorganicaid=self.user_check_var.get('firstProfile').faculdade)))

		context[self.get_context_table_name(table)] = table
		return context


class AtividadesColaboradorSelecionadas(SingleTableMixin, FilterView):
	''' Página onde o colaborador escolhe quais vê as atividades que selecionou '''
	table_class = ColaboradorAtividadesSelecionadasTable
	template_name = 'colaboradores/minhas_atividades.html'
	filterset_class = ColaboradorAtividadeFilter
	table_pagination = {
		'per_page': 10
	}
	
	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Colaborador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		self.user_check_var = user_check_var
		return super().dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return self.user_check_var.get('firstProfile').get_atividades_escolhidas_tabela()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		table = self.get_table(**self.get_table_kwargs())
		table.request = self.request
		context["deps"] = list(map(lambda x: (x.id, x.nome), Departamento.objects.filter(unidadeorganicaid=self.user_check_var.get('firstProfile').faculdade)))
		context[self.get_context_table_name(table)] = table
		return context


def ver_departamentos(request):
	user_check_var = user_check(request=request, user_profile=[Colaborador])
	if not user_check_var.get('exists'): return user_check_var.get('render')

	value_uo = request.POST.get("value_uo")
	value_dep = request.POST.get('value_dep')

	value_uo = is_int(value_uo)
	if value_uo != 'None' and value_uo is not None and value_uo is not False:
		uo= Unidadeorganica.objects.filter(id=value_uo).first()
		departamentos= Departamento.objects.filter(unidadeorganicaid=  uo)
	else:
		departamentos= Departamento.objects.filter(unidadeorganicaid=user_check_var.get('firstProfile').faculdade)

	deps= []
	for dep in departamentos:    
		deps.append({'key': dep.id ,'value': dep.nome})
	value_dep = is_int(value_dep)
	default= {}
	if value_dep != 'None' and value_dep is not None and value_dep is not False:
		dep= Departamento.objects.get(id=value_dep)
		default={
					'key': dep.id,
					'value': dep.nome
		} 
	else:
		default={
						'key': "",
						'value': "Qualquer Departamento"
			} 
	return render(request=request,template_name='configuracao/dropdown.html',context={'options':deps, 'default': default})   



def minha_disponibilidade(request): 
	''' Página onde o colaborador seleciona a disponibilidade para desempenhar tarefas escolhendo desta forma o(s) horário(s) que lhe dá mais jeito '''
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = Colaborador.objects.get(id=user.id)      
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)
	erros = []
	HorarioFormSet = preferenciaHorarioFormset()
	horario_form_set = HorarioFormSet(queryset=ColaboradorHorario.objects.none())
	form_preferencia_tarefas = PreferenciaTarefasForm()	
	msg = False
	# horarios = []
	# for horario in ColaboradorHorario.objects.filter(colab=u)
	# 	if horari
	# 	horarios.append(horario)
	colab_horario_queryset = ColaboradorHorario.objects.filter(colab=u)
	if len(colab_horario_queryset) > 0:
		horario_form_set = HorarioFormSet(queryset=colab_horario_queryset)
	
	
	
	preferencia_auxiliar = Preferencia.objects.filter(colab = u, tipoTarefa = "tarefaAuxiliar")
	if 	len(preferencia_auxiliar)>0:
		tarefa_auxiliar = True
	else:
		tarefa_auxiliar = False

	preferencia_acompanhar = Preferencia.objects.filter(colab = u, tipoTarefa = "tarefaAcompanhar")
	if 	len(preferencia_acompanhar)>0:
		tarefa_acompanhar = True
	else:
		tarefa_acompanhar = False
	preferencia_outra = Preferencia.objects.filter(colab = u, tipoTarefa = "tarefaOutra")
	if 	len(preferencia_outra)>0:
		tarefa_outra = True
	else:
		tarefa_outra = False
	
	
	
	
	if request.method == "POST":
		horario_form_set = HorarioFormSet(request.POST)
		values = PreferenciaTarefasForm(request.POST)	

		tarefas = request.POST.getlist('tipo_tarefa')
		if tarefas == []: 
			erros.append("Deverá escolher pelo menos uma preferência de tarefa")
		print(horario_form_set.errors)
		if values.is_valid() and horario_form_set.is_valid():

			instances = horario_form_set.save(commit=False)

			for instance in instances:
				instance.colab = u
				instance.save()
			for instance in horario_form_set.deleted_objects:
				instance.delete()
			
			if  "tarefaAcompanhar" in tarefas:
				preferencia = Preferencia.objects.get_or_create(colab = u, tipoTarefa = "tarefaAcompanhar")[0]
			else:
				preferencia_acompanhar = Preferencia.objects.filter(colab = u, tipoTarefa = "tarefaAcompanhar")
				if 	len(preferencia_acompanhar)>0:
					preferencia_acompanhar.delete()
			
			if "tarefaAuxiliar" in tarefas:
				preferencia = Preferencia.objects.get_or_create(colab = u, tipoTarefa = "tarefaAuxiliar")[0]
			else:
				preferencia_auxiliar = Preferencia.objects.filter(colab = u, tipoTarefa = "tarefaAuxiliar")
				if 	len(preferencia_auxiliar)>0:	
					preferencia_auxiliar.delete()

			if "tarefaOutra" in tarefas:
				preferencia = Preferencia.objects.get_or_create(colab = u, tipoTarefa = "tarefaOutra")[0]
			else:
				preferencia_outra = Preferencia.objects.filter(colab = u, tipoTarefa = "tarefaOutra")
				if 	len(preferencia_outra)>0:
					preferencia_outra.delete()

			return redirect('colaboradores:preferencia-atividade')
		else:
			if not "Deverá escolher pelo menos uma preferência de tarefa" in erros:
				erros.append("Preencha corretamente todos os campos")
			msg = True
			
	return render(request = request,
				template_name='colaboradores/minha_disponibilidade.html',
				context={'form_preferencia_tarefas': form_preferencia_tarefas,
				'horario_form_set': horario_form_set,'dias' : Diaaberto.current().days_as_array() ,
				'msg' : msg,'erros':erros,'tarefa_auxiliar':tarefa_auxiliar,'tarefa_acompanhar':tarefa_acompanhar,'tarefa_outra':tarefa_outra})


def preferenciaHorarioFormset(extra = 0, minVal = 1):
	formSets = modelformset_factory(model=ColaboradorHorario, exclude = ['colab','id'],form=colaboradorHorarioForm, extra = extra, min_num = minVal, can_delete=True, )
	return formSets

def newHorarioRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_dia': "form-" + str(value-1) + "-dia",
		'form_inicio': "form-" + str(value-1) + "-inicio",
		'form_fim': "form-" + str(value-1) + "-fim",
		'form_id': 'form-' + str(value-1) + '-id',
		'dias' : Diaaberto.current().days_as_array() 
	}
	return render(request=request, template_name='colaboradores/preferencia_horario.html', context=data)




def concluir_disponibilidade(request):
	''' Página que é mostrada ao colaborador quando altera a sua disponibilidade na plataforma '''
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = "Colaborador"       
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)

	return render(request=request,
				  template_name="colaboradores/concluir_disponibilidade.html")


def selecionar_atividade(request,id):
	''' Selecionar uma atividade como preferencia '''
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = Colaborador.objects.get(id=user.id)        
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)
	msg = True
	preferencia_auxiliar = Preferencia.objects.get_or_create(colab = u, tipoTarefa = "tarefaAuxiliar")[0]
	atividade = Atividade.objects.get(id=id)	
	preferencia_atividade = PreferenciaAtividade(preferencia = preferencia_auxiliar,atividade = atividade)
	preferencia_atividade.save()	
	return redirect('colaboradores:escolher-atividades')




def retirar_atividade(request,id):
	''' Remover uma atividade das preferencias '''
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = Colaborador.objects.get(id=user.id)        
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)
	msg = True
	preferencia_auxiliar = Preferencia.objects.get_or_create(colab = u, tipoTarefa = "tarefaAuxiliar")[0]
	atividade = Atividade.objects.get(id=id)	
	preferencia_atividade = PreferenciaAtividade.objects.get_or_create(preferencia = preferencia_auxiliar,atividade = atividade)[0]
	preferencia_atividade.delete()
	return redirect('colaboradores:atividades-escolhidas')


def preferencia_atividade(request):
	''' Página que permite ao colaborador obtar por escolher as atividades que pretende, ver atividades escolhidas, ou concluir a sua atualização de disponibilidade '''
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = "Colaborador"       
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)
	return render(request=request,
				  template_name="colaboradores/preferencia_atividade.html")

def concluir_tarefa(request, id): 
	''' Funcionalidade de conclusão de uma tarefa do colaborador '''
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = "Colaborador"       
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)


	tarefa = Tarefa.objects.get(id=id)
	tarefa.estado="Concluida"
	tarefa.save()
	msg="Tarefa concluída com sucesso!"
	return render(request=request,
				  template_name="colaboradores/tarefa_concluida.html",
				  context={"msg": msg})



def iniciar_tarefa(request, id): 
	''' Funcionalidade de inicio de uma tarefa do colaborador '''
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = "Colaborador"       
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)


	tarefa = Tarefa.objects.get(id=id)
	tarefa.estado="Iniciada"
	tarefa.save()
	return redirect('colaboradores:consultar-tarefas')   



def cancelar_tarefa(request, id):
	''' Funcionalidade de cancelamento de uma tarefa do colaborador ''' 
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Colaborador").exists():
			u = "Colaborador"       
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5)
	# Envio de notificação automática
	views.enviar_notificacao_automatica(request,"cancelarTarefa",id) #Envio de notificação automática !!!!
	tarefa = Tarefa.objects.get(id=id)
	nome = tarefa.coord.first_name+" "+tarefa.coord.last_name
	msg = "A enviar pedido de cancelamento de tarefa a "+nome
	return render(request=request,
				  template_name="colaboradores/enviar_notificacao_informativa.html",
				  context={"msg": msg})


def validar_cancelamento_tarefa(request, id_notificacao):
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Coordenador").exists():
			u = "Coordenador"       
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5) 
	try:
		notificacao = Notificacao.objects.get(id=id_notificacao)
		notificacao.deleted = True
		notificacao.save()
		id_tarefa = notificacao.action_object.id
		tarefa = Tarefa.objects.get(id=id_tarefa)
		tarefa.estado="Cancelada"
		tarefa.save()
		views.enviar_notificacao_automatica(request,"confirmarCancelarTarefa",id_tarefa)
	except:
		return redirect('utilizadores:mensagem',11)    
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def rejeitar_cancelamento_tarefa(request, id_notificacao):
	if request.user.is_authenticated:    
		user = get_user(request)
		if user.groups.filter(name = "Coordenador").exists():
			u = "Coordenador"       
		else:
			return redirect('utilizadores:mensagem',5) 
	else:
		return redirect('utilizadores:mensagem',5) 
	try:
		notificacao = Notificacao.objects.get(id=id_notificacao)
		notificacao.deleted = True
		notificacao.save() 
		id_tarefa = notificacao.action_object.id
		views.enviar_notificacao_automatica(request,"rejeitarCancelarTarefa",id_tarefa)
	except:
		return redirect('utilizadores:mensagem',11)      
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



