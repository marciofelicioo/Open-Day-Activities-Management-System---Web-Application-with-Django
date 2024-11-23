import csv
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from inscricoes.utils import render_pdf  
from .forms import AtividadeForm , MateriaisForm, RoteiroForm
from django.views.generic.edit import CreateView
from .models import *
from configuracao.models import Horario
from .models import Atividade, Sessao, Tema, Materiais
from utilizadores.models import Administrador, Coordenador, ProfessorUniversitario
from configuracao.models import Campus, Departamento, Diaaberto, Edificio, Espaco, Horario, Unidadeorganica
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime, date,timezone
from _datetime import timedelta
from django.db.models import Q
from django.core import serializers
from django.forms.models import modelformset_factory
from django.forms.widgets import Select


from notificacoes import views as nviews
from utilizadores.views import user_check
from coordenadores.models import TarefaAuxiliar
from atividades.tables import *
from atividades.filters import *
from django_tables2 import SingleTableMixin, SingleTableView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin


class AtividadesProfessor(SingleTableMixin, FilterView):
    
    table_class = ProfAtividadesTable
    template_name = 'atividades/minhasAtividades.html'
    filterset_class = ProfAtividadesFilter
    table_pagination = {
		'per_page': 10
	}
    

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[ProfessorUniversitario])
        if not user_check_var.get('exists'): return user_check_var.get('render')
        self.user_check_var = user_check_var
        return super().dispatch(request, *args, **kwargs)
        
    def get_queryset(self):
        return Atividade.objects.filter(professoruniversitarioutilizadorid=self.user_check_var.get('firstProfile')).order_by('-id').exclude(estado="nsub")
    


class Conflito:
    def __init__(self, atividade1,atividade2):
        self.atividade1=atividade1
        self.atividade2=atividade2
        
class AtividadesCoordenador(SingleTableMixin, FilterView):
    
    table_class = CoordAtividadesTable
    template_name = 'atividades/atividadesUOrganica.html'
    filterset_class = CoordAtividadesFilter
    table_pagination = {
		'per_page': 10
	}
    
    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[Coordenador])
        if not user_check_var.get('exists'): return user_check_var.get('render')
        self.user_check_var = user_check_var
        today= datetime.now(timezone.utc) - timedelta(hours=1, minutes=00)
        Atividade.objects.filter(estado="nsub",datasubmissao__lte=today).delete()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Atividade.objects.filter(professoruniversitarioutilizadorid__faculdade=self.user_check_var.get('firstProfile').faculdade).order_by('-id').exclude(estado="nsub")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())

        #Everything below goes to details
        table.conflitos = conflict_array()
        #This goes to un-detailed view
        context["deps"] = list(map(lambda x: (x.id, x.nome), Departamento.objects.filter(unidadeorganicaid=self.user_check_var.get('firstProfile').faculdade)))
        #----------
    
        context[self.get_context_table_name(table)] = table
        return context


class AtividadesAdmin(SingleTableMixin, FilterView):
    
    table_class = AdminAtividadesTable
    template_name = 'atividades/atividadesAdmin.html'
    filterset_class = AdminAtividadesFilter
    table_pagination = {
		'per_page': 10
	}
    
    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[Administrador])
        if not user_check_var.get('exists'): return user_check_var.get('render')
        self.user_check_var = user_check_var
        today= datetime.now(timezone.utc) - timedelta(hours=1, minutes=00)
        Atividade.objects.filter(estado="nsub",datasubmissao__lte=today).delete()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Atividade.objects.all().order_by('-id').exclude(estado="nsub")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())

        #Everything below goes to details
        table.conflitos = conflict_array()
        #This goes to un-detailed view
        context["deps"] = list(map(lambda x: (x.id, x.nome), Departamento.objects.all()))
        context["uos"] = list(map(lambda x: (x.id, x.nome), Unidadeorganica.objects.all()))
        context["campus"] = list(map(lambda x: (x.id, x.nome), Campus.objects.all()))
        #----------
    
        context[self.get_context_table_name(table)] = table
        return context






def conflict_array():
    sessoes=Sessao.objects.all().exclude(atividadeid__estado = 'nsub')
    sessoes= sessoes.exclude(atividadeid__estado = 'Recusada')
    sessoes=sessoes.exclude(atividadeid=None)
    conflito2= []
    for sessao1 in sessoes:
        for sessao2 in sessoes:
            if sessao1.id!=sessao2.id and sessao1.atividadeid!= sessao2.atividadeid and sessao1.atividadeid.espacoid == sessao2.atividadeid.espacoid and sessao1.dia == sessao2.   dia:     
                    hora1inicio=sessao1.horarioid.inicio.hour*60+sessao1.horarioid.inicio.minute
                    hora1fim=sessao1.horarioid.fim.hour*60+sessao1.horarioid.fim.minute
                    hora2inicio=sessao2.horarioid.inicio.hour*60+sessao2.horarioid.inicio.minute
                    hora2fim=sessao2.horarioid.fim.hour*60+sessao2.horarioid.fim.minute
                    if hora1inicio<=hora2inicio < hora1fim or hora1inicio< hora2fim <= hora1fim:
                        C1=Conflito(sessao1,sessao2)
                        conflito2.append(C1)
    conflito2= list(dict.fromkeys(conflito2))
    return conflito2


def alterarAtividade(request,id):
    user_check_var = user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    atividadecheck= atividade.first()
    sessoes= Sessao.objects.filter(atividadeid=atividadecheck)
    for sessao in sessoes:
        if sessao.vagas != atividadecheck.participantesmaximo:
            return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })

    if atividade.exists():  
        activity_object = Atividade.objects.get(id=id) #Objecto da atividade que temos de mudar, ativdade da dupla
        if activity_object.professoruniversitarioutilizadorid != ProfessorUniversitario.objects.get(utilizador_ptr_id = request.user.id):
            return redirect("utilizadores:home")
        #------atividade a alterar----
        activity_object = Atividade.objects.get(id=id) #Objecto da atividade que temos de mudar, ativdade da dupla
        activity_object_form = AtividadeForm(instance=activity_object) #Formulario instanciado pela atividade a mudar
        espaco= Espaco.objects.get(id=activity_object.espacoid.id)
        materiais_object= Materiais.objects.get(atividadeid=id)
        new_material = Materiais(atividadeid=activity_object, nomematerial= materiais_object)
        materiais_object_form= MateriaisForm(instance=materiais_object)
        campusid= espaco.edificio.campus.id
        campus= Campus.objects.all().exclude(id=campusid)

        edificioid= espaco.edificio.id
        edificios= Edificio.objects.filter(campus=campusid).exclude(id=edificioid)

        espacos= Espaco.objects.filter(edificio=edificioid).exclude(id=espaco.id)
        #print(espaco)
        #print(espacos)
        #-----------------------------
        if request.method == 'POST':    #Se estivermos a receber um request com formulario  
            submitted_data = request.POST.copy()
            activity_object.tema = Tema.objects.get(id=int(request.POST['tema']))
            activity_object_form = AtividadeForm(submitted_data, instance=activity_object)
            materiais_object_form = MateriaisForm(request.POST, instance=materiais_object)
            if activity_object_form.is_valid() and materiais_object_form.is_valid():
                
                    #-------Guardar as mudancas a atividade em si------
                    activity_object_formed = activity_object_form.save(commit=False) 
                    espacoid=request.POST["espacoid"] 
                    espaco=Espaco.objects.get(id=espacoid) 
                    activity_object_formed.espacoid= espaco
                    if  activity_object_formed.estado == "nsub":
                        activity_object_formed.estado = "nsub"
                        activity_object_formed.save()
                        materiais_object_form.save()
                        sessoes= Sessao.objects.filter(atividadeid= activity_object_formed)
                        print(sessoes)
                        for sessao in sessoes:
                            inicio= str(sessao.horarioid.inicio)
                            splitinicio=inicio.split(":")
                            print(splitinicio)
                            duracaoesperada= activity_object_formed.duracaoesperada
                            hfim= horariofim(splitinicio,duracaoesperada)
                            horario= Horario.objects.filter(inicio= sessao.horarioid.inicio, fim=hfim).first()
                            if horario is None:
                                new_Horario= Horario(inicio=inicio, fim=hfim)
                                new_Horario.save()
                            else:
                                new_Horario= horario
                            sessao.horarioid=Horario.objects.get(id=new_Horario.id)
                            sessao.vagas= activity_object_formed.participantesmaximo
                            sessao.save()
                    else:
                        print("hello")
                        print(Atividade.objects.get(id=id) == activity_object_formed)
                        if Atividade.objects.get(id=id).ne(activity_object_formed) or Materiais.objects.get(atividadeid=id).ne(materiais_object_form.instance):
                            espacoid=request.POST["espacoid"] 
                            espaco=Espaco.objects.get(id=espacoid) 
                            activity_object_formed.espacoid= espaco
                            activity_object_formed.estado = "Pendente"
                            activity_object_formed.dataalteracao = datetime.now()
                            activity_object_formed.save()
                            materiais_object_form.save()
                            sessoes= Sessao.objects.filter(atividadeid= activity_object_formed)
                            print(sessoes)
                            for sessao in sessoes:
                                inicio= str(sessao.horarioid.inicio)
                                splitinicio=inicio.split(":")
                                print(splitinicio)
                                duracaoesperada= activity_object_formed.duracaoesperada
                                hfim= horariofim(splitinicio,duracaoesperada)
                                horario= Horario.objects.filter(inicio= sessao.horarioid.inicio, fim=hfim).first()
                                if horario is None:
                                    new_Horario= Horario(inicio=inicio, fim=hfim)
                                    new_Horario.save()
                                else:
                                    new_Horario= horario
                                sessao.horarioid=Horario.objects.get(id=new_Horario.id)
                                sessao.vagas= activity_object_formed.participantesmaximo
                                sessao.save()
                    #nviews.enviar_notificacao_automatica(request,"atividadeAlterada",activity_object_formed.id) #Enviar Notificacao Automatica !!!!!!
                    return redirect('atividades:inserirSessao',id)          
        return render(request=request,
                        template_name='atividades/proporAtividadeAtividade.html',
                        context={'form': activity_object_form, 'espaco':espaco,'espacos':espacos, "edificios": edificios, "campus":campus, "materiais":materiais_object_form}
                        )
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })

def eliminarAtividade(request,id):
    user_check_var = user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    atividadecheck= atividade.first()
    sessoes= Sessao.objects.filter(atividadeid=atividadecheck)
    for sessao in sessoes:
        if sessao.vagas != atividadecheck.participantesmaximo:
            return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })

    if atividade.exists():
        nviews.enviar_notificacao_automatica(request,"atividadeApagada",id) #Enviar Notificacao Automatica !!!!!!
        atividade.delete()
        return redirect('atividades:minhasAtividades')
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })
    



def eliminarSessao(request,id):
    user_check_var = user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')
    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    sessoes = Sessao.objects.filter(id=id,atividadeid__professoruniversitarioutilizadorid=userId)

        

    if sessoes.exists():
        sessaor=sessoes.first()
        if sessaor.vagas != sessaor.atividadeid.participantesmaximo:
            return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })
        atividadeid= sessaor.atividadeid.id
        sessaor.delete()
        return redirect('atividades:inserirSessao',atividadeid)
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })


def proporatividade(request):
    
    user_check_var = user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    today= datetime.now(timezone.utc) 
    diaabertopropostas=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)

    
    diainicio= diaabertopropostas.datadiaabertoinicio.date()
    diafim= diaabertopropostas.datadiaabertofim.date()
    totaldias= diafim-diainicio+timedelta(days=1)
    dias_diaaberto= []
    for d in range(totaldias.days):
        dias_diaaberto.append(diainicio+timedelta(days=d))

    sessoes= ""
    if request.method == "POST":
        
        activity_object_form = AtividadeForm(request.POST)
        material_object_form= MateriaisForm(request.POST)

        espacoid=request.POST["espacoid"] 
        espaco=Espaco.objects.get(id=espacoid)  
        new_form = Atividade(professoruniversitarioutilizadorid = ProfessorUniversitario.objects.get(utilizador_ptr_id = request.user.id),
                             estado = "nsub", diaabertoid = diaabertopropostas,espacoid= Espaco.objects.get(id=espaco.id),
                             tema=Tema.objects.get(id=request.POST['tema']))
        activity_object_form = AtividadeForm(request.POST, instance=new_form)
        if activity_object_form.is_valid():  
            activity_object_formed= activity_object_form.save()
            new_material= Materiais(atividadeid=activity_object_formed)
            material_object_form= MateriaisForm(request.POST, instance= new_material)
            material_object_form.save()
            return redirect('atividades:inserirSessao', activity_object_formed.id)
    else:
        material_object_form= MateriaisForm() 
        activity_object_form= AtividadeForm()
    return render(request,'atividades/proporAtividadeAtividade.html',{'form': activity_object_form,'campus': Campus.objects.all(),"materiais": material_object_form
                            })




def horariofim(inicio,duracao):
    calculo= int(inicio[0])*60+ int(inicio[1])+duracao
    hora=int(calculo/60)
    minutos= int(calculo%60)
    fim= str(hora)+":"+str(minutos)
    return fim

def inserirsessao(request,id):

    user_check_var = user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    atividadecheck= atividade.first()
    sessoes= Sessao.objects.filter(atividadeid=atividadecheck)
    for sessao in sessoes:
        if sessao.vagas != atividadecheck.participantesmaximo:
            return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })

    if atividade.exists():  
        today= datetime.now(timezone.utc) 
        diaaberto=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today)
        diainicio= diaaberto.datadiaabertoinicio.date()
        diafim= diaaberto.datadiaabertofim.date()
        totaldias= diafim-diainicio+timedelta(days=1)
        dias_diaaberto= []
        for d in range(totaldias.days):
            dias_diaaberto.append(diainicio+timedelta(days=d))
        horariosindisponiveis= []
        disp= []
        atividadeid=Atividade.objects.get(id=id)
        sessoes=Sessao.objects.all().filter(atividadeid=id)
        check= len(sessoes)
        if request.method == "POST":
            if 'new' in request.POST:
                diasessao=request.POST["diasessao"]
                print(diasessao)
                inicio= request.POST['horarioid']
                splitinicio=inicio.split(":")
                print(splitinicio)
                duracaoesperada= atividadeid.duracaoesperada
                hfim= horariofim(splitinicio,duracaoesperada)
                horario= Horario.objects.filter(inicio= request.POST['horarioid'], fim=hfim).first()
                if horario is None:
                    new_Horario= Horario(inicio=inicio, fim=hfim)
                    new_Horario.save()
                else:
                    new_Horario= horario
                new_Sessao= Sessao(vagas=Atividade.objects.get(id= id).participantesmaximo,ninscritos=0 ,horarioid=Horario.objects.get(id=new_Horario.id), atividadeid=Atividade.objects.get(id=id),dia=diasessao)
                if atividadeid.estado != "nsub":
                    atividadeid.estado= "Pendente"
                atividadeid.save()
                new_Sessao.save()
                return redirect('atividades:inserirSessao', id)
        return render(request=request,
                      template_name='atividades/proporAtividadeSessao.html',
                      context={'horarios': "" , 
                               'sessions_activity': Sessao.objects.all().filter(atividadeid= id), 
                               'dias': dias_diaaberto,
                               'check': check, "id":id})
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })    


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




def veredificios(request):
    campus=request.POST["valuecampus"]
    edificios = Edificio.objects.filter(campus=campus)
    print(request.POST["valuecampus"])
    print(edificios)
    return render(request, template_name="atividades/generic_list_options.html", context={"default": "Escolha um Edificio","generic": edificios})

def versalas(request):
    edificios=request.POST["valueedificio"]
    print(request.POST["valueedificio"])
    salas = Espaco.objects.filter(edificio=edificios)
    return render(request, template_name="atividades/generic_list_options.html", context={"default": "Escolha uma Sala","generic": salas})


class Chorarios:
    def __init__(self, inicio,fim):
        self.inicio=inicio
        self.fim=fim


def verhorarios(request):
    horarios=[]
    #horarioindisponivel = request.POST['horarioindisponivel[]']
    #print(horarioindisponivel)
    today = datetime.now(timezone.utc)

    default = {
        'key': '',
        'value': 'Escolha um horario'
    }

    diasessao=request.POST["valuedia"]
    id= request.POST["id"]
    print(id)
    if id != -1:
        sessaodia=Sessao.objects.filter(atividadeid=id, dia=diasessao)

        print(sessaodia)
        horar= []
        horariosindisponiveis= []
        horar2= []
        horar3= []
        escala=Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today).escalasessoes.minute
        print(escala)
        if len(sessaodia)==0:
            options = [{
            'key': str(session_time),
            'value': str(session_time),
            } for session_time in Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today).session_times()]
        else:
            for sessao in sessaodia:
                timeinicio= TimeC(time=str(sessao.horarioid.inicio.hour)+":"+str(sessao.horarioid.inicio.minute))
                timefim= TimeC(time=str(sessao.horarioid.fim.hour)+":"+str(sessao.horarioid.fim.minute))    
                hor= Chorarios(timeinicio,timefim)
                horariosindisponiveis.append(hor)
            #print(horariosindisponiveis)
            
            for session_time in Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today).session_times():
                timelist= TimeC(time=str(session_time))
                horar.append(timelist)

        
            #print(horar)
            for h in horar:             
                for s in horariosindisponiveis:
                    print("inicio:"+ str(s.inicio) )
                    if h >= s.inicio and h < s.fim:
                        horar2.append(h)

            for h in horar:
                if h not in horar2:
                    horar3.append(h)
            options = [{
                'key': str(session_time),
                'value': str(session_time),
            } for session_time in horar3]

    else:       
        options = [{
            'key': str(session_time),
            'value': str(session_time),
        } for session_time in Diaaberto.objects.get(datapropostasatividadesincio__lte=today,dataporpostaatividadesfim__gte=today).session_times()]

    return render(request=request, 
                template_name="configuracao/dropdown.html", 
                context={"options": options,    "default": default})


def validaratividade(request,id, action):

    user_check_var = user_check(request=request, user_profile=[Coordenador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    atividade=Atividade.objects.get(id=id)
    if action==0:
        nviews.enviar_notificacao_automatica(request,"rejeitarAtividade",id) #Enviar Notificacao Automatica !!!!!!
        atividade.estado='Recusada'
    if action==1:
        nviews.enviar_notificacao_automatica(request,"confirmarAtividade",id) #Enviar Notificacao Automatica !!!!!!
        atividade.estado='Aceite'
    atividade.save()
    return redirect('atividades:atividadesUOrganica')


def verresumo(request,id):

    user_check_var = user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    atividadecheck= atividade.first()
    sessoes= Sessao.objects.filter(atividadeid=atividadecheck)
    for sessao in sessoes:
        if sessao.vagas != atividadecheck.participantesmaximo:
            return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })

    if atividade.exists():  
        atividade= Atividade.objects.get(id=id)
        material= Materiais.objects.filter(atividadeid = atividade).first()
        nsub= 0
        if atividade.estado == "nsub":
            nsub= 1
        print(nsub)
        if request.method == "POST":
            if 'anterior' in request.POST:
                return redirect('atividades:inserirSessao', id)
        sessions_activity= Sessao.objects.filter(atividadeid=atividade)
        return render(request=request, 
                    template_name="atividades/resumo.html",  context={"atividade": atividade, "sessions_activity": sessions_activity, "nsub": nsub , "material": material} )
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })


def confirmarResumo(request,id):
    user_check_var = user_check(request=request, user_profile=[ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    atividade = Atividade.objects.filter(id=id,professoruniversitarioutilizadorid=userId)

    atividadecheck= atividade.first()
    sessoes= Sessao.objects.filter(atividadeid=atividadecheck)
    for sessao in sessoes:
        if sessao.vagas != atividadecheck.participantesmaximo:
            return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })

    if atividade.exists():  
        atividade= Atividade.objects.get(id=id)
        if atividade.estado == "nsub":
            atividade.estado= "Pendente"
            atividade.save()
            print(atividade.id)
            nviews.enviar_notificacao_automatica(request,"validarAtividades",atividade.id) #Enviar Notificacao Automatica !!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            nviews.enviar_notificacao_automatica(request,"atividadeAlterada",atividade.id) #Enviar Notificacao Automatica !!!!!!
        return redirect("atividades:minhasAtividades")
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })
def is_int(value):
    try:
        val = int(value)
        return val
    except:
        return False

def verdeps(request):
    value_uo = request.POST.get("value_uo")
    value_dep = request.POST.get('value_dep')
    print(value_dep)
    value_uo = is_int(value_uo)
    if value_uo != 'None' and value_uo is not None and value_uo is not False:
        uo= Unidadeorganica.objects.filter(id=value_uo).first()
        departamentos= Departamento.objects.filter(unidadeorganicaid=  uo)
    else:
        departamentos= Departamento.objects.all()

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

    
def verfaculdades(request):
    value_campus = request.POST.get('value_campus')
    value_uo = request.POST.get('value_uo')
    print(value_campus)
    value_campus = is_int(value_campus)
    if value_campus != 'None' and value_campus is not None and value_campus is not False:
        campus= Campus.objects.filter(id=value_campus).first()
        print(campus)
        faculdades = Unidadeorganica.objects.filter(campusid= campus)
    else:
        faculdades= Unidadeorganica.objects.all()

    uos= []
    for uo in faculdades:    
        uos.append({'key': uo.id ,'value': uo.nome})
    value_uo = is_int(value_uo)
    default= {}
    if value_uo != 'None' and value_uo is not None and value_uo is not False:
        uo= Unidadeorganica.objects.get(id=value_uo)
        default={
                    'key': uo.id,
                    'value': uo.nome
        } 
    else:
        default={
                        'key': "",
                        'value': "Qualquer Faculdade"
            } 
    return render(request=request,template_name='configuracao/dropdown.html',context={'options':uos, 'default': default})  


class ConsultarRoteiros(SingleTableMixin, FilterView):
    table_class = RoteiroTable  # Substitua RoteiroTable pelo nome da sua tabela de roteiros
    template_name = 'atividades/consultar_roteiros.html'  # Substitua 'consultarroteiro.html' pelo nome do seu template
    filterset_class = RoteiroFilter  # Substitua RoteiroFilter pelo nome da sua classe de filtro de roteiros
    table_pagination = {
		'per_page': 10
	}

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[Coordenador, Administrador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        self.user = user_check_var.get('firstProfile')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Se o usuário for um administrador, retorne todos os roteiros
        if isinstance(self.user, Administrador):
            queryset = Roteiro.objects.all().order_by('-created_at')
        # Se for um coordenador, retorne apenas os roteiros associados a ele
        else:
            queryset = Roteiro.objects.filter(coord=self.user).order_by('-created_at')
        # Filtro adicional para mostrar apenas os roteiros do ano de 2024 inicialmente
        if not self.request.GET and Diaaberto.current():
            queryset = queryset.filter(ano=datetime.now().year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        context["is_open"] = True if Diaaberto.current() is not None else False
        context[self.get_context_table_name(table)] = table
        if not isinstance(self.user, Administrador):
            table.columns.hide('coord')
        return context

def verDetalheRoteiro(request, id):
    user_check_var = user_check(request=request, user_profile=[Coordenador, Administrador])
    if not user_check_var.get('exists'): return user_check_var.get('render')
    roteiro = Roteiro.objects.get(id=id)

    context={"roteiro": roteiro}
    return render(request=request, template_name="atividades/verDetalheRoteiro.html", context=context)

def criar_roteiro(request):
    user_check_var = user_check(request=request, user_profile=[Coordenador, Administrador])
    if not user_check_var.get('exists'): return user_check_var.get('render')
    # ano = datetime.now().year
    dia_aberto = Diaaberto.current()
    diainicio= dia_aberto.datadiaabertoinicio.date()
    diafim= dia_aberto.datadiaabertofim.date()
    totaldias= diafim-diainicio+timedelta(days=1)
    dias_diaaberto= []
    for d in range(totaldias.days):
        dias_diaaberto.append(diainicio+timedelta(days=d))
    if request.method == 'POST':
        form = RoteiroForm(request.POST)
        if form.is_valid():
            # Salvando o roteiro, mas não o commitando ainda
            roteiro = form.save(commit=False)
            coord = Coordenador.objects.get(id=request.user.id)
            ano = dia_aberto.ano
            roteiro.coord = coord
            roteiro.diaabertoid = dia_aberto
            roteiro.ano = ano
            # Salvando o roteiro com o horário definido
            roteiro.save()

            
            inicio = form.cleaned_data['inicio']
            fim = form.cleaned_data['fim']
            horario = Horario.objects.create(inicio=inicio, fim=fim)
            Sessao.objects.create(
                ninscritos = 0,
                vagas = form.cleaned_data['nparticipantes'],
                roteiroid = roteiro,
                dia = form.cleaned_data['diasessao'],
                horarioid = horario,
            )

            # Redirecionar para alguma página de sucesso ou outra ação necessária
            return redirect('atividades:adicionarAtividades', roteiro.id)
        else:
            # Se o formulário não for válido, renderize o formulário novamente com os erros
            context = {'form': form, 'dia_aberto': dia_aberto, 'dias': dias_diaaberto}
            # Adicione um contexto para os erros do formulário
            context['errors'] = form.errors
            return render(request, 'atividades/criar_roteiro.html', context)
    else:
        form = RoteiroForm()
    
    context = {'form': form, 'dia_aberto': dia_aberto, 'dias': dias_diaaberto}
    return render(request, 'atividades/criar_roteiro.html', context)

def adicionar_atividades(request, id):
    user_check_var = user_check(request=request, user_profile=[Coordenador, Administrador])
    if not user_check_var.get('exists'): return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    coordenador = Coordenador.objects.get(pk=userId)
    roteiro = Roteiro.objects.filter(id=id,coord=userId)

    if roteiro.exists(): 
        diaaberto=Diaaberto.current()
        diainicio= diaaberto.datadiaabertoinicio.date()
        diafim= diaaberto.datadiaabertofim.date()
        totaldias= diafim-diainicio+timedelta(days=1)
        dias_diaaberto= []
        for d in range(totaldias.days):
            dias_diaaberto.append(diainicio+timedelta(days=d))
        sessoesRoteiro = Sessao.objects.filter(roteiroid=id)

        for sessao in sessoesRoteiro:
            if sessao.dia in dias_diaaberto:
                dias_diaaberto.remove(sessao.dia)


        departamento_coordenador = coordenador.departamento
        roteiroid=Roteiro.objects.get(id=id)
        atividadesRoteiro=AtividadeRoteiro.objects.all().filter(roteiro=id)
        atividades = Atividade.objects.all().filter(estado="Aceite",
                                                    professoruniversitarioutilizadorid__departamento=departamento_coordenador,
                                                    diaabertoid=Diaaberto.current()).exclude(id__in=atividadesRoteiro.values_list('atividade__id', flat=True))  
    
        sessaoRoteiro = Sessao.objects.filter(roteiroid=id).first()    
        # Obter a hora de início e fim como objetos datetime
        inicio = datetime.combine(datetime.today(), sessaoRoteiro.horarioid.inicio)
        fim = datetime.combine(datetime.today(), sessaoRoteiro.horarioid.fim)
        duracao_total = (fim - inicio).total_seconds()
        # Subtrair a duração de todas as atividades já presentes na sessão
        for atividade in atividadesRoteiro:
            duracao_total -= atividade.duracao * 60
        duracao_restante_minutos = duracao_total // 60
        duracao_restante_minutos = int(duracao_restante_minutos)

        check2 = len(sessoesRoteiro)
        check= len(atividadesRoteiro)
        if request.method == "POST":
            if 'new-activ' in request.POST:
                duracaoesperada= int(request.POST['duracao'])
                atividadeid = Atividade.objects.get(id=request.POST['atividade'])
                AtividadeRoteiro.objects.create(
                    atividade = atividadeid,
                    roteiro = roteiroid,
                    duracao = duracaoesperada,
                )
                return redirect('atividades:adicionarAtividades', id)
            if 'new-sessao' in request.POST:
                inicio_str = request.POST['inicio']
                fim_str = request.POST['fim']
                diaAbertoInicio = Diaaberto.current().datadiaabertoinicio
                diaAbertoFim = Diaaberto.current().datadiaabertofim
                inicio = datetime.strptime(inicio_str, '%H:%M')
                fim = datetime.strptime(fim_str, '%H:%M')
                if (fim.hour > diaAbertoFim.hour or (fim.hour == diaAbertoFim.hour and fim.minute > diaAbertoFim.minute)) or (inicio.hour < diaAbertoInicio.hour or (inicio.hour == diaAbertoInicio.hour and inicio.minute < diaAbertoInicio.minute)) or inicio_str > fim_str:
                    error_message = f"O horário deve estar entre o horário do Dia Aberto ({diaAbertoInicio.hour}:{diaAbertoInicio.minute} - {diaAbertoFim.hour}:{diaAbertoFim.minute})"    
                    return render(request=request, 
                      template_name='atividades/adicionar_atividades.html',
                      context={ 'atividades_roteiro': AtividadeRoteiro.objects.all().filter(roteiro=id), 
                               'dias': dias_diaaberto,
                               'sessoes_roteiro': sessoesRoteiro,
                               'check': check,
                               'check2': check2,
                               'id': id,
                               'atividades': atividades,
                               'duracaorestante': duracao_restante_minutos,
                               'error_message': error_message})
                horario = Horario.objects.create(inicio=inicio_str, fim=fim_str)
                sessao = Sessao.objects.create(
                    ninscritos = 0,
                    vagas = sessaoRoteiro.ninscritos + sessaoRoteiro.vagas,
                    roteiroid = roteiroid,
                    dia = request.POST['diasessao'],
                    horarioid = horario,
                )
                return redirect('atividades:adicionarAtividades', id)
        return render(request=request, 
                      template_name='atividades/adicionar_atividades.html',
                      context={ 'atividades_roteiro': AtividadeRoteiro.objects.all().filter(roteiro=id), 
                               'dias': dias_diaaberto,
                               'sessoes_roteiro': sessoesRoteiro,
                               'check': check,
                               'check2': check2,
                               'id': id,
                               'atividades': atividades,
                               'duracaorestante': duracao_restante_minutos})
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })    

def eliminarAtividadeRoteiro(request,id):
    user_check_var = user_check(request=request, user_profile=[Coordenador,Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')
    atividade_sessao = AtividadeRoteiro.objects.filter(id=id)

    if atividade_sessao.exists():
        atividadeRot=atividade_sessao.first()
        roteiroid= atividadeRot.roteiro.id 
        atividadeRot.delete()
        return redirect('atividades:adicionarAtividades',roteiroid)
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })

def eliminarSessaoRoteiro(request,id):
    user_check_var = user_check(request=request, user_profile=[Coordenador,Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')
    roteiro_sessao = Sessao.objects.filter(id=id)

    if roteiro_sessao.exists():
        sessaoRot=roteiro_sessao.first()
        roteiroid= sessaoRot.roteiroid.id 
        sessaoRot.delete()
        return redirect('atividades:adicionarAtividades',roteiroid)
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })    

def verresumo_roteiro(request, id):
    user_check_var = user_check(request=request, user_profile=[Coordenador,Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    roteiro = Roteiro.objects.filter(id=id,coord=userId)

    if roteiro.exists():  
        roteiro= Roteiro.objects.get(id=id)
        if request.method == "POST":
            if 'anterior' in request.POST:
                return redirect('atividades:adicionarAtividades', id)
        atividades_roteiro= AtividadeRoteiro.objects.filter(roteiro=id)
        sessoes_roteiro = Sessao.objects.filter(roteiroid=id)
        return render(request=request, 
                      template_name="atividades/resumo_roteiro.html",  
                      context={"roteiro": roteiro, 
                               "atividades_roteiro": atividades_roteiro,
                               'sessoes_roteiro': sessoes_roteiro}
                      )
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })    


def eliminar_roteiro(request, id):
    user_check_var = user_check(request=request, user_profile=[Coordenador,Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    
    roteiro = ''
    if Roteiro.objects.filter(id=id).exists():
        roteiro = Roteiro.objects.get(id=id)
        roteiro.delete()
        return render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'success',
                                'm':'Roteiro eliminado'
                            })
    
    return redirect('atividades:consultarRoteiro')


def alterarRoteiro(request,id):
    user_check_var = user_check(request=request, user_profile=[Coordenador, Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    userId = user_check_var.get('firstProfile').utilizador_ptr_id
    roteiro = Roteiro.objects.filter(id=id,coord=userId)
 
    diaaberto=Diaaberto.current()
    diainicio= diaaberto.datadiaabertoinicio.date()
    diafim= diaaberto.datadiaabertofim.date()
    totaldias= diafim-diainicio+timedelta(days=1)
    dias_diaaberto= []
    for d in range(totaldias.days):
        dias_diaaberto.append(diainicio+timedelta(days=d))

    if roteiro.exists():  
        roteiro_object = Roteiro.objects.get(id=id)
        sessaoRoteiro = Sessao.objects.filter(roteiroid=id).first()
        # Preencha os dados do roteiro nos campos do formulário manualmente
        form_data = {
            'nome': roteiro_object.nome,
            'descricao': roteiro_object.descricao,
            'diaabertoid': roteiro_object.diaabertoid.id,
            'diasessao': sessaoRoteiro.dia,
            'inicio': sessaoRoteiro.horarioid.inicio,
            'fim': sessaoRoteiro.horarioid.fim,
            'nparticipantes': sessaoRoteiro.ninscritos+sessaoRoteiro.vagas,
        }
       
        roteiro_object_form = RoteiroForm(instance=roteiro_object, initial=form_data)
        if request.method == 'POST':    #Se estivermos a receber um request com formulario  
            submitted_data = request.POST.copy()
            roteiro_object_form = RoteiroForm(submitted_data, instance=roteiro_object)
            if roteiro_object_form.is_valid():
                roteiro_object_formed = roteiro_object_form.save(commit=False)
                roteiro_object_formed.save()
                
                inicio = roteiro_object_form.cleaned_data['inicio']
                fim = roteiro_object_form.cleaned_data['fim']
                if fim != sessaoRoteiro.horarioid.fim or inicio != sessaoRoteiro.horarioid.inicio:
                    horario = Horario.objects.create(inicio=inicio, fim=fim)
                    sessaoRoteiro.horarioid = horario
                if roteiro_object_form.cleaned_data['diasessao'] != sessaoRoteiro.dia:
                    sessaoRoteiro.dia = roteiro_object_form.cleaned_data['diasessao']    
                if roteiro_object_form.cleaned_data['nparticipantes'] != (sessaoRoteiro.vagas + sessaoRoteiro.ninscritos):
                    sessaoRoteiro.ninscritos = 0
                    sessaoRoteiro.vagas = roteiro_object_form.cleaned_data['nparticipantes']

                sessaoRoteiro.save()
                #nviews.enviar_notificacao_automatica(request,"atividadeAlterada",activity_object_formed.id) #Enviar Notificacao Automatica !!!!!!
                return redirect('atividades:adicionarAtividades',id)   
            else:
                # Se o formulário não for válido, renderize o formulário novamente com os erros
                context = {'form': roteiro_object_form,
                           'roteiro_object': roteiro_object,
                           'dia_aberto': roteiro_object.diaabertoid,
                           'sessaoRoteiro': sessaoRoteiro,
                           'dias': dias_diaaberto,
                           }
                # Adicione um contexto para os erros do formulário
                context['errors'] = roteiro_object_form.errors
                return render(request, 'atividades/criar_roteiro.html', context)       
        return render(request=request,
                        template_name='atividades/criar_roteiro.html',
                        context={'form': roteiro_object_form,
                                 'roteiro_object': roteiro_object,
                                 'dia_aberto': roteiro_object.diaabertoid, 
                                 'sessaoRoteiro': sessaoRoteiro,
                                 'dias': dias_diaaberto}
                        )
    else:
        return    render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para esta ação!'
                            })
    

def RoteiroPDF(request, id):
    """ View que gera um PDF com os detalhes da inscrição """
    roteiro = get_object_or_404(Roteiro, id=id)
    user_check_var = user_check(request=request, user_profile=[Coordenador, Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')
    ano = roteiro.ano
    atividades = roteiro.atividaderoteiro_set.all()
    sessoes = roteiro.sessao_set.all()
    context = {
        'request': request,
        'roteiro': roteiro,
        'ano': ano,
        'atividades': atividades,
        'sessoes': sessoes,
    }
    return render_pdf("atividades/pdf.html", context, f"dia_aberto_ualg_{ano}.pdf")   

def duplicarAtividade(request, id):

    user_check_var = user_check(request=request, user_profile=[Coordenador, ProfessorUniversitario])
    if user_check_var.get('exists') == False: return user_check_var.get('render')
    # Recupere a atividade que deseja duplicar
    atividade_original = get_object_or_404(Atividade, id=id)
    material_original = get_object_or_404(Materiais, atividadeid=id)

    # Crie uma cópia da atividade com o dia aberto atual
    nova_atividade = Atividade.objects.create(
        nome = atividade_original.nome,
        descricao = atividade_original.descricao,
        publicoalvo = atividade_original.publicoalvo,
        nrcolaboradoresnecessario = atividade_original.nrcolaboradoresnecessario,
        tipo = atividade_original.tipo,
        estado = atividade_original.estado,
        professoruniversitarioutilizadorid = atividade_original.professoruniversitarioutilizadorid,
        duracaoesperada = atividade_original.duracaoesperada,
        participantesmaximo = atividade_original.participantesmaximo,
        diaabertoid = Diaaberto.current(),
        espacoid = atividade_original.espacoid,
        tema = atividade_original.tema,
    )
    Materiais.objects.create(
        atividadeid = nova_atividade,
        nomematerial = material_original.nomematerial,
    )

    if isinstance(user_check_var['firstProfile'], Coordenador):
        return redirect(reverse('atividades:atividadesUOrganica'))

    # Verifica se o usuário é um ProfessorUniversitario
    elif isinstance(user_check_var['firstProfile'], ProfessorUniversitario):
        return redirect(reverse('atividades:minhasAtividades'))


def duplicarRoteiro(request, id):
    user_check_var = user_check(request=request, user_profile=[Coordenador, Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    roteiro_original = get_object_or_404(Roteiro, id=id)

    novo_roteiro = Roteiro.objects.create(
        nome = roteiro_original.nome,
        descricao = roteiro_original.descricao,
        ano = Diaaberto.current().ano,
        coord = roteiro_original.coord,
        diaabertoid = Diaaberto.current(),
    )


    for atividade in roteiro_original.atividaderoteiro_set.all():
        atividades_similares = Atividade.objects.filter(
            nome=atividade.atividade.nome,
            diaabertoid=Diaaberto.current()
        )
        
        if atividades_similares and atividades_similares.exists():
            atividade_similar = Atividade.objects.get(
                nome=atividade.atividade.nome,
                diaabertoid=Diaaberto.current()
            )
            new_atividadeRoteiro = AtividadeRoteiro(roteiro=Roteiro.objects.get(id=novo_roteiro.id), atividade=Atividade.objects.get(id=atividade_similar.id), duracao=atividade.duracao)
            new_atividadeRoteiro.save()

        else:
            material_original = get_object_or_404(Materiais, atividadeid=atividade.atividade)

            # Crie uma cópia da atividade com o dia aberto atual
            nova_atividade = Atividade.objects.create(
                nome = atividade.atividade.nome,
                descricao = atividade.atividade.descricao,
                publicoalvo = atividade.atividade.publicoalvo,
                nrcolaboradoresnecessario = atividade.atividade.nrcolaboradoresnecessario,
                tipo = atividade.atividade.tipo,
                estado = atividade.atividade.estado,
                professoruniversitarioutilizadorid = atividade.atividade.professoruniversitarioutilizadorid,
                duracaoesperada = atividade.atividade.duracaoesperada,
                participantesmaximo = atividade.atividade.participantesmaximo,
                diaabertoid = Diaaberto.current(),
                espacoid = atividade.atividade.espacoid,
                tema = atividade.atividade.tema,
            )
            Materiais.objects.create(
                atividadeid = nova_atividade,
                nomematerial = material_original.nomematerial,
            )
            new_atividadeRoteiro = AtividadeRoteiro(roteiro=Roteiro.objects.get(id=novo_roteiro.id), atividade=Atividade.objects.get(id=nova_atividade.id), duracao=atividade.duracao)
            new_atividadeRoteiro.save()

    sessaoRoteiro = Sessao.objects.filter(roteiroid=id).first()
    Sessao.objects.create(
        ninscritos = 0,
        vagas = sessaoRoteiro.vagas,
        roteiroid = novo_roteiro,
        dia = Diaaberto.current().datadiaabertoinicio.date(),
        horarioid = sessaoRoteiro.horarioid,
    )         
        

    return redirect(reverse('atividades:consultarRoteiros'))


def relatoriosRoteiros(request):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    anos = Diaaberto.objects.values_list('ano', flat=True).distinct()

    context = {'anos': anos}
    return render(request=request, template_name="atividades/relatoriosRoteiros.html", context=context)


def dias_disponiveis(request):
    ano_selecionado = request.POST.get("ano")
    print(ano_selecionado)

    default = {
        'key': '',
        'value': 'Selecione o dia'
    }
    
    if ano_selecionado:
        dias = Sessao.objects.filter(dia__year=ano_selecionado).values_list('dia', flat=True).distinct()
        print(dias)
        options = '<option value="">Selecione o dia</option>'
        options = []
        for dia in dias:
            options.append({'key': dia.strftime('%Y-%m-%d'), 'value': dia})
    else:
        dias = []
        print('nada')
    
    return render(request=request, 
                template_name="configuracao/dropdown.html", 
                context={"options": options,    "default": default})


def relatorioRoteirosPDF(request):
    """ View que gera um PDF com os detalhes da inscrição """
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    ano = request.POST.get('ano')
    dia = request.POST.get('dia')

    sessoes = Sessao.objects.all()

    if ano:
        sessoes = sessoes.filter(dia__year=ano)
    if dia:
        sessoes = sessoes.filter(dia=dia)

    context = {
        'request': request,
        'sessoes': sessoes,
        'ano': ano,
        'dia': dia,
    }
    return render_pdf("atividades/relatorio_roteiros_pdf.html", context, f"Roteiros.pdf")


def relatorioRoteirosCSV(request):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if user_check_var.get('exists') == False: return user_check_var.get('render')

    ano = request.POST.get('ano')
    dia = request.POST.get('dia')

    sessoes = Sessao.objects.all()

    if ano:
        sessoes = sessoes.filter(dia__year=ano)
    if dia:
        sessoes = sessoes.filter(dia=dia)

    # Crie o objeto HttpResponse com o tipo de conteúdo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="roteiros.csv"'

    # Crie o escritor CSV usando o objeto de resposta
    writer = csv.writer(response, delimiter=";")

    # Escreva o cabeçalho do arquivo CSV
    writer.writerow(['Nome', 'Tipo', 'Sessoes', 'Atividades', 'Dia', 'Início', 'Fim', 'Inscritos','Presenças'])

    # Escreva os dados para cada sessão
    for sessao in sessoes:
        nome = sessao.atividadeid.nome if sessao.atividadeid else sessao.roteiroid.nome
        tipo = 'Atividade' if sessao.atividadeid else 'Roteiro'
        sessoes_count = sessao.atividadeid.numero_de_sessoes() if sessao.atividadeid else sessao.roteiroid.numero_de_sessoes()
        atividades_count = '-' if sessao.atividadeid else sessao.roteiroid.numero_de_atividades()
        dia = sessao.dia
        inicio = sessao.horarioid.inicio
        fim = sessao.horarioid.fim
        inscritos = f"{sessao.ninscritos}/{sessao.vagas + sessao.ninscritos}"
        presentes = sessao.nr_presentes
        
        writer.writerow([nome, tipo, sessoes_count, atividades_count, dia, inicio, fim, inscritos, presentes])

    return response