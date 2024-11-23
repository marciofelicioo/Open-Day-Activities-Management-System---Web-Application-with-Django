from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Utilizador, ProfessorUniversitario, Participante, Colaborador, Coordenador
from django.shortcuts import redirect
from .forms import *
from .tables import UtilizadoresTable
from .filters import UtilizadoresFilter
from django.contrib import messages
from django.contrib.auth import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group
from configuracao.models import Unidadeorganica,Departamento,Curso
from django.core.paginator import Paginator
from notificacoes import views
from inscricoes.models import Inscricao
from django.db import transaction
from atividades.models import Sessao
from notificacoes.models import *
from coordenadores.models import Tarefa
from django.db.models import F
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView



def user_check(request, user_profile = None):
    ''' 
    Verifica se o utilizador que esta logado pertence a pelo menos um dos perfis mencionados 
    e.g. user_profile = {Administrador,Coordenador,ProfessorUniversitario}
    Isto faz com que o user que esta logado possa ser qualquer um dos 3 perfis. 
    '''
    if not request.user.is_authenticated:
        return {'exists': False, 'render': redirect('utilizadores:login')}
    elif user_profile is not None:
        matches_profile = False
        for profile in user_profile:
            if profile.objects.filter(utilizador_ptr_id = request.user.id).exists():
                return {'exists': True, 'firstProfile': profile.objects.filter(utilizador_ptr_id = request.user.id).first()}
        return {'exists': False, 
                'render': render(request=request,
                            template_name='mensagem.html',
                            context={
                                'tipo':'error',
                                'm':'Não tem permissões para aceder a esta página!'
                            })
                }
    raise Exception('Unknown Error!')



def load_departamentos(request):
    ''' Carregar todos os departamentos para uma determinada faculdade '''
    faculdadeid = request.GET.get('faculdade')
    departamentos = Departamento.objects.filter(unidadeorganicaid=faculdadeid).order_by('nome')
    return render(request, 'utilizadores/departamento_dropdown_list_options.html', {'departamentos': departamentos})





def load_cursos(request):
    ''' Carregar todos os cursos para uma determinada faculdade '''
    faculdadeid = request.GET.get('faculdade')
    cursos = Curso.objects.filter(unidadeorganicaid=faculdadeid).order_by('nome')
    return render(request, 'utilizadores/curso_dropdown_list_options.html', {'cursos': cursos})




class consultar_utilizadores(SingleTableMixin, FilterView):
    ''' Consultar todos os utilizadores com as funcionalidades dos filtros '''
    table_class = UtilizadoresTable
    template_name = 'utilizadores/consultar_utilizadores.html'
    filterset_class = UtilizadoresFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(
            request=request, user_profile=[Coordenador, Administrador])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context




def escolher_perfil(request):
    ''' Escolher tipo de perfil para criar um utilizador '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    utilizadores = ["Participante",
                    "Professor Universitário", "Coordenador", "Colaborador","Administrador"]
    return render(request=request, template_name='utilizadores/escolher_perfil.html', context={"utilizadores": utilizadores,'u': u})






def criar_utilizador(request, id):
    ''' Criar um novo utilizador que poderá ter de ser validado dependendo do seu tipo '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    msg=False
    if request.method == "POST":
        tipo = id
        if tipo == 1:
            form = ParticipanteRegisterForm(request.POST)
            perfil = "Participante"
            my_group = Group.objects.get(name='Participante') 
        elif tipo == 2:
            form = ProfessorUniversitarioRegisterForm(request.POST)
            perfil = "Professor Universitario"
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorRegisterForm(request.POST)
            perfil = "Coordenador"
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorRegisterForm(request.POST)
            perfil = "Colaborador"
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorRegisterForm(request.POST)
            perfil = "Administrador"
            my_group = Group.objects.get(name='Administrador')    
        else:
            return redirect("utilizadores:escolher-perfil")

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            my_group.user_set.add(user)

            if tipo == 1:
                user.valido = 'True'
                user.save()
                p=1
            else:
                user.valido = 'False'
                recipient_id = user.id #Enviar Notificacao Automatica !!!!!!!!!
                user.save()
                p=0
                views.enviar_notificacao_automatica(request,"validarRegistosPendentes",recipient_id) #Enviar Notificacao Automatica !!!!!!!!!
            if request.user.is_authenticated:    
                user = get_user(request)
                if user.groups.filter(name = "Coordenador").exists():
                    return redirect("utilizadores:concluir-registo",2)
                elif user.groups.filter(name = "Administrador").exists():
                    return redirect("utilizadores:concluir-registo",2)  
            else:   
                return redirect("utilizadores:concluir-registo",p)
        else:
            msg=True
            tipo = id
            return render(request=request,
                          template_name="utilizadores/criar_utilizador.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'registo' : tipo,'msg': msg})
    else:
        tipo = id
        if tipo == 1:
            form = ParticipanteRegisterForm()
            perfil = "Participante"
        elif tipo == 2:
            form = ProfessorUniversitarioRegisterForm()
            perfil = "Professor Universitario"
        elif tipo == 3:
            form = CoordenadorRegisterForm()
            perfil = "Coordenador"
        elif tipo == 4:
            form = ColaboradorRegisterForm()
            perfil = "Colaborador"
        elif tipo == 5:
            form = AdministradorRegisterForm()
            perfil = "Administrador" 
        else:
            return redirect("utilizadores:escolher-perfil")
    return render(request=request,
                  template_name="utilizadores/criar_utilizador.html",
                  context={"form": form, 'perfil': perfil,'u': u,'registo' : tipo,'msg': msg})




def login_action(request):
    ''' Fazer login na plataforma do dia aberto e gestão de acessos à plataforma '''
    if request.user.is_authenticated: 
        return redirect("utilizadores:logout")   
    else:
        u=""
    msg=False
    error=""
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username=="" or password=="":
                msg=True
                error="Todos os campos são obrigatórios!"
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                utilizador = Utilizador.objects.get(id=user.id)
                if utilizador.valido=="False": 
                    msg=True
                    error="O seu registo ainda não foi validado"
                elif utilizador.valido=="Rejeitado":
                    msg=True
                    error="O seu registo não é válido"
                else:
                    login(request, user)
                    return redirect('utilizadores:mensagem',1)
            else:
                msg=True
                error="O nome de utilizador ou a palavra-passe inválidos!"
    form = LoginForm()
    return render(request=request,
                  template_name="utilizadores/login.html",
                  context={"form": form,"msg": msg, "error": error, 'u': u})






def logout_action(request):
    ''' Fazer logout na plataforma '''
    logout(request)
    return redirect('utilizadores:mensagem',2)





def alterar_password(request):
    ''' Alterar a password do utilizador '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        return redirect('utilizadores:mensagem',5)
    msg=False
    error="" 
    if request.method == 'POST':
        form = AlterarPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('utilizadores:mensagem',6)
        else:
            msg=True
            error="Passwords Incorretas!"
    form = AlterarPasswordForm(user=request.user)
    return render(request=request,
                  template_name="utilizadores/alterar_password.html",
                  context={"form": form,"msg": msg, "error": error, 'u': u})    






def rejeitar_utilizador(request, id): 
    ''' Funcionalidade de rejeitar um utilizador na pagina de consultar utilizadores '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"   
        elif user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
        
    try:
        u = Utilizador.objects.get(id = id)
        u.valido = 'Rejeitado'           
        u.save()   
        subject = 'Validação do registo do na plataforma do dia aberto'
        message = 'Caro(a) '+u.first_name+",\n\n"
        message+='O seu registo na plataforma do dia aberto foi rejeitado!'+"\n\n"
        message+='Equipa do dia aberto da Ualg'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [u.email,]
        send_mail( subject, message, email_from, recipient_list )
    except:
        pass
    if 'consultar_utilizadores' not in request.session:
        return redirect('utilizadores:consultar-utilizadores')
    else:    
        return HttpResponseRedirect(request.session['consultar_utilizadores'])





def alterar_idioma(request):  
    ''' Alterar o idioma da plataforma ''' 
    return redirect('utilizadores:mensagem',5)  




def validar_utilizador(request, id): 
    ''' Validar um utilizador na pagina consultar utilizadores '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"   
        elif user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5) 
        
    try:
        u = Utilizador.objects.get(id = id)
        u.valido = 'True'           
        u.save()   
        subject = 'Validação do registo do na plataforma do dia aberto'
        message = 'Caro(a) '+u.first_name+"\n\n"
        message+='O seu registo na plataforma do dia aberto foi bem sucedido!'+",\n\n"
        message+='Equipa do dia aberto da Ualg'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [u.email,]
        send_mail( subject, message, email_from, recipient_list )
    except:
        pass

    if 'consultar_utilizadores' not in request.session:
        return redirect('utilizadores:consultar-utilizadores')
    else:    
        return HttpResponseRedirect(request.session['consultar_utilizadores'])





def apagar_utilizador(request, id): 
    ''' Apagar um utilizador na pagina consultar utilizadores '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"   
        elif user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"       
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5)

    user = User.objects.get(id=id)
    # try:
    if user.groups.filter(name = "Coordenador").exists():
        u = Coordenador.objects.get(id=id)
    elif user.groups.filter(name = "Administrador").exists():
        u = Administrador.objects.get(id=id)
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        u = ProfessorUniversitario.objects.get(id=id)
    elif user.groups.filter(name = "Colaborador").exists():
        u = Colaborador.objects.get(id=id)
        for tarefa in Tarefa.objects.filter(colab=u):
            if tarefa.estado=="Iniciada":
                return redirect('utilizadores:mensagem',14)
            elif tarefa.estado=="Concluida":
                tarefa.delete()
            else:    
                tarefa.estado="naoAtribuida"
                tarefa.colab=None
                tarefa.save()
    elif user.groups.filter(name="Participante").exists():
        u = Participante.objects.get(id=id)
        for inscricao in Inscricao.objects.filter(participante=u):
            inscricaosessao_set = inscricao.inscricaosessao_set.all()
            for inscricaosessao in inscricaosessao_set:
                sessaoid = inscricaosessao.sessao.id
                nparticipantes = inscricaosessao.nparticipantes
                with transaction.atomic():
                    sessao = Sessao.objects.select_for_update().get(pk=sessaoid)
                    sessao.vagas = F('vagas') + nparticipantes
                    sessao.save()
            inscricao.delete()
    else:
        u = user    
    utilizador = Utilizador.objects.get(user_ptr_id=u.id)
    
    informacao_mensagem1 = InformacaoMensagem.objects.filter(emissor=utilizador.id)
    for msg in informacao_mensagem1:
        msg.delete()

    informacao_mensagem2 = InformacaoMensagem.objects.filter(recetor=utilizador.id)
    for msg in informacao_mensagem2:
        msg.delete()

    mensagens_recebidas1 = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=utilizador.id)
    for msg in mensagens_recebidas1:
        msg.delete()
    mensagens_recebidas2 = MensagemRecebida.objects.select_related('mensagem__emissor').filter(mensagem__emissor=utilizador.id)
    for msg in mensagens_recebidas2:
        msg.delete()
    mensagens_enviadas1 = MensagemEnviada.objects.select_related('mensagem__recetor').filter(mensagem__recetor=utilizador.id)
    for msg in mensagens_enviadas1:
        msg.delete()
    mensagens_enviadas2 = MensagemEnviada.objects.select_related('mensagem__emissor').filter(mensagem__emissor=utilizador.id)
    for msg in mensagens_enviadas2:
        msg.delete()    
    u.delete() 
    # except:
    #     return redirect('utilizadores:mensagem',13)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




def apagar_proprio_utilizador(request):  
    ''' Apagar a própria conta '''
    if request.user.is_authenticated:
        id=request.user.id  
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = Coordenador.objects.get(id=id)
        elif user.groups.filter(name = "Administrador").exists():
            u = Administrador.objects.get(id=id)
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = ProfessorUniversitario.objects.get(id=id)
        elif user.groups.filter(name = "Colaborador").exists():
            u = Colaborador.objects.get(id=id)
            try:
                for tarefa in Tarefa.objects.filter(colab=u):
                    if tarefa.estado=="Iniciada":
                        return redirect('utilizadores:mensagem',15)
                    elif tarefa.estado=="Concluida":
                        tarefa.delete()
                    else:    
                        tarefa.estado="naoAtribuida"
                        tarefa.colab=None
                        tarefa.save()
            except:
                return redirect('utilizadores:mensagem',13)
        elif user.groups.filter(name = "Participante").exists():
            try:
                u = Participante.objects.filter(id=id) 
                u = Participante.objects.get(id=id)
                for inscricao in Inscricao.objects.filter(participante=u):
                    inscricaosessao_set = inscricao.inscricaosessao_set.all()
                    for inscricaosessao in inscricaosessao_set:
                        sessaoid = inscricaosessao.sessao.id
                        nparticipantes = inscricaosessao.nparticipantes
                        with transaction.atomic():
                            sessao = Sessao.objects.select_for_update().get(pk=sessaoid)
                            sessao.vagas = F('vagas') + nparticipantes
                            sessao.save()
                    inscricao.delete()
            except:
                return redirect('utilizadores:mensagem',13)
        else:
            u= user     
    else:
        return redirect('utilizadores:mensagem',5)
    try:
        utilizador = Utilizador.objects.get(user_ptr_id=user.id)
        
        informacao_mensagem1 = InformacaoMensagem.objects.filter(emissor=utilizador.id)
        for msg in informacao_mensagem1:
            msg.delete()

        informacao_mensagem2 = InformacaoMensagem.objects.filter(recetor=utilizador.id)
        for msg in informacao_mensagem2:
            msg.delete()

        mensagens_recebidas1 = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=utilizador.id)
        for msg in mensagens_recebidas1:
            msg.delete()
        mensagens_recebidas2 = MensagemRecebida.objects.select_related('mensagem__emissor').filter(mensagem__emissor=utilizador.id)
        for msg in mensagens_recebidas2:
            msg.delete()
        mensagens_enviadas1 = MensagemEnviada.objects.select_related('mensagem__recetor').filter(mensagem__recetor=utilizador.id)
        for msg in mensagens_enviadas1:
            msg.delete()
        mensagens_enviadas2 = MensagemEnviada.objects.select_related('mensagem__emissor').filter(mensagem__emissor=utilizador.id)
        for msg in mensagens_enviadas2:
            msg.delete()   
                
        u.delete() 
        logout(request)
    except:
        return redirect('utilizadores:mensagem',13)

    return redirect('utilizadores:mensagem',7)   




def enviar_email_validar(request,nome,id):
    ''' Envio de email quando o utilizador é validado na pagina consultar utilizadores '''  
    msg="A enviar email a "+nome+" a informar que o seu registo foi validado"
    user_check_var = user_check(request=request, user_profile=[Coordenador, Administrador])
    if user_check_var.get('exists') == False: 
        return user_check_var.get('render')
    request.session['consultar_utilizadores'] = request.META.get('HTTP_REFERER', '/')
    return render(request=request,
                  template_name="utilizadores/enviar_email_validar.html",
                  context={"msg": msg, "id":id})



def enviar_email_rejeitar(request,nome,id):  
    ''' Envio de email quando o utilizador é rejeitado na pagina consultar utilizadores '''
    msg="A enviar email a "+nome+" a informar que o seu registo foi rejeitado"
    user_check_var = user_check(request=request, user_profile=[Coordenador, Administrador])
    if user_check_var.get('exists') == False: 
        return user_check_var.get('render')
    request.session['consultar_utilizadores'] = request.META.get('HTTP_REFERER', '/')
    return render(request=request,
                  template_name="utilizadores/enviar_email_rejeitar.html",
                  context={"msg": msg, "id":id})



def alterar_utilizador_admin(request,id):
    ''' Funcionalidade de o administrador alterar um utilizador '''
    if request.user.is_authenticated:    
        utilizador_atual = get_user(request)
        if utilizador_atual.groups.filter(name = "Administrador").exists():
            admin = "Administrador"         
        else:
            return redirect('utilizadores:mensagem',5) 
    else:
        return redirect('utilizadores:mensagem',5)


    
    user = User.objects.get(id=id)
    if user.groups.filter(name = "Coordenador").exists():
        tipo=3            
        u = "Coordenador"
        utilizador_object = Coordenador.objects.get(id=user.id)
        utilizador_form = CoordenadorAlterarPerfilForm(instance=utilizador_object)
        perfil= "Coordenador"
    elif user.groups.filter(name = "Administrador").exists():
        tipo=5
        u = "Administrador"
        utilizador_object = Administrador.objects.get(id=user.id)
        utilizador_form = AdministradorAlterarPerfilForm(instance=utilizador_object)
        perfil="Administrador"
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        tipo=2
        u = "ProfessorUniversitario"
        utilizador_object = ProfessorUniversitario.objects.get(id=user.id)
        utilizador_form = ProfessorUniversitarioAlterarPerfilForm(instance=utilizador_object)
        perfil="Professor Universitario"
    elif user.groups.filter(name = "Colaborador").exists():
        tipo=4            
        u = "Colaborador"
        utilizador_object = Colaborador.objects.get(id=user.id)
        utilizador_form = ColaboradorAlterarPerfilForm(instance=utilizador_object)
        perfil= "Colaborador"
    elif user.groups.filter(name = "Participante").exists():
        tipo=1
        u = "Participante" 
        utilizador_object = Participante.objects.get(id=user.id)
        utilizador_form = ParticipanteAlterarPerfilForm(instance=utilizador_object)
        perfil= "Participante"
    else:
        return redirect('utilizadores:mensagem',5)     



    msg=False
    if request.method == "POST":
        submitted_data = request.POST.copy()
        if tipo == 1:
            form = ParticipanteAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Participante') 
        elif tipo == 2:
            form = ProfessorUniversitarioAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Administrador')    
        else:
            return redirect('utilizadores:mensagem',5)   

        email = request.POST.get('email')

        erros=[]


        if email and User.objects.exclude(email=utilizador_object.email).filter(email=email).exists():
            erros.append('O email já existe')
        elif email==None:
            erros.append('O email é inválido')

        if form.is_valid() and len(erros)==0:
            utilizador_form_object = form.save(commit=False)
            if tipo==2 or tipo==3 or tipo==4:
                utilizador_form_object.faculdade = Unidadeorganica.objects.get(id=submitted_data['faculdade'])
                utilizador_form_object.departamento = Departamento.objects.get(id=submitted_data['departamento'])
            utilizador_form_object.save()  
            return redirect('utilizadores:consultar-utilizadores')   
        else:
            msg=True
            return render(request=request,
                          template_name="utilizadores/alterar_utilizador_admin.html",
                          context={"form": form, 'perfil': perfil, 'u': admin,'registo' : tipo,'msg': msg, 'erros':erros,'id':id})
    else:

        return render(request=request,
                  template_name="utilizadores/alterar_utilizador_admin.html",
                  context={"form": utilizador_form, 'perfil': perfil,'u': admin,'registo' : tipo,'msg': msg,'id':id})




def alterar_utilizador(request):
    ''' Funcionalidade de alterar dados de conta '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            tipo=3            
            u = "Coordenador"
            utilizador_object = Coordenador.objects.get(id=user.id)
            utilizador_form = CoordenadorAlterarPerfilForm(instance=utilizador_object)
            perfil= "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            tipo=5
            u = "Administrador"
            utilizador_object = Administrador.objects.get(id=user.id)
            utilizador_form = AdministradorAlterarPerfilForm(instance=utilizador_object)
            perfil="Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            tipo=2
            u = "ProfessorUniversitario"
            utilizador_object = ProfessorUniversitario.objects.get(id=user.id)
            utilizador_form = ProfessorUniversitarioAlterarPerfilForm(instance=utilizador_object)
            perfil="Professor Universitario"
        elif user.groups.filter(name = "Colaborador").exists():
            tipo=4            
            u = "Colaborador"
            utilizador_object = Colaborador.objects.get(id=user.id)
            utilizador_form = ColaboradorAlterarPerfilForm(instance=utilizador_object)
            perfil= "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            tipo=1
            u = "Participante" 
            utilizador_object = Participante.objects.get(id=user.id)
            utilizador_form = ParticipanteAlterarPerfilForm(instance=utilizador_object)
            perfil= "Participante"
        else:
            return redirect('utilizadores:mensagem',5)     
    else:
        return redirect('utilizadores:mensagem',5) 


    msg=False
    if request.method == "POST":
        submitted_data = request.POST.copy()
        if tipo == 1:
            form = ParticipanteAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Participante') 
        elif tipo == 2:
            form = ProfessorUniversitarioAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorAlterarPerfilForm(submitted_data,instance=utilizador_object)
            my_group = Group.objects.get(name='Administrador')    
        else:
            return redirect('utilizadores:mensagem',5) 

        username = request.POST.get('newusername')
        email = request.POST.get('email')

        erros=[]
        if username and User.objects.exclude(username=utilizador_object.username).filter(username=username).exists():
            erros.append('O username já existe')
        elif username=="":
            erros.append('Todos os campos são obrigatórios!')

        if email and User.objects.exclude(email=utilizador_object.email).filter(email=email).exists():
            erros.append('O email já existe')
        elif email==None:
            erros.append('O email é inválido')

        if form.is_valid() and len(erros)==0:
            utilizador_form_object = form.save(commit=False)
            utilizador_form_object.username = username
            if tipo==2 or tipo==3 or tipo==4:
                utilizador_form_object.faculdade = Unidadeorganica.objects.get(id=submitted_data['faculdade'])
                utilizador_form_object.departamento = Departamento.objects.get(id=submitted_data['departamento'])
            if tipo==1 or tipo==5:
                utilizador_form_object.valido="True"
            else:
                utilizador_form_object.valido="False"    
            utilizador_form_object.save()  
            return redirect('utilizadores:mensagem',8) 
        else:
            msg=True
            return render(request=request,
                          template_name="utilizadores/alterar_utilizador.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'registo' : tipo,'msg': msg,'username':username, 'erros':erros})
    else:

        return render(request=request,
                  template_name="utilizadores/alterar_utilizador.html",
                  context={"form": utilizador_form, 'perfil': perfil,'u': u,'registo' : tipo,'username':user.username,'msg': msg})




def home(request):
    ''' Pagina principal da plataforma '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""
    
    return render(request, "inicio.html",context={ 'u': u})



def concluir_registo(request,id):
    ''' Página que é mostrada ao utilizador quando faz um registo na plataforma '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""   
    else:
        u=""
    if id == 1:
        participante="True"
    elif id == 0:
        participante="False"
    elif id == 2:
        participante="Admin"   
    return render(request=request,
                  template_name="utilizadores/concluir_registo.html",
                  context={'participante': participante, 'u': u})




def mensagem(request, id, *args, **kwargs):
    ''' Template de mensagens informativas/erro/sucesso '''

    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u = ""


    if id == 400 or id == 500:
        user = get_user(request)
        m = "Erro no servidor"
        tipo = "error"
    elif id == 1:
        user = get_user(request)
        m = "Bem vindo(a) "+user.first_name
        tipo = "info"

    elif id == 2:
        m = "Até á próxima!"
        tipo = "info"

    elif id == 3:
        m = "Registo feito com sucesso!"
        tipo = "sucess"

    elif id == 4:
        m = "É necessário fazer login primeiro"
        tipo = "error"

    elif id == 5:
        m = "Não permitido"
        tipo = "error"
    elif id == 6:
        m = "Senha alterada com sucesso!"
        tipo = "success"    
    elif id == 7:
        m = "Conta apagada com sucesso"
        tipo = "success"   
    elif id == 8:
        m = "Perfil alterado com sucesso"
        tipo = "success" 
    elif id == 9:
        m = "Perfil criado com sucesso"
        tipo = "success" 
    elif id == 10:
        m = "Não existem notificações"
        tipo = "info"
    elif id == 11:
        m = "Esta tarefa deixou de estar atribuída"
        tipo = "error"
    elif id == 12:
        m = "Ainda não é permitido criar inscrições"
        tipo = "error"
    elif id == 13:
        m = "Erro ao apagar dados do utilizador"
        tipo = "error" 
    elif id == 14:
        m = "Não existem mensagens"
        tipo = "info"  
    elif id == 15:
        m = "Este colaborador tem tarefas iniciadas pelo que apenas deverá ser apagado quando estas estiverem concluidas"
        tipo = "info"  
    elif id == 16:
        m = "Para puder apagar a sua conta deverá concluir primeiro as tarefas que estão iniciadas"
        tipo = "info"                 
    elif id == 17:
        m = "A sua disponibilidade foi alterada com sucesso"
        tipo = "success"
    elif id == 18:
        m = "Antes de poder ver dados e estatísticas é preciso configurar um Dia Aberto."
        tipo = "error"
    elif id == 19:  # Novo código para erro de banco de dados
        m = "Base de dados temporáriamente indisponível, volte mais tarde!"
        tipo = "error"    
    else:
        m = "Esta pagina não existe"
        tipo = "error"                                     

    
    continuar = "on" 
    if id == 400 or id == 500 or id == 19:
        continuar = "off" 
    return render(request=request,
        template_name="mensagem.html", context={'m': m, 'tipo': tipo ,'u': u, 'continuar': continuar,})





def mudar_perfil_escolha_admin(request,id):
    '''  Funcionalidade de o administrador alterar o perfil de um dado utilizador 
     Redireciona para uma pagina onde é possível escolher o perfil que quer alterar '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        else:
            return redirect('utilizadores:mensagem',5)   
    else:
        return redirect('utilizadores:mensagem',5) 

    user=User.objects.get(id=id)  
    if user.groups.filter(name = "Coordenador").exists():           
        x = "Coordenador"
    elif user.groups.filter(name = "Administrador").exists():
        x = "Administrador"
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        x = "Professor Universitário"
    elif user.groups.filter(name = "Colaborador").exists():        
        x = "Colaborador"
    elif user.groups.filter(name = "Participante").exists():
        x = "Participante" 
    else:
        return redirect('utilizadores:mensagem',5)     

    utilizadores = ["Participante",
                    "Professor Universitário", "Coordenador", "Colaborador","Administrador"]
    return render(request=request, template_name='utilizadores/mudar_perfil_escolha_admin.html', context={"utilizadores": utilizadores,'u': u,'id':id ,'x':x})




def mudar_perfil_escolha(request):
    ''' Funcionalidade de o utilizador alterar o seu próprio perfil
    Redireciona para uma pagina onde é possível escolher o perfil que quer alterar '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        u=""

    user=User.objects.get(id=user.id)  
    
    if user.groups.filter(name = "Coordenador").exists():           
        x = "Coordenador"
    elif user.groups.filter(name = "Administrador").exists():
        x = "Administrador"
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        x = "ProfessorUniversitario"
    elif user.groups.filter(name = "Colaborador").exists():        
        x = "Colaborador"
    elif user.groups.filter(name = "Participante").exists():
        x = "Participante" 
    else:
        return redirect('utilizadores:mensagem',5)     

    utilizadores = ["Participante",
                    "Professor Universitário", "Coordenador", "Colaborador","Administrador"]
    return render(request=request, template_name='utilizadores/mudar_perfil_escolha.html', context={"utilizadores": utilizadores,'u': u,'id':id ,'x':x})






def mudar_perfil_admin(request,tipo,id):
    ''' Funcionalidade de o administrador alterar o perfil de um dado utilizador 
    Redireciona para uma pagina que contem os dados já existentes do utilizador a alterar sendo 
    que apenas os campos diferentes não estão preenchidos '''
    if request.user.is_authenticated:    
        user = get_user(request)
        if user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        else:
            return redirect('utilizadores:mensagem',5)   
    else:
        return redirect('utilizadores:mensagem',5) 

    if tipo == 1:
        form = ParticipanteAlterarPerfilForm()
        perfil = "Participante"
    elif tipo == 2:
        form = ProfessorUniversitarioAlterarPerfilForm()
        perfil = "Professor Universitario"
    elif tipo == 3:
        form = CoordenadorAlterarPerfilForm()
        perfil = "Coordenador"
    elif tipo == 4:
        form = ColaboradorAlterarPerfilForm()
        perfil = "Colaborador"
    elif tipo == 5:
        form = AdministradorAlterarPerfilForm()
        perfil = "Administrador" 
    else:
        return redirect('utilizadores:mensagem',5) 

    user=User.objects.get(id=id)
    if user.groups.filter(name = "Coordenador").exists():         
        utilizador_object = Coordenador.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial =utilizador_object.faculdade.id

    elif user.groups.filter(name = "Administrador").exists():
        utilizador_object = Administrador.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        utilizador_object = ProfessorUniversitario.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial =utilizador_object.faculdade.id
    elif user.groups.filter(name = "Colaborador").exists():
        utilizador_object = Colaborador.objects.get(id=user.id) 
        gabinete=""
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial = utilizador_object.faculdade.id
    elif user.groups.filter(name = "Participante").exists():
        utilizador_object = Participante.objects.get(id=user.id)  
        gabinete=""   
    else:
        return redirect('utilizadores:mensagem',5) 
    msg=False
    if request.method == "POST":
        submitted_data = request.POST
        if tipo == 1:
            form = ParticipanteAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Participante')
        elif tipo == 2:
            form = ProfessorUniversitarioAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Administrador')  
        else:
            return redirect('utilizadores:mensagem',5) 

        username = request.POST.get('username')
        email = request.POST.get('email')
        
        erros=[]
        if username and User.objects.exclude(username=utilizador_object.username).filter(username=username).exists():
            erros.append('O username já existe')
        elif username=="":
            erros.append('Todos os campos são obrigatórios!')

        if email and User.objects.exclude(email=utilizador_object.email).filter(email=email).exists():
            erros.append('O email já existe')
        elif email==None:
            erros.append('O email é inválido')

        if form.is_valid() and len(erros)==0:
            
            utilizador_form_object = form.save(commit=False)
            utilizador_form_object.username = username
            if tipo==2 or tipo==3 or tipo==4:
                utilizador_form_object.faculdade = Unidadeorganica.objects.get(id=submitted_data['faculdade'])
                utilizador_form_object.departamento = Departamento.objects.get(id=submitted_data['departamento'])

            
            utilizador_form_object.valido=utilizador_object.valido
            utilizador_object.delete()
            utilizador_form_object.password=utilizador_object.password
            utilizador_form_object.id=id
            utilizador_form_object.save()  
            my_group.user_set.add(utilizador_form_object)
            
            return redirect('utilizadores:mensagem',8) 
        else:
            msg=True
            return render(request=request,
                          template_name="utilizadores/mudar_perfil_admin.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'user':utilizador_object,'registo' : tipo,'msg': msg, 'erros':erros,'gabinete':gabinete,'username':username})
    else:
        username=utilizador_object.username
        return render(request=request,
                  template_name="utilizadores/mudar_perfil_admin.html",
                  context={"form": form, 'perfil': perfil,'u': u,'registo' : tipo,'user':utilizador_object,'msg': msg,'gabinete':gabinete,'username':username})





def mudar_perfil(request,tipo):  
    ''' Alterar perfil do próprio utilizador
    Redireciona para uma pagina que contem os dados já existentes do utilizador a alterar
    sendo que apenas os campos diferentes não estão preenchidos '''
     
    if request.user.is_authenticated:    
        user = get_user(request)
        id=user.id
        if user.groups.filter(name = "Coordenador").exists():
            u = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            u = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            u = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            u = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            u = "Participante" 
        else:
            u=""     
    else:
        return redirect('utilizadores:mensagem',5) 

    if tipo == 1:
        form = ParticipanteAlterarPerfilForm()
        perfil = "Participante"
    elif tipo == 2:
        form = ProfessorUniversitarioAlterarPerfilForm()
        perfil = "Professor Universitario"
    elif tipo == 3:
        form = CoordenadorAlterarPerfilForm()
        perfil = "Coordenador"
    elif tipo == 4:
        form = ColaboradorAlterarPerfilForm()
        perfil = "Colaborador"
    elif tipo == 5:
        form = AdministradorAlterarPerfilForm()
        perfil = "Administrador" 
    else:
        return redirect('utilizadores:mensagem',5) 

    user=User.objects.get(id=user.id)
    if user.groups.filter(name = "Coordenador").exists():         
        utilizador_object = Coordenador.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial =utilizador_object.faculdade.id

    elif user.groups.filter(name = "Administrador").exists():
        utilizador_object = Administrador.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
    elif user.groups.filter(name = "ProfessorUniversitario").exists():
        utilizador_object = ProfessorUniversitario.objects.get(id=user.id)
        gabinete=utilizador_object.gabinete
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial =utilizador_object.faculdade.id
    elif user.groups.filter(name = "Colaborador").exists():
        utilizador_object = Colaborador.objects.get(id=user.id) 
        gabinete=""
        if tipo!=1 and tipo!=5:
            form.fields['departamento'].initial =utilizador_object.departamento.id
            form.fields['faculdade'].initial = utilizador_object.faculdade.id
    elif user.groups.filter(name = "Participante").exists():
        utilizador_object = Participante.objects.get(id=user.id)  
        gabinete=""   
    else:
        return redirect('utilizadores:mensagem',5) 
    msg=False
    if request.method == "POST":
        submitted_data = request.POST
        if tipo == 1:
            form = ParticipanteAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Participante')
        elif tipo == 2:
            form = ProfessorUniversitarioAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='ProfessorUniversitario')
        elif tipo == 3:
            form = CoordenadorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Coordenador')
        elif tipo == 4:
            form = ColaboradorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Colaborador')
        elif tipo == 5:
            form = AdministradorAlterarPerfilForm(submitted_data)
            my_group = Group.objects.get(name='Administrador')  
        else:
            return redirect('utilizadores:mensagem',5) 

        username = request.POST.get('username')
        email = request.POST.get('email')
        
        erros=[]
        if username and User.objects.exclude(username=utilizador_object.username).filter(username=username).exists():
            erros.append('O username já existe')
        elif username=="":
            erros.append('Todos os campos são obrigatórios!')

        if email and User.objects.exclude(email=utilizador_object.email).filter(email=email).exists():
            erros.append('O email já existe')
        elif email==None:
            erros.append('O email é inválido')

        if form.is_valid() and len(erros)==0:
            
            utilizador_form_object = form.save(commit=False)
            utilizador_form_object.username = username
            if tipo==2 or tipo==3 or tipo==4:
                utilizador_form_object.faculdade = Unidadeorganica.objects.get(id=submitted_data['faculdade'])
                utilizador_form_object.departamento = Departamento.objects.get(id=submitted_data['departamento'])

            if tipo == 1:
                utilizador_form_object.valido="True"
            else:
                utilizador_form_object.valido="False"
            utilizador_form_object.password=utilizador_object.password
            utilizador_object.delete()
            utilizador_form_object.id=id
            utilizador_form_object.save()  
            my_group.user_set.add(utilizador_form_object)

            if tipo == 2 or tipo == 3 or tipo == 4 or tipo == 5: #Enviar Notificacao Automatica !!!!!!!!!
                recipient_id = utilizador_form_object.id #Enviar Notificacao Automatica !!!!!!!!!
                views.enviar_notificacao_automatica(request,"validarAlteracoesPerfil",recipient_id) #Enviar Notificacao Automatica !!!!!!!!!
            return redirect('utilizadores:logout') 
        else:
            msg=True
            return render(request=request,
                          template_name="utilizadores/mudar_perfil.html",
                          context={"form": form, 'perfil': perfil, 'u': u,'user':utilizador_object,'registo' : tipo,'msg': msg, 'erros':erros,'gabinete':gabinete,'username':username})
    else:
        username=utilizador_object.username
        return render(request=request,
                  template_name="utilizadores/mudar_perfil.html",
                  context={"form": form, 'perfil': perfil,'u': u,'registo' : tipo,'user':utilizador_object,'msg': msg,'gabinete':gabinete,'username':username})

