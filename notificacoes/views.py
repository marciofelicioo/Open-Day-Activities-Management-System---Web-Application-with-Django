from django.http import HttpResponse
from .models import *
from utilizadores.models import *
from configuracao.models import *
from coordenadores.models import *
from atividades.models import *
import math

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import *
from django.conf import settings
from django.contrib.auth.models import Group

from django.core.paginator import Paginator

from notifications.signals import notify
from django.utils import timezone

from datetime import datetime, timedelta

from .forms import *

from django.http import HttpResponseRedirect

def apagar_notificacao_automatica(request, id ,nr):
    ''' Apagar uma notificação automática '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    try:    
        notificacao = Notificacao.objects.get(id=nr)
    except:
        return redirect("utilizadores:mensagem", 5)
    if notificacao == None:
        return redirect("utilizadores:mensagem", 5)
    notificacao.delete()
   
    page=request.GET.get('page')
    response = redirect('notificacoes:categorias-notificacao-automatica', id, 0)
    response['Location'] += '?page='+page
    return response


def limpar_notificacoes(request, id):
    ''' Apagar notificacoes de um utilizadore por categorias '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    if id == 1:
        notificacoes = user.notifications.unread() 
    elif id ==2:
        notificacoes = user.notifications.read() 
    elif id == 3:
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=False)
    elif id ==4:    
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=True)
    elif id == 5:
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="info")
    elif id ==6:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="warning")
    elif id ==7: 
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="error")
    elif id ==8:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="success")
    else:
        notificacoes = user.notifications.all()
    for x in notificacoes:
        x.delete()

    return redirect('notificacoes:categorias-notificacao-automatica',0,0)




def marcar_como_lida(request):
    ''' Marcar todas as notificações de um utilizador como lidas '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    user.notifications.mark_all_as_read(user)
    return redirect('notificacoes:categorias-notificacao-automatica',0,0)






def sem_notificacoes(request, id):
    ''' Página quando não existem notificacoes '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)

    return render(request, 'notificacoes/sem_notificacoes.html', {
        'categoria':id,
    })




def categorias_notificacao_automatica(request, id, nr):
    ''' Ver notificações automáticas por categorias '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    x = 0   
    if id == 1:
        notificacoes = user.notifications.unread().order_by('-id') 
    elif id ==2:
        notificacoes = user.notifications.read().order_by('-id') 
    elif id == 3:
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=False).order_by('-id')
    elif id ==4:    
        notificacoes = Notificacao.objects.filter(recipient_id=user , public=True).order_by('-id')
    elif id == 5:
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="info").order_by('-id')
    elif id ==6:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="warning").order_by('-id')
    elif id ==7: 
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="error").order_by('-id')
    elif id ==8:  
        notificacoes = Notificacao.objects.filter(recipient_id=user , level="success").order_by('-id')
    else:
        notificacoes = user.notifications.all().order_by('-id')
    
    x = len(notificacoes)
    if nr!=0:
        try:
            notificacao = Notificacao.objects.get(id=nr)
        except:  
            if x>0:
                notificacao = notificacoes[0]
            else:
                return redirect("notificacoes:sem-notificacoes", id)      
    else:
        if x>0:
            notificacao = notificacoes[0]
        else:
            return redirect("notificacoes:sem-notificacoes", id)    
    nr_notificacoes_por_pagina = 15
    paginator= Paginator(notificacoes,nr_notificacoes_por_pagina)
    page=request.GET.get('page')
    notificacoes = paginator.get_page(page)
    total = x
    if notificacao != None:
        notificacao.unread = False
        notificacao.save()
    else:
        return redirect("utilizadores:mensagem", 5)
    return render(request, 'notificacoes/detalhes_notificacao_automatica.html', {
        'atual': notificacao, 'notificacoes':notificacoes,'categoria':id,'total':total
    })




def enviar_notificacao_automatica(request, sigla, id):
    ''' Envio de notificação automatica '''
    if request.user.is_authenticated:
        user_sender = get_user(request)
    elif sigla!="validarRegistosPendentes":
        return redirect('utilizadores:mensagem', 5)
    # Enviar notificacao ao cancelar tarefa - colaborador
    if sigla == "cancelarTarefa":
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Pedido de cancelamento da tarefa"
        descricao = "Foi feito um pedido de cancelamento da tarefa \"" + \
            tarefa.getDescription()+"\""
        user_recipient = Utilizador.objects.get(id=tarefa.coord.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                    target=None, level="error", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificacao ao enviar confirmação do cancelamento da tarefa - coordenador
    elif sigla == "confirmarCancelarTarefa":
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Confirmação do cancelamento da tarefa"
        descricao = "O cancelamento da sua tarefa \"" + \
            tarefa.getDescription()+"\" foi aprovado."
        user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                    target=None, level="success", description=titulo, public=False, timestamp=timezone.now())
        tarefa.colab=None
        tarefa.save()
    # Enviar notificação ao enviar rejeicao do pedido de cancelamento da tarefa - coordenador
    elif sigla == "rejeitarCancelarTarefa":
        tarefa = Tarefa.objects.get(id=id)
        titulo = "Pedido de cancelamento da tarefa rejeitado"
        descricao = "O pedido de cancelamento da tarefa \"" + \
            tarefa.getDescription()+"\" foi rejeitado."
        user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                    target=None, level="warning", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação atividade confirmada - professor universitario
    elif sigla == "confirmarAtividade":
        atividade = Atividade.objects.get(id=id)
        titulo = "Confirmação da atividade proposta"
        descricao = "A sua proposta de atividade \""+atividade.nome+"\" foi aceite."
        user_recipient = Utilizador.objects.get(
            id=atividade.professoruniversitarioutilizadorid.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=None,
                    target=atividade, level="success", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação atividade rejeitada - professor universitario
    elif sigla == "rejeitarAtividade":
        atividade = Atividade.objects.get(id=id)
        titulo = "Rejeição da atividade proposta"
        descricao = "A sua proposta de atividade "+atividade.nome+" foi rejeitada."
        user_recipient = Utilizador.objects.get(
            id=atividade.professoruniversitarioutilizadorid.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=None,
                    target=atividade, level="error", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificacao tarefa atribuida - colaborador
    elif sigla == "tarefaAtribuida":
        tarefa = Tarefa.objects.get(id=id)
        if tarefa.estado != "naoAtribuida":
            titulo = "Atribuição de uma tarefa"
            descricao = "Foi lhe atribuida a tarefa \""+tarefa.getDescription()+"\""
            user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
            notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                        target=None, level="success", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação tarefa apagada - colaborador
    elif sigla == "tarefaApagada":
        titulo = "Foi apagada uma tarefa"
        tarefa = Tarefa.objects.get(id=id)
        descricao = "Foi apagada a tarefa \""+tarefa.getDescription() + \
            "\", por esse motivo a tarefa deixou de lhe estar atribuída."
        user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                    target=None, level="error", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação tarefa alterada - colaborador
    elif sigla == "tarefaAlterada":
        tarefa = Tarefa.objects.get(id=id)
        if tarefa.estado != "naoAtribuida":
            titulo = "Alteração de uma tarefa"
            descricao = "Foi alterada a tarefa \""+tarefa.getDescription()+"\""
            user_recipient = Utilizador.objects.get(id=tarefa.colab.id)
            notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=tarefa,
                        target=None, level="info", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação atividade apagada - coordenador
    elif sigla == "atividadeApagada":
        titulo = "Foi apagada uma atividade"
        atividade = Atividade.objects.get(id=id)
        descricao = "Foi apagada a atividade \""+atividade.nome+"\""
        user_recipient = Utilizador.objects.get(
            id=atividade.get_coord().id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=None,
                    target=None, level="error", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação atividade alterada - coordenador
    elif sigla == "atividadeAlterada":
        titulo = "Foi alterada uma atividade"
        atividade = Atividade.objects.get(id=id)
        descricao = "Foi feita uma alteração na atividade \""+atividade.nome+"\""
        user_recipient = Utilizador.objects.get(
            id=atividade.get_coord().id)
        notify.send(sender=user_sender, recipient=user_recipient, verb=descricao, action_object=None,
                    target=atividade, level="warning", description=titulo, public=False, timestamp=timezone.now())
    # Enviar notificação quando há registo de utilizador por validar - administrador e ao coordenador ( 5 dias depois de criado se ainda tiver pendente
    elif sigla == "validarRegistosPendentes":  # timezone.now() + timedelta(days=5)
        titulo = "Validação de registos de utilizadores pendentes"
        descricao = "Foram feitos registos de utilizadores na plataforma que necessitam de ser validados."
        administradores = Administrador.objects.all()
        user_sender = Utilizador.objects.get(id=id)
        for x in administradores:
            user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
            info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                              descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "register "+str(id) , lido = False)
            info.save()
        if user_sender.getProfile() != "Administrador":
            coordenadores = Coordenador.objects.filter(faculdade=Unidadeorganica.objects.get(id=user_sender.getUser().faculdade.id)) 
            for x in coordenadores: 
                user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
                info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                                descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "register "+str(id) , lido = False)
                info.save()
    # Enviar notificação quando há alterações de perfil de utilizador por validar - administrador e ao coordenador ( 5 dias depois de alterado se ainda tiver pendente )
    elif sigla == "validarAlteracoesPerfil":  # timezone.now() + timedelta(days=5)
        titulo = "Alterações de perfil de utilizadores por validar"
        descricao = "Foram feitas alterações de perfil de utilizadores que necessitam de ser validadas."
        administradores = Administrador.objects.all()
        user_sender = Utilizador.objects.get(id=id)
        for x in administradores:
            user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
            info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                              descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "profile "+str(id) , lido = False)
            info.save()
        if user_sender.getProfile() != "Administrador":
            coordenadores = Coordenador.objects.filter(faculdade=Unidadeorganica.objects.get(id=user_sender.getUser().faculdade.id)) 
            for x in coordenadores: 
                user_recipient = Utilizador.objects.get(id=x.id)
                info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                                descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "profile "+str(id) , lido = False)
                info.save()
    # Enviar notificação atividades por validar pendentes - coordenador (5 dias depois de criada a atividade se ainda tiver pendente)
    elif sigla == "validarAtividades":
        titulo = "Existem atividades por validar"
        atividade = Atividade.objects.get(id=id)
        descricao = "Foram criadas propostas de atividades que têm de ser validadas."
        user_recipient = Utilizador.objects.get(
            id=atividade.get_coord().id)
        user_sender = Utilizador.objects.get(id=user_sender.id)
        info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = titulo,
                              descricao = descricao, emissor = user_sender , recetor = user_recipient, tipo = "atividade "+str(id) , lido = False)
        info.save()


######################################################### Mensagens #####################################################


def escolher_tipo(request):
    ''' Escolher tipo de mensagem a enviar, poderá ser uma mensagem de grupo ou individual '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    return render(request, 'notificacoes/escolher_tipo_mensagem.html')


def concluir_envio(request):
    ''' Página de sucesso quando a mensagem é enviada '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    return render(request, 'notificacoes/concluir_envio.html')



def criar_mensagem(request, id):
    ''' Criar uma nova mensagem tomando em consideração o tipo de utilizador que está logado atualmente no sistema '''
    if request.user.is_authenticated: 
        user = get_user(request) 
        user = Utilizador.objects.get(id=user.id)
        if user.getProfile()=="Coordenador" or user.getProfile()=="Colaborador" or user.getProfile()=="ProfessorUniversitario" :
            return redirect('notificacoes:criar-mensagem-uo', id) 
        elif user.getProfile()=="Administrador":
            return redirect('notificacoes:criar-mensagem-admin', id) 
        elif user.getProfile()=="Participante":
            return redirect('notificacoes:criar-mensagem-participante', id) 
        else:
            return redirect('utilizadores:mensagem',5 ) 
    else:
        return redirect('utilizadores:mensagem', 5)      





def criar_mensagem_participante(request, id):
    ''' Criar uma nova mensagem por um participante '''
    msg = False
    if request.user.is_authenticated: 
        user = get_user(request) 
        if user.groups.filter(name = "Participante").exists() == False:
            return redirect('utilizadores:mensagem', 5)  
        user = Utilizador.objects.get(id=user.id)
    else:
        return redirect('utilizadores:mensagem', 5)      
           
    if request.method == "POST":
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualParticipante(request.POST)
        elif tipo == 1:
            form = MensagemFormGrupoParticipante(request.POST)
        else:
            return redirect("utilizadores:mensagem",5)
        if form.is_valid():
            titulo = form.cleaned_data.get('titulo')
            mensagem = form.cleaned_data.get('mensagem')
            if tipo == 0:
                email = form.cleaned_data.get('email')
                user_recipient = Utilizador.objects.get(email=email)
                info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "Individual" , lido = False)
                info.save()
                mensagem1 = MensagemEnviada(mensagem=info)
                mensagem1.mensagem.lido = False
                mensagem1.save()
                mensagem2 = MensagemRecebida(mensagem=info)
                mensagem2.save()
            elif tipo == 1:
                tipo_utilizadores = request.POST.get('filtro_tipo')
                if tipo_utilizadores == "Administrador":
                    utilizadores = Administrador.objects.all()    
                else:
                    return redirect("utilizadores:mensagem",5)
                
                for x in utilizadores:
                    user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
                    info = InformacaoMensagem(data=timezone.now(), pendente=True, titulo = titulo,
                                    descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "Grupo de admistradores do dia aberto" , lido = False)
                    info.save()
                    if user_recipient.id != user.id:
                        tmp = MensagemRecebida(mensagem=info)
                        tmp.save()  
                mensagem1 = MensagemEnviada(mensagem=info)
                mensagem1.mensagem.lido = False
                mensagem1.save()    
            return redirect("notificacoes:concluir-envio")
        else:
            msg = True
            if tipo == 0:
                return render(request=request,
                    template_name="notificacoes/enviar_notificacao.html",
                    context={"form": form,"msg":msg,})
            elif tipo == 1:    
                form_group = UtilizadorFiltroParticipante(request.POST)
                return render(request=request,
                            template_name="notificacoes/enviar_para_grupo.html",
                            context={"form": form,"form_group":form_group,"msg":msg,})
    else:
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualParticipante()
            return render(request=request,
                  template_name="notificacoes/enviar_notificacao.html",
                  context={"form": form,"msg":msg,})
        elif tipo == 1:
            formFilter = UtilizadorFiltroParticipante()
            form = MensagemFormGrupoParticipante()
            return render(request=request,
                  template_name="notificacoes/enviar_para_grupo.html",
                  context={"form": form,"form_group":formFilter,"msg":msg,})
        else:
            return redirect("utilizadores:mensagem",5)




def criar_mensagem_uo(request, id):
    ''' Criar uma nova mensagem por um colaborador, coordenador ou docente '''
    msg = False
    if request.user.is_authenticated: 
        user = get_user(request) 
        if user.groups.filter(name = "Colaborador").exists():
            utilizador_atual_verificacao = True
        elif user.groups.filter(name = "Coordenador").exists():
            utilizador_atual_verificacao = True
        elif user.groups.filter(name = "ProfessorUniversitario").exists():     
            utilizador_atual_verificacao = True 
        else:     
            return redirect('utilizadores:mensagem', 5)  
        user = Utilizador.objects.get(id=user.id)
    else:
        return redirect('utilizadores:mensagem', 5)      

    if request.method == "POST":
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualUO(request.POST)
        elif tipo == 1:
            form = MensagemFormGrupoUO(request.POST)
        else:
            return redirect("utilizadores:mensagem",5)
        if form.is_valid():
            titulo = form.cleaned_data.get('titulo')
            mensagem = form.cleaned_data.get('mensagem')
            if tipo == 0:
                email = form.cleaned_data.get('email')
                user_recipient = Utilizador.objects.get(email=email)
                if user_recipient.emailValidoUO(user.getUser().faculdade) == False:
                    msg_erro = "Apenas pode ser enviada mensagem a coordenadores, colaboradores ou professores universitários da mesma unidade orgânica ou a administradores"
                    msg = True
                    erro = True
                    return render(request=request,
                        template_name="notificacoes/enviar_notificacao.html",
                        context={"form": form,"msg":msg,"msg_erro":msg_erro, "erro":erro})
                else:        
                    info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                    descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "Individual" , lido = False)
                    info.save()
                    mensagem1 = MensagemEnviada(mensagem=info)
                    mensagem1.mensagem.lido = False
                    mensagem1.save()
                    mensagem2 = MensagemRecebida(mensagem=info)
                    mensagem2.save()
            elif tipo == 1:
                grupo = "Grupo"
                tipo_utilizadores = request.POST.get('filtro_tipo')
                if tipo_utilizadores == "ProfessorUniversitario":
                    utilizadores = ProfessorUniversitario.objects.filter(faculdade=user.getUser().faculdade)
                    grupo = "Grupo de professores universitários"
                elif tipo_utilizadores == "Coordenador":
                    utilizadores = Coordenador.objects.filter(faculdade=user.getUser().faculdade)
                    grupo = "Grupo de coordenadores"
                elif tipo_utilizadores == "Colaborador":
                    utilizadores = Colaborador.objects.filter(faculdade=user.getUser().faculdade)
                    grupo = "Grupo de colaboradores"
                elif tipo_utilizadores == "Administrador":
                    utilizadores = Administrador.objects.filter() 
                    grupo = "Grupo de administradores do dia aberto"   
                else:
                    return redirect("utilizadores:mensagem",5)
                
                for x in utilizadores:
                    user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
                    info = InformacaoMensagem(data=timezone.now(), pendente=True, titulo = titulo,
                                    descricao = mensagem, emissor = user , recetor = user_recipient, tipo = grupo , lido = False)
                    info.save()
                    if user_recipient.id != user.id:
                        tmp = MensagemRecebida(mensagem=info)
                        tmp.save()  
                mensagem1 = MensagemEnviada(mensagem=info)
                mensagem1.mensagem.lido = False
                mensagem1.save()    
            return redirect("notificacoes:concluir-envio")
        else:
            msg = True
            if tipo == 0:
                return render(request=request,
                    template_name="notificacoes/enviar_notificacao.html",
                    context={"form": form,"msg":msg,})
            elif tipo == 1:    
                form_group = UtilizadorFiltroUO(request.POST)
                return render(request=request,
                            template_name="notificacoes/enviar_para_grupo.html",
                            context={"form": form,"form_group":form_group,"msg":msg,})
    else:
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualUO()
            return render(request=request,
                  template_name="notificacoes/enviar_notificacao.html",
                  context={"form": form,"msg":msg,})
        elif tipo == 1:
            formFilter = UtilizadorFiltroUO()
            form = MensagemFormGrupoUO()
            return render(request=request,
                  template_name="notificacoes/enviar_para_grupo.html",
                  context={"form": form,"form_group":formFilter,"msg":msg,})
        else:
            return redirect("utilizadores:mensagem",5)



def criar_mensagem_admin(request, id):
    ''' Criar uma nova mensagem por um administrador '''
    msg = False
    if request.user.is_authenticated: 
        user = get_user(request) 
        if user.groups.filter(name = "Administrador").exists() == False:
            return redirect('utilizadores:mensagem', 5) 
        user = Utilizador.objects.get(id=user.id)
    else:
        return redirect('utilizadores:mensagem', 5)      
 
    if request.method == "POST":
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualAdmin(request.POST)
        elif tipo == 1:
            form = MensagemFormGrupoAdmin(request.POST)
        else:
            return redirect("utilizadores:mensagem",5)
        if form.is_valid():
            titulo = form.cleaned_data.get('titulo')
            mensagem = form.cleaned_data.get('mensagem')
            if tipo == 0:
                email = form.cleaned_data.get('email')
                user_recipient = Utilizador.objects.get(email=email)
                info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = titulo,
                                descricao = mensagem, emissor = user , recetor = user_recipient, tipo = "Individual" , lido = False)
                info.save()
                mensagem1 = MensagemEnviada(mensagem=info)
                mensagem1.mensagem.lido = False
                mensagem1.save()
                mensagem2 = MensagemRecebida(mensagem=info)
                mensagem2.save()
            elif tipo == 1:
                grupo = ""
                tipo_utilizadores = request.POST.get('filtro_tipo')
                if tipo_utilizadores == "Participante":
                    utilizadores = Participante.objects.all()
                    grupo = "Grupo de participantes"
                elif tipo_utilizadores == "ProfessorUniversitario":
                    utilizadores = ProfessorUniversitario.objects.all()
                    grupo = "Grupo de professores universitários"
                elif tipo_utilizadores == "Coordenador":
                    utilizadores = Coordenador.objects.all()
                    grupo = "Grupo de coordenadores"
                elif tipo_utilizadores == "Colaborador":
                    utilizadores = Colaborador.objects.all()
                    grupo = "Grupo de colaboradores"
                elif tipo_utilizadores == "Administrador":
                    utilizadores = Administrador.objects.all() 
                    grupo = "Grupo de administradores do dia aberto"   
                else:
                    return redirect("utilizadores:mensagem",5)
                
                for x in utilizadores:
                    user_recipient = Utilizador.objects.get(user_ptr_id=x.utilizador_ptr_id)
                    info = InformacaoMensagem(data=timezone.now(), pendente=True, titulo = titulo,
                                    descricao = mensagem, emissor = user , recetor = user_recipient, tipo = grupo , lido = False)
                    info.save()
                    if user_recipient.id != user.id:
                        tmp = MensagemRecebida(mensagem=info)
                        tmp.save()  
                mensagem1 = MensagemEnviada(mensagem=info)
                mensagem1.mensagem.lido = False
                mensagem1.save()    
            return redirect("notificacoes:concluir-envio")
        else:
            msg = True
            if tipo == 0:
                return render(request=request,
                    template_name="notificacoes/enviar_notificacao.html",
                    context={"form": form,"msg":msg,})
            elif tipo == 1:    
                form_group = UtilizadorFiltro(request.POST)
                return render(request=request,
                            template_name="notificacoes/enviar_para_grupo.html",
                            context={"form": form,"form_group":form_group,"msg":msg,})
    else:
        tipo = id
        if tipo == 0:
            form = MensagemFormIndividualAdmin()
            return render(request=request,
                  template_name="notificacoes/enviar_notificacao.html",
                  context={"form": form,"msg":msg,})
        elif tipo == 1:
            formFilter = UtilizadorFiltro()
            form = MensagemFormGrupoAdmin()
            return render(request=request,
                  template_name="notificacoes/enviar_para_grupo.html",
                  context={"form": form,"form_group":formFilter,"msg":msg,})
        else:
            return redirect("utilizadores:mensagem",5)
    



def apagar_mensagem(request, id ,nr):
    ''' Apagar uma mensagem '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    m=""
    msg = False
    form = MensagemResposta()

    try:
        if id != 5:
            tmp = MensagemRecebida.objects.get(mensagem=nr)
        else:
            tmp = MensagemEnviada.objects.get(mensagem=nr)

        tmp.delete()
    except:
        return redirect('utilizadores:mensagem', 404)   
    
    page=request.GET.get('page')
    response = redirect('notificacoes:detalhes-mensagem', id, 0)
    response['Location'] += '?page='+page
    return response





def limpar_mensagens(request, id):
    ''' Apagar mensagens por categorias de um dado utilizador '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)

    if id == 5:
        notificacoes = MensagemEnviada.objects.select_related('mensagem__emissor').filter(mensagem__emissor=user.id)
    elif id == 1:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__lido=False) 
    elif id == 2:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__lido=True) 
    elif id == 3:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__pendente=False) 
    elif id == 4:    
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__pendente=True)
    else:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id)
    
    for x in notificacoes:
        x.delete()

    return redirect('notificacoes:detalhes-mensagem',id,0)




def mensagem_como_lida(request, id):
    ''' Marcar todas as mensagens de um utilizador como lidas '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    msgs = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id)
    for msg in msgs:
        msg.mensagem.lido = True
        msg.mensagem.save()
        msg.save()
    return redirect('notificacoes:detalhes-mensagem',0,0)






def sem_mensagens(request, id):
    ''' Página quando não existem mensagens '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)

    return render(request, 'notificacoes/sem_mensagens.html', {
        'categoria':id,
    })




def detalhes_mensagens(request, id, nr):
    ''' Ver mensagens por categorias '''
    if request.user.is_authenticated:
        user = get_user(request)
    else:
        return redirect('utilizadores:mensagem', 5)
    m=""
    if request.method == "POST":
        msg = True
        form = MensagemResposta(request.POST)
        if form.is_valid():
            mensagem = form.cleaned_data.get('mensagem')
            msg_id = form.cleaned_data.get('msg_atual')
            user_sender = Utilizador.objects.get(user_ptr_id=user.id)
            notificacao = MensagemRecebida.objects.get(id=msg_id)
            if "Re: " in notificacao.mensagem.titulo:
                t = notificacao.mensagem.titulo
            else:
                t = "Re: "+notificacao.mensagem.titulo
            info = InformacaoMensagem(data=timezone.now(), pendente=False, titulo = t ,
                            descricao = mensagem, emissor = user_sender, recetor = notificacao.mensagem.emissor, tipo = "Individual" , lido = False)
            info.save()
            mensagem1 = MensagemEnviada(mensagem=info)
            mensagem1.mensagem.lido = False
            mensagem1.save()
            mensagem2 = MensagemRecebida(mensagem=info)
            mensagem2.save()
            m = "Mensagem enviada com sucesso"
            form = MensagemResposta()
        else:
            m = ""  
    else:
        msg = False
        form = MensagemResposta()

    x = 0   
    if id == 1:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__lido=False).order_by('-id') 
    elif id == 2:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__lido=True).order_by('-id') 
    elif id == 3:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__pendente=False).order_by('-id') 
    elif id == 4:    
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id,mensagem__pendente=True).order_by('-id')
    elif id == 5:    
        notificacoes = MensagemEnviada.objects.select_related('mensagem__emissor').filter(mensagem__emissor=user.id).order_by('-id')
    else:
        notificacoes = MensagemRecebida.objects.select_related('mensagem__recetor').filter(mensagem__recetor=user.id).order_by('-id')
    
    x = len(notificacoes)
    if nr!=0:
        try:
            notificacao = MensagemRecebida.objects.get(mensagem=nr)
        except:
            if x>0:
                notificacao = notificacoes[0]
            else:
                return redirect("notificacoes:sem-mensagens", id)       
    else:
        if x>0:
            notificacao = notificacoes[0]
        else:
            return redirect("notificacoes:sem-mensagens", id) 

    nr_notificacoes_por_pagina = 5
    paginator= Paginator(notificacoes,nr_notificacoes_por_pagina)
    page=request.GET.get('page')
    notificacoes = paginator.get_page(page)
    total = x
    if notificacao != None:
        if id != 5:
            notificacao.mensagem.lido = True
            notificacao.mensagem.save()
            notificacao.save()
    else:
        return redirect("utilizadores:mensagem", 5)
    return render(request, 'notificacoes/detalhes_mensagens.html', {
        "form": form,'atual': notificacao, 'notificacoes':notificacoes,'categoria':id,'total':total,"msg": msg,"m":m
    })

