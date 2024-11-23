import csv
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse

from inscricoes.utils import render_pdf
from questionario.models import TemaQuestionario
from .forms import *
from .models import *
from utilizadores.models import *
from inscricoes.models import Inscricao, Inscricaosessao, Inscricaotransporte
from atividades.models import Tema
from datetime import datetime, timezone,date, time
from atividades.models import Sessao
from django.core.serializers import *
from django.db.models import Count, Q
import random
from datetime import timedelta
import json
from pip._vendor import requests
from django.core import serializers
from utilizadores.views import user_check
from configuracao.tables import CursoTable, DepartamentoTable, DiaAbertoTable, EdificioTable, MenuTable, TemaTable,TemaQuestionarioTable, TransporteTable, UOTable
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters.views import FilterView
from configuracao.filters import CursoFilter, DepartamentoFilter, DiaAbertoFilter, EdificioFilter, MenuFilter, TemaFilter, TemaQuestionarioFilter,TransporteFilter, UOFilter
from django.db.models.query import QuerySet
# Create your views here.

class TimeC():
	time: str = None
	seconds: int = None
	time_split = None

	def __init__(self, time:str = None, time_as_seconds: int = None):
		if time is not None and time_as_seconds is not None:
			raise Exception('Only one argument can be set')
		if time is None and time_as_seconds is None:
			raise Exception('Either argument must be set')
		if time is not None:
			self.time = time
			self.time_split = str(time).split(':')
			self.seconds = int(self.time_split[0])*60*60 + int(self.time_split[1])*60
			self.__str__()
		else:
			self.time = str(int(time_as_seconds/60/60)) + ':' + str(int(time_as_seconds%3600))
			self.seconds = time_as_seconds
			self.time_split = self.time.split(':')
			self.__str__()


	def __add__(self, other):
		time_s = other.seconds
		time_sum = self.seconds+time_s
		if time_sum >= 86400:
			time_sum-=86400
		return TimeC(time_as_seconds=time_sum)

	def __sub__(self, other):
		time_s = other.seconds
		time_sub = self.seconds-time_s
		if time_sub < 0:
			time_sub=0
		return TimeC(time_as_seconds=time_sub)

	def __str__(self):
		if (len(self.time_split[0]) == 1): time_start = '0' + str(self.time_split[0]) 
		else: time_start = self.time_split[0]
		if (len(self.time_split[1]) == 1): time_end =  self.time_split[1] + '0'
		else: time_end =  self.time_split[1]
		self.time= time_start+':'+time_end
		return self.time

	def __eq__(self, other):
		return other.__str__() == self.__str__()
	def __lt__(self, other):
		return self.seconds < other.seconds
	def __gt__(self, other):
		return self.seconds > other.seconds
	def __le__(self, other):
		return self.seconds <= other.seconds
	def __ge__(self, other):
		return self.seconds >= other.seconds	
	def __ne__(self, other):
		return not self.__eq__(self,other=other)

class viewDays(SingleTableMixin, FilterView):

	table_class = DiaAbertoTable
	template_name = 'configuracao/listaDiaAberto.html'
	filterset_class = DiaAbertoFilter
	table_pagination = {
		'per_page': 10
	}


	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Administrador])
		if not user_check_var.get('exists'): return user_check_var.get('render')

		return super().dispatch(request, *args, **kwargs)
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		earliest = Diaaberto.objects.all().order_by('ano').first()	#Obtain some constants
		latest = Diaaberto.objects.all().order_by('ano').last()
		current = Diaaberto.current()
		is_open=False
		latest_year = 9999
		earliest_year = 0
		if earliest is not None: 
			if current is not None:
				is_open = True
			latest_year = latest.ano
			earliest_year = earliest.ano
		context["earliest"] = earliest_year
		context['latest'] = latest_year
		context["is_open"] = is_open
		return context


def newDay(request, id=None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')
	if Diaaberto.current() is not None and id is None:
		return redirect('configuracao:diasAbertos')

	logged_admin = Administrador.objects.get(utilizador_ptr_id = request.user.id)

	if id is None:
		dia_aberto = Diaaberto(administradorutilizadorid=logged_admin)
	else:
		dia_aberto = Diaaberto.objects.get(id=id,administradorutilizadorid=logged_admin)

	dia_aberto_form = diaAbertoSettingsForm(instance=dia_aberto)

	if request.method == 'POST':
		submitted_data = request.POST.copy()
		dia_aberto_form = diaAbertoSettingsForm(submitted_data, instance=dia_aberto)

		if dia_aberto_form.is_valid():
			dia_aberto = dia_aberto_form.save()
			if dia_aberto.escalasessoes > time(0,59):
				dia_aberto.escalasessoes = time(0,59)
				dia_aberto.save()
			return redirect('configuracao:diasAbertos')

	return render(request=request,
				template_name = 'configuracao/diaAbertoForm.html',
				context = {'form': dia_aberto_form})

def delDay(request, id=None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	if id is not None:
		dia_aberto = Diaaberto.objects.filter(id=id)
		dia_aberto.delete()
	return redirect('configuracao:diasAbertos')

class verMenus(SingleTableMixin, FilterView):

	table_class = MenuTable
	template_name = 'configuracao/listaMenu.html'
	filterset_class = MenuFilter
	table_pagination = {
		'per_page': 10
	}

	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Administrador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		return super().dispatch(request, *args, **kwargs)
		
	def get_context_data(self, **kwargs):
		context = super(SingleTableMixin, self).get_context_data(**kwargs)
		table = self.get_table(**self.get_table_kwargs())
		table.fixed = True
		context["campi"] = list(map(lambda x: (x.id, x.nome), Campus.objects.all()))
		context[self.get_context_table_name(table)] = table
		return context

def newMenu(request, id = None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	PratoFormSet = menuPratoFormset()
	prato_form_set = PratoFormSet(queryset=Prato.objects.none())
	menu_object = Menu()

	if id is not None:
		menu_object = Menu.objects.get(id=id)
		prato_form_set = PratoFormSet(queryset=Prato.objects.filter(menuid=menu_object))
	menu_form = menuForm(instance=menu_object)

	if request.method == 'POST':
		menu_form = menuForm(request.POST,instance=menu_object)
		prato_form_set = PratoFormSet(request.POST)
		#print(request.POST)
		if menu_form.is_valid() and prato_form_set.is_valid():
			menu_object = menu_form.save()
			instances = prato_form_set.save(commit=False)

			for instance in instances:
				instance.menuid = menu_object
				instance.save()
			for instance in prato_form_set.deleted_objects:
				instance.delete()
			return redirect('configuracao:verMenus')

	return render(request=request,
				  template_name='configuracao/menuForm.html',
				  context = {'form': menu_form, 'formset': prato_form_set}
				)

def delMenu(request, id = None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	menu=Menu.objects.get(id=id)
	menu.delete()
	return redirect('configuracao:verMenus')

def menuPratoFormset(extra = 0, minVal = 1, max = 1000):
	formSets = modelformset_factory(model=Prato, exclude = ['id','menuid'],widgets={
			'tipo': Select(attrs={'class': 'input'}),
			'prato': TextInput(attrs={'class': 'input'}),
			'nrpratosdisponiveis': NumberInput(attrs={'class': 'input', 'min':'1','style':'width: 30%'}),
		},labels={
			'nrpratosdisponiveis': '# Pratos'
		}, extra = extra, min_num = minVal, max_num = max, can_delete=True)
	return formSets

def delPrato(request, id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	prato=Prato.objects.get(id=id)
	menuid=prato.menuid.id
	prato.delete()
	return redirect('configuracao:novoPrato',menuid)

def newPratoRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_tipo': "form-" + str(value-1) + "-tipo",
		'form_prato': "form-" + str(value-1) + "-prato",
		'form_num': "form-" + str(value-1) + "-nrpratosdisponiveis",
		'form_id': 'form-' + str(value-1) + '-id',
	}
	return render(request=request, template_name='configuracao/menuPratoRow.html', context=data)

def getDias(request):
	options = []
	default = {
		'key': '',
		'value': 'Escolha um Dia',
	}
	if request.POST['diaaberto_id'] != '':
		if 'default' in request.POST and request.POST['default'] != 'None':
			if request.POST['typeForm'] == 'menu':
				default = {
					'key': str(Menu.objects.get(id=request.POST['default']).dia),
					'value': str(Menu.objects.get(id=request.POST['default']).dia),
				}
			if request.POST['typeForm'] == 'transporte':
				default = {
					'key': str(Transporte.objects.get(id=request.POST['default']).dia),
					'value': str(Transporte.objects.get(id=request.POST['default']).dia),
				}
		diaaberto = Diaaberto.objects.get(id=request.POST['diaaberto_id'])
		data_inicio = diaaberto.datadiaabertoinicio
		data_fim = diaaberto.datadiaabertofim
		total_dias= data_fim-data_inicio+timedelta(days=1)
		options = diaaberto.days_as_dict()
		
	return render(request = request,
				  template_name='configuracao/dropdown.html',
				  context={'options':options, 'default': default}
				)

class verTransportes(SingleTableMixin, FilterView):

	table_class = TransporteTable
	template_name = 'configuracao/listaTransportes.html'
	filterset_class = TransporteFilter
	table_pagination = {
		'per_page': 10
	}

	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Administrador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["campi"] = list(map(lambda x: (x.nome, x.nome), Campus.objects.all()))
		return context


def criarTransporte(request, id = None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')
	if Diaaberto.current() is None:
		return {'exists': False, 
            'render': render(request=request,
                template_name='mensagem.html',
                context={
                    'tipo':'error',
                    'm':'Crie um dia aberto primeiro!'
                })
            }
	#vars
	transport_by_default = Transporte()
	transport_universitario_default = Transporteuniversitario(transporte=transport_by_default)
	#forms
	HorarioFormSet = transporteHorarioFormset()
	horario_form_set = HorarioFormSet(queryset=Transportehorario.objects.none())
	form_transport = transporteForm()
	form_universitario = transporteUniversitarioForm()

	if id is not None:

		transport_by_default = Transportehorario.objects.get(id=id).transporte
		transport_universitario_default = Transporteuniversitario(transporte=transport_by_default)
		horario_form_set = HorarioFormSet(queryset=Transportehorario.objects.filter(transporte=transport_by_default))
		form_transport = transporteForm(instance=transport_by_default)
		form_universitario = transporteUniversitarioForm(instance=Transporteuniversitario.objects.get(transporte=transport_by_default))

	if request.method == "POST":
		form_transport = transporteForm(request.POST, instance=transport_by_default)
		form_universitario = transporteUniversitarioForm(request.POST, instance=transport_universitario_default)
		horario_form_set = HorarioFormSet(request.POST)
		if form_transport.is_valid() and form_universitario.is_valid() and horario_form_set.is_valid():

			transport = form_transport.save()
			form_universitario.instance.transporte = transport
			form_universitario.save()
			instances = horario_form_set.save(commit=False)

			for instance in instances:
				instance.transporte = transport
				instance.save()

			for instance in horario_form_set.deleted_objects:
				instance.delete()

			return redirect('configuracao:verTransportes')

	return render(request = request,
				template_name='configuracao/criarTransporte.html',
				context={'form_t': form_transport,
						'form_uni': form_universitario,
						'formset': horario_form_set})

def transporteHorarioFormset(extra = 0, minVal = 1):
	formSets = modelformset_factory(model=Transportehorario, exclude = ['transporte','id'],widgets={
			'origem': Select(attrs={'class': 'input'}),
			'chegada': Select(attrs={'class': 'input'}),
			'horaPartida': CustomTimeWidget(attrs={'class': 'input'}),
			'horaChegada': CustomTimeWidget(attrs={'class': 'input'}),
		}, extra = extra, min_num = minVal, can_delete=True)
	return formSets

def newHorarioRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_origem': "form-" + str(value-1) + "-origem",
		'form_chegada': "form-" + str(value-1) + "-chegada",
		'form_horaPartida': "form-" + str(value-1) + "-horaPartida",
		'form_horaChegada': "form-" + str(value-1) + "-horaChegada",
		'form_id': 'form-' + str(value-1) + '-id',
	}
	return render(request=request, template_name='configuracao/transporteHorarioEmptyRow.html', context=data)


def eliminarTransporte(request, id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	Transportehorario.objects.get(id=id).delete()
	return redirect('configuracao:verTransportes')


def atribuirTransporte(request, id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	class ChegadaPartida:
		def __init__(self, id,nparticipantes,local,horario, check):
			self.id=id
			self.nparticipantes=nparticipantes
			self.local= local
			self.horario=horario
			self.check=check

	transportehorario = Transportehorario.objects.get(id=id)
	inscricoesindisponiveis= []
	inscricaotransporte= Inscricaotransporte.objects.filter(transporte=transportehorario.id)
	ocupadas=0
	for ocp in inscricaotransporte:
		ocupadas+=ocp.npassageiros
	#print(ocupadas)
	transportevagas= transportehorario.transporte.transporteuniversitario.capacidade - ocupadas
	inscricoestotais = Inscricao.objects.filter(nalunos__lte=transportevagas,dia=transportehorario.transporte.dia).exclude(hora_chegada = None)
	inscricoes= []
	chepart= 0
	dadoschepart=[]
	for t in inscricaotransporte:
		inscricoesindisponiveis.append(t.inscricao)
	
	for inscricao in inscricoestotais:
		if inscricao not in inscricoesindisponiveis:
					inscricoes.append(inscricao)
		
	for inscricao in inscricoes:
		isessaochegada=Inscricaosessao.objects.filter(inscricao=inscricao).order_by('sessao__horarioid__inicio').first()
		if isessaochegada != None:	
			if isessaochegada.sessao.dia == transportehorario.transporte.dia:
				if transportehorario.origem == "Gambelas" or transportehorario.origem == "Penha":
					isessaopartida=Inscricaosessao.objects.filter(inscricao=inscricao.id).order_by('-sessao__horarioid__inicio').first() # ultima sessao da inscricao
					isessaopartidalocal= isessaopartida.sessao.atividadeid.espacoid.edificio.campus.nome	# campus ultima sessao da inscricao
					isessaopartidahorario= isessaopartida.sessao.horarioid.fim #horario de fim da ultima sessao
					horapartida= (transportehorario.horaPartida.hour*60 + transportehorario.horaPartida.minute) - (isessaopartidahorario.hour*60 + isessaopartidahorario.minute) # diferença entre horario transporte e da ultima sessao
					if isessaopartidalocal == transportehorario.origem  and horapartida <=60 and  horapartida >= 0:
						chepart= ChegadaPartida(inscricao.id, inscricao.nalunos,inscricao.local_chegada, isessaopartidahorario, 1)
				else:
					isessaochegadalocal= isessaochegada.sessao.atividadeid.espacoid.edificio.campus.nome
					horachegada= (transportehorario.horaChegada.hour*60 + transportehorario.horaChegada.minute )- (inscricao.hora_chegada.hour*60 + inscricao.hora_chegada.minute)
					if isessaochegadalocal == transportehorario.chegada and horachegada <=60 and horachegada >=0:
						chepart= ChegadaPartida(inscricao.id,inscricao.nalunos,inscricao.local_chegada,inscricao.hora_chegada, 0)

				dadoschepart.append(chepart)
				dadoschepart=list(dict.fromkeys(dadoschepart))

	

	if request.method == "POST":
		gruposid=request.POST["gruposid"]
		if "new" in request.POST:
			grupo= Inscricao.objects.get(id=gruposid)

			new_inscricaotransporte= Inscricaotransporte(transporte=transportehorario, npassageiros=grupo.nalunos, inscricao= grupo)
			new_inscricaotransporte.save()
			return redirect('configuracao:atribuirTransporte', id)

	return render(request = request,
				  template_name='configuracao/atribuirTransporte.html',
				  context={'transporte': transportehorario,  "inscricoestransporte": inscricaotransporte, "vagas": transportevagas, 'chegadapartida': dadoschepart})

def eliminarAtribuicao(request, id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	transportehorario=Inscricaotransporte.objects.get(id=id).transporte.id
	Inscricaotransporte.objects.get(id=id).delete()
	return redirect('configuracao:atribuirTransporte', transportehorario)

class verEdificios(SingleTableMixin, FilterView):

	table_class = EdificioTable
	template_name = 'configuracao/listaEdificios.html'
	filterset_class = EdificioFilter
	table_pagination = {
		'per_page': 10
	}

	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Administrador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		return super().dispatch(request, *args, **kwargs)
		

	def get_context_data(self, **kwargs):
		context = super(SingleTableMixin, self).get_context_data(**kwargs)
		table = self.get_table(**self.get_table_kwargs())
		table.word = "woooooord"
		context['campi'] = list(map(lambda x: (x.id, x.nome), Campus.objects.all()))
		context[self.get_context_table_name(table)] = table
		return context


def configurarEdificio(request, id = None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	espacoFormSet = modelformset_factory(model=Espaco, form=EspacoForm,extra=0, min_num = 1, can_delete=True)
	formSet = espacoFormSet(queryset=Espaco.objects.none())
	edificio = Edificio()

	if id is not None:
		edificio = Edificio.objects.get(id=id)
		formSet = espacoFormSet(queryset=Espaco.objects.filter(edificio=edificio))
	edificioForm = EdificioForm(instance=edificio)


	if request.method == 'POST':
		edificioForm = EdificioForm(request.POST,request.FILES,instance=edificio)
		formSet = espacoFormSet(request.POST)
		if edificioForm.is_valid() and formSet.is_valid():
			edificio = edificioForm.save()
			instances = formSet.save(commit=False)

			for instance in instances:
				instance.edificio=edificio
				instance.save()

			for instance in formSet.deleted_objects:
				instance.delete()

			return redirect('configuracao:verEdificios')

	return	render(request=request,
				template_name='configuracao/criarEdificio.html',
				context={'form':edificioForm,
						'formset':formSet})

def newEspacoRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_nome': "form-" + str(value-1) + "-nome",
		'form_espaco': "form-" + str(value-1) + "-espaco",
		'form_descricao': "form-" + str(value-1) + "-descricao",
		'form_id': 'form-' + str(value-1) + '-id',
	}
	return render(request=request, template_name='configuracao/edificioEspacoRow.html', context=data)

def eliminarEdificio(request,id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	Edificio.objects.get(id=id).delete()
	return redirect('configuracao:verEdificios')


def verEdificioImagem(request,id = None):

	if id is None:
		return redirect('verEdificios')
	edifi = Edificio.objects.filter(id=id)
	if edifi.exists():
		edifi = Edificio.objects.get(id=id)
		img = edifi.image

	return render(request=request,
				template_name='configuracao/verImagem.html',
				context={'img': img})



class verUOs(SingleTableMixin, FilterView):

	table_class = UOTable
	template_name = 'configuracao/listaUO.html'
	filterset_class = UOFilter
	table_pagination = {
		'per_page': 10
	}

	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Administrador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		return super().dispatch(request, *args, **kwargs)
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["campi"] = list(map(lambda x: (x.id, x.nome), Campus.objects.all()))
		return context


def configurarUO(request, id = None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	uOformSet = uOFormset()
	uOforms = uOformSet(queryset=Unidadeorganica.objects.none())
	uO = Unidadeorganica()
	allowMore = True
	allowDelete = True

	if id is not None:
		uO = Unidadeorganica.objects.get(id=id)
		uOforms = uOformSet(queryset=Unidadeorganica.objects.filter(id=uO.id))
		allowMore, allowDelete = False, False	

	if(request.method == 'POST'):
		uOforms = uOformSet(request.POST)
		if uOforms.is_valid():
			uOforms.save()
			return redirect('configuracao:verUOs')
	return render(request=request,
				template_name='configuracao/criarUOs.html',
				context={'formset': uOforms,
					'allowMore': allowMore,
					'allowDelete': allowDelete,
				})

def uOFormset(extra = 0, minVal = 1):
	formSets = modelformset_factory(model=Unidadeorganica, exclude = ['id'],widgets={
			'nome': TextInput(attrs={'class': 'input'}),
			'sigla': TextInput(attrs={'class': 'input'}),
			'campusid': Select(attrs={'class': 'input'}),
		}, extra = extra, min_num = minVal, can_delete=True)
	return formSets

def newUORow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_nome': "form-" + str(value-1) + "-nome",
		'form_sigla': "form-" + str(value-1) + "-sigla",
		'form_campusid': 'form-' + str(value-1) + '-campusid',
		'form_id': 'form-' + str(value-1) + '-id',
	}
	return render(request=request, template_name='configuracao/UORow.html', context=data)

def eliminarUO(request, id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	Unidadeorganica.objects.filter(id=id).delete()
	return redirect('configuracao:verUOs')

class verDepartamentos(SingleTableMixin, FilterView):

	table_class = DepartamentoTable
	template_name = 'configuracao/listaDepartamento.html'
	filterset_class = DepartamentoFilter
	table_pagination = {
		'per_page': 10
	}

	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Administrador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		return super().dispatch(request, *args, **kwargs)
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["facs"] = list(map(lambda x: (x.id, x.nome), Unidadeorganica.objects.all()))
		return context


def configurarDepartamento(request, id = None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	departamentoformSet = departamentoFormset()
	departamentoforms = departamentoformSet(queryset=Departamento.objects.none())
	departamento = Departamento()
	allowMore = True
	allowDelete = True

	if id is not None:
		departamento = Departamento.objects.get(id=id)
		departamentoforms = departamentoformSet(queryset=Departamento.objects.filter(id=departamento.id))
		allowMore, allowDelete = False, False	

	if(request.method == 'POST'):
		departamentoforms = departamentoformSet(request.POST)
		if departamentoforms.is_valid():
			objectDep = departamentoforms.save()
			return redirect('configuracao:verDepartamentos')
	return render(request=request,
				template_name='configuracao/criarDepartamentos.html',
				context={'formset': departamentoforms,
					'allowMore': allowMore,
					'allowDelete': allowDelete,
				})

def departamentoFormset(extra = 0, minVal = 1):
	formSets = modelformset_factory(model=Departamento, exclude = ['id'],widgets={
			'nome': TextInput(attrs={'class': 'input'}),
			'sigla': TextInput(attrs={'class': 'input'}),
			'unidadeorganicaid': Select(attrs={'class': 'input'}),
		}, extra = extra, min_num = minVal, can_delete=True)
	return formSets

def newDepartamentoRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_nome': "form-" + str(value-1) + "-nome",
		'form_sigla': "form-" + str(value-1) + "-sigla",
		'form_unidadeorganicaid': 'form-' + str(value-1) + '-unidadeorganicaid',
		'form_id': 'form-' + str(value-1) + '-id',
		'options': Unidadeorganica.objects.all()
	}
	return render(request=request, template_name='configuracao/departamentoRow.html', context=data)

def eliminarDepartamento(request, id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	Departamento.objects.filter(id=id).delete()
	return redirect('configuracao:verDepartamentos')

class verCursos(SingleTableMixin, FilterView):

	table_class = CursoTable
	template_name = 'configuracao/listaCurso.html'
	filterset_class = CursoFilter
	table_pagination = {
		'per_page': 10
	}

	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Administrador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		return super().dispatch(request, *args, **kwargs)
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["faculdades"] = list(map(lambda x: (x.id, x.nome), Unidadeorganica.objects.all()))
		return context


def configurarCurso(request, id = None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	departamentoformSet = cursoFormSet()
	departamentoforms = departamentoformSet(queryset=Curso.objects.none())
	departamento = Curso()
	allowMore = True
	allowDelete = True

	if id is not None:
		departamento = Curso.objects.get(id=id)
		departamentoforms = departamentoformSet(queryset=Curso.objects.filter(id=departamento.id))
		allowMore, allowDelete = False, False	

	if(request.method == 'POST'):
		departamentoforms = departamentoformSet(request.POST)
		if departamentoforms.is_valid():
			departamentoforms.save()
			return redirect('configuracao:verCursos')
	return render(request=request,
				template_name='configuracao/criarCursos.html',
				context={'formset': departamentoforms,
					'allowMore': allowMore,
					'allowDelete': allowDelete,
				})

def cursoFormSet(extra = 0, minVal = 1):
	formSets = modelformset_factory(model=Curso, exclude = ['id'],widgets={
			'nome': TextInput(attrs={'class': 'input'}),
			'sigla': TextInput(attrs={'class': 'input'}),
			'unidadeorganicaid': Select(attrs={'class': 'input'}),
		}, extra = extra, min_num = minVal, can_delete=True)
	return formSets

def newCursoRow(request):
	value = int(request.POST.get('extra'))
	data = {
		'form_nome': "form-" + str(value-1) + "-nome",
		'form_sigla': "form-" + str(value-1) + "-sigla",
		'form_unidadeorganicaid': 'form-' + str(value-1) + '-unidadeorganicaid',
		'form_id': 'form-' + str(value-1) + '-id',
		'options': Unidadeorganica.objects.all()
	}
	return render(request=request, template_name='configuracao/departamentoRow.html', context=data)

def eliminarCurso(request, id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	Curso.objects.filter(id=id).delete()
	return redirect('configuracao:verCursos')


class verTemasQuestionario(SingleTableMixin, FilterView):

	table_class = TemaQuestionarioTable	
	template_name = 'configuracao/listaTemasQuestionario.html' 
	filterset_class = TemaQuestionarioFilter		
	table_pagination = {
		'per_page': 10
	}
	
	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Administrador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		return super().dispatch(request, *args, **kwargs)

def configurarTemasQuestionario(request, id = None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	tema = TemaQuestionario()

	if id is not None:
		tema = TemaQuestionario.objects.get(id=id)
	temaForm = TemaQuestionarioForm(instance=tema)


	if request.method == 'POST':
		temaForm = TemaQuestionarioForm(data=request.POST,instance=tema)
		if temaForm.is_valid():
			tema = temaForm.save()
			return redirect('configuracao:verTemasQuestionario')

	return	render(request=request,
				template_name='configuracao/criarTemaQuestionario.html',
				context={'form':temaForm})

def eliminarTemaQuestionario(request,id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	TemaQuestionario.objects.get(id=id).delete()
	return redirect('configuracao:verTemasQuestionario')


class verTemas(SingleTableMixin, FilterView):

	table_class = TemaTable
	template_name = 'configuracao/listaTemas.html'
	filterset_class = TemaFilter
	table_pagination = {
		'per_page': 10
	}
	def dispatch(self, request, *args, **kwargs):
		user_check_var = user_check(request=request, user_profile=[Administrador])
		if not user_check_var.get('exists'): return user_check_var.get('render')
		return super().dispatch(request, *args, **kwargs)



def configurarTema(request, id = None):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	tema = Tema()

	if id is not None:
		tema = Tema.objects.get(id=id)
	temaForm = TemaForm(instance=tema)


	if request.method == 'POST':
		temaForm = TemaForm(data=request.POST,instance=tema)
		if temaForm.is_valid():
			tema = temaForm.save()
			return redirect('configuracao:verTemas')

	return	render(request=request,
				template_name='configuracao/criarTema.html',
				context={'form':temaForm})

def eliminarTema(request,id):

	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	Tema.objects.get(id=id).delete()
	return redirect('configuracao:verTemas')

def relatoriosTransportes(request):
	user_check_var = user_check(request=request, user_profile=[Administrador])
	if user_check_var.get('exists') == False: return user_check_var.get('render')

	anos = Diaaberto.objects.values_list('ano', flat=True).distinct()
	print(anos)
	
	context = {'anos': anos}
	return render(request=request, template_name="configuracao/relatorio_transportes.html", context=context)


def dias_disponiveis(request):
	ano_selecionado = request.POST.get("ano")

	default = {
        'key': '',
        'value': 'Selecione o dia'
    }

	print(ano_selecionado)

	if ano_selecionado:
		dias = Transporte.objects.filter(diaaberto__ano=ano_selecionado).values_list('dia', flat=True).distinct()
		print(dias)
		options = '<option value="">Selecione o dia</option>'
		options = []
		for dia in dias:
			options.append({'key': dia.strftime('%Y-%m-%d'), 'value': dia})
			print(dias)
	else:
		dias = []
		print("ardeu")
		return render(request=request, 
                template_name="configuracao/dropdown.html", 
                context={"options": options,    "default": default})
	
def relatoriosTransportesPDF(request):
    """ View que gera um PDF com os detalhes da inscrição """
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    ano = request.POST.get('ano')
    dia = request.POST.get('dia')
  
    Transportes = Transportehorario.objects.all()
    print(Transportes)

    if ano:
        Transportes = Transportes.filter(transporte__diaaberto__ano=ano)
        print(ano)

    if dia:
        Transportes = Transportes.filter(transporte__dia=dia)
		
    context = {
        'request': request,
        'Transportes': Transportes,
    }
    return render_pdf("configuracao/relatorio_transportes_pdf.html", context, f"Transportes.pdf")


def relatoriosTransportesCSV(request):
    # Obtenha os dados de transporte do banco de dados
    transportes = Transportehorario.objects.all()

    # Crie o objeto HttpResponse com o tipo de conteúdo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="relatorio_transportes.csv"'

    # Crie o escritor CSV usando o objeto de resposta
    writer = csv.writer(response, delimiter=';')

    # Escreva o cabeçalho do CSV
    writer.writerow([
        'Autocarro ID', 'Hora Partida', 'Hora Chegada', 'Origem', 'Dia'
    ])

    # Escreva os dados de cada transporte
    for transporte in transportes:
        writer.writerow([
            transporte.transporte.identificador,
            transporte.horaPartida.strftime("%H:%M") if transporte.horaPartida else '',
            transporte.horaChegada.strftime("%H:%M") if transporte.horaChegada else '',
            transporte.origem,
            transporte.transporte.dia.strftime("%d/%m/%Y")  # Assumindo que 'dia' é uma data
        ])

    return response
