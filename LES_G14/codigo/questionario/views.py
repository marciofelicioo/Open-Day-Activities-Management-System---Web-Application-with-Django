from django.utils import timezone
import json
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from configuracao.models import Diaaberto
from .models import Questionario, Pergunta, OpcaoResposta, TemaQuestionario, Estado
from .forms import PerguntaForm, PublicarQuestionarioForm, QuestionarioForm
from utilizadores.models import Administrador
from utilizadores.views import user_check
from .tables import QuestionarioTable
from reportlab.lib.pagesizes import letter
import io
from django.http import FileResponse, HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from reportlab.lib.utils import simpleSplit
from django.views.decorators.http import require_POST
from django.db import OperationalError
from django.core.mail import send_mail
from django.contrib import messages
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .filters import QuestionarioFilter
from datetime import timedelta
from reportlab.lib import colors
from reportlab.lib import colors
from .models import Resposta 

def criar_questionario(request, id=None):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    
    temas = TemaQuestionario.objects.all()
    questionario = None
    if id:
        questionario = get_object_or_404(Questionario, id=id)
    form = QuestionarioForm(request.POST or None, instance=questionario)
      
    ano_atual = now().year  
    
    try:
        diaaberto_atual = Diaaberto.objects.get(ano=ano_atual)
    except Diaaberto.DoesNotExist:
        diaaberto_atual = None
        messages.success(request, "Questionário criado com sucesso!")
        return render(request, 'mensagem.html', {'tipo':'warning', 'm':'Não há dia Aberto criado para este ano'}) 
    
    titulos_existentes = Questionario.objects.values_list('titulo', flat=True)
    descricoes_existentes = Questionario.objects.values_list('descricao', flat=True)
    
    if request.method == 'POST' and form.is_valid():
        questionario = form.save(commit=False)  
        questionario.data_publicacao = None
        if diaaberto_atual:
            questionario.diaaberto = diaaberto_atual  
        questionario.save()  
        
        estado = Estado.objects.create(estado='criado', questionario=questionario)
        estado.save()
        questionario.estado = estado
        questionario.save()
        
        temaCount = sum(1 for key in request.POST.keys() if key.startswith('pergunta'))
        
        for idx in range(1, temaCount + 1):
            texto_pergunta = request.POST.get(f'perguntas{idx}', '').strip()
            tema_id = request.POST.get(f'tema{idx}', None)
            tipo_resposta = request.POST.get(f'tipoResposta{idx}', 'porExtenso').strip()

            if texto_pergunta:
                try:
                    tema = TemaQuestionario.objects.get(pk=tema_id) if tema_id else None
                except ObjectDoesNotExist:
                    tema = None

                pergunta = Pergunta.objects.create(
                    texto=texto_pergunta,
                    questionario=questionario,
                    tipo=tipo_resposta,
                    tema=tema
                )
                if tipo_resposta in ['escolhaMultipla', 'inteiro']:
                    opcoes = request.POST.getlist(f'respostaOpcao{idx}[]')
                    for opcao_texto in opcoes:
                        OpcaoResposta.objects.create(
                            texto=opcao_texto,
                            pergunta=pergunta
                        )
                
        messages.success(request, "Questionário criado com sucesso!")
        return render(request, 'mensagem.html', {'tipo':'success', 'm':'Questionário criado com sucesso'}) 
    
    return render(request, 'questionarios/criar_questionario.html', {
        'form': form,
        'temas': temas,
        'questionario': questionario,
        'titulos_existentes': list(titulos_existentes),
        'descricoes_existentes': list(descricoes_existentes),
    })
def remover_pergunta(request):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    
    if request.method == 'POST' and request.is_ajax():
        pergunta_id = request.POST.get('pergunta_id')
        print("ID da pergunta recebido:", pergunta_id)
        try:
            pergunta = Pergunta.objects.get(id=pergunta_id)
            pergunta.delete()
            return JsonResponse({"success": True})
        except Pergunta.DoesNotExist:
            return JsonResponse({"success": False, "error": "Pergunta não encontrada."})
    return JsonResponse({"success": False, "error": "Requisição inválida."})



def editar_questionario(request, id=None):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')

    questionario = get_object_or_404(Questionario, id=id) if id else None
    form = QuestionarioForm(request.POST or None, instance=questionario)
    temas = TemaQuestionario.objects.all()
    opcoes = OpcaoResposta.objects.all()
    if questionario:
        titulos_existentes = Questionario.objects.exclude(id=questionario.id).values_list('titulo', flat=True)
        descricoes_existentes = Questionario.objects.exclude(id=questionario.id).values_list('descricao', flat=True)
    else:
        titulos_existentes = Questionario.objects.values_list('titulo', flat=True)
        descricoes_existentes = Questionario.objects.values_list('descricao', flat=True)
    if request.method == 'POST' and form.is_valid():
        questionario = form.save(commit=False)  
        questionario.save()
        
        temaCount_pergunta_id = max([int(key.split('_')[-1]) for key in request.POST.keys() if key.startswith('pergunta_id_')], default=0)
        temaCount_perguntas = max([int(key.replace('perguntas', '')) for key in request.POST.keys() if key.startswith('perguntas')], default=0)
        
        for idx in range(1, temaCount_pergunta_id + 1):  
            pergunta_id = request.POST.get(f'pergunta_id_{idx}', None)
            texto_pergunta = request.POST.get(f'perguntas{idx}', '').strip()
            tema_id = request.POST.get(f'tema{idx}', None)
            tipo_resposta = request.POST.get(f'tipoResposta{idx}', 'porExtenso').strip()
            if pergunta_id: 
                try:
                    tema_id = request.POST.get(f'tema{idx}', None)
                    tipo_resposta = request.POST.get(f'tipoResposta{idx}', 'porExtenso').strip()
                    texto_pergunta = request.POST.get(f'perguntas{idx}', '').strip()

                    if tema_id:
                        tema = TemaQuestionario.objects.get(pk=tema_id)
                    else:
                        tema = None

                    pergunta = Pergunta.objects.get(id=pergunta_id)
                    
                    
                    pergunta_data = {
                        'texto': texto_pergunta,
                        'questionario': pergunta.questionario.id,  
                        'tipo': tipo_resposta,
                        'tema': tema_id  
                    }
                    
                    form = PerguntaForm(pergunta_data, instance=pergunta)
                    if form.is_valid():
                        form.save()  
                            
                    
                    if tipo_resposta in ['escolhaMultipla', 'inteiro']:
                        opcoes_enviadas = request.POST.getlist(f'respostaOpcao{idx}[]')
                        opcoes_existentes = list(pergunta.opcoes_resposta.values_list('id', 'texto'))
                        
                        for texto_opcao in opcoes_enviadas:
                           
                            opcao_match = next((o for o in opcoes_existentes if o[1] == texto_opcao), None)
                            
                            if opcao_match:
                                
                                opcoes_existentes.remove(opcao_match)
                            else:
                                
                                OpcaoResposta.objects.create(pergunta=pergunta, texto=texto_opcao)

                        
                        opcoes_ids_para_deletar = [o[0] for o in opcoes_existentes]
                        OpcaoResposta.objects.filter(id__in=opcoes_ids_para_deletar).delete()
                except ObjectDoesNotExist:
                    pass

        if temaCount_perguntas - temaCount_pergunta_id > 0:
            for idx in range(temaCount_pergunta_id + 1, temaCount_perguntas + 1):
                texto_pergunta = request.POST.get(f'perguntas{idx}', '').strip()
                tema_id = request.POST.get(f'tema{idx}', None)
                tipo_resposta = request.POST.get(f'tipoResposta{idx}', 'porExtenso').strip()
                if texto_pergunta:
                    try:
                        tema = TemaQuestionario.objects.get(pk=tema_id) if tema_id else None
                    except ObjectDoesNotExist:
                        tema = None

                    pergunta = Pergunta.objects.create(
                        texto=texto_pergunta,
                        questionario=questionario,
                        tipo=tipo_resposta,
                        tema=tema
                    )
                    print(f"Pergunta criada: ID={pergunta.id}, Texto='{pergunta.texto}', Tipo='{pergunta.tipo}', Tema='{tema}'")
                    if tipo_resposta in ['escolhaMultipla', 'inteiro']:
                        opcoes = request.POST.getlist(f'respostaOpcao{idx}[]')
                        for opcao_texto in opcoes:
                            OpcaoResposta.objects.create(
                                texto=opcao_texto,
                                pergunta=pergunta
                            )
        
        messages.success(request, "Questionário atualizado com sucesso!")
        return render(request, 'mensagem.html', {'tipo':'success', 'm':'Questionário atualizado com sucesso'}) 

    
    perguntas_e_opcoes = [
        {
            'id': pergunta.id,
            'texto': pergunta.texto,
            'tipo': pergunta.tipo,
            'tema_id': pergunta.tema_id,
            'opcoes': [opcao['texto'] for opcao in pergunta.opcoes_resposta.values('texto')]
        }
        for pergunta in questionario.perguntas.all()
    ]

    return render(request, 'questionarios/editar_questionario.html', {
        'form': form,
        'temas': temas,
        'questionario': questionario,
        'perguntas_e_opcoes': perguntas_e_opcoes,
        'titulos_existentes': list(titulos_existentes),
        'descricoes_existentes': list(descricoes_existentes),
    })

def consultar_questionario(request, id=None):
    
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    existe_publicado = Questionario.objects.filter(estado__estado='publicado').exists()
    
    questionario = get_object_or_404(Questionario, id=id) if id else None
    temas = TemaQuestionario.objects.all()
   
    perguntas_e_opcoes = []
    if questionario:
        perguntas_e_opcoes = [
            {
                'id': pergunta.id,
                'texto': pergunta.texto,
                'tipo': pergunta.tipo,
                'tema_id': pergunta.tema_id,
                'opcoes': [opcao['texto'] for opcao in pergunta.opcoes_resposta.values('texto')]
            }
            for pergunta in questionario.perguntas.all()
        ]
    if request.method == 'POST':
        return render(request=request,template_name="mensagem.html", context={
            'tipo':"info", 
            'm':"consultado"
        })
    
    return render(request, 'questionarios/consultar_questionario.html', {
        'temas': temas,
        'questionario': questionario,
        'perguntas_e_opcoes': perguntas_e_opcoes,
        'existe_publicado': existe_publicado,
    })


def listar_questionarios(request):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')

    ano_atual = now().year
    try:
        diaaberto_atual = Diaaberto.objects.get(ano=ano_atual)
        ano_diaaberto_atual = diaaberto_atual.ano
    except Diaaberto.DoesNotExist:
        ano_diaaberto_atual = None
   
    try:
        query = Questionario.objects.all()
    except OperationalError as e:
        return render(request, 'erro.html', {'mensagem': 'A base de dados está temporariamente indisponível. Por favor, tente novamente mais tarde.'})

    # Filtra por data de criação, se fornecido
    data = request.GET.get('data')
    if data:
        query = query.filter(created_at__date=data)

    questionarios = Questionario.objects.exclude(estado__estado='arquivado')  
    
    estado_selecionado = request.GET.get('estado')
    if estado_selecionado == 'arquivado':
        questionarios = Questionario.objects.all()  

    filter = QuestionarioFilter(request.GET, queryset=questionarios)
    query = filter.qs  
    
    # diaaberto_atual = Diaaberto.objects.get(ano=timezone.now().year)
    # current_time = timezone.now()
    # current_time += timedelta(hours=1)
    # questionario_validado = Questionario.objects.filter(estado__estado='validado').first()
    # if current_time >= diaaberto_atual.datadiaabertofim and questionario_validado:
    #     publicar_questionario(request=request, questionario_id=questionario_validado.id)
    
    
    table = QuestionarioTable(query)
    context = {
        'data_fim_diaaberto': diaaberto_atual.datadiaabertofim,
        'table': table,
        'filter': filter 
    }
    return render(request, 'questionarios/listar_questionarios.html', context)


def validar_questionario(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    try:
        questionario = get_object_or_404(Questionario, id=questionario_id)

        if questionario.estado.estado == 'criado':
            questionario.estado.estado = 'validado'
            questionario.estado.save()
            questionario.data_validacao = now()
            questionario.data_publicacao = None
            questionario.save()
            messages.success(request, "Questionário validado com sucesso!")
            return render(request, 'mensagem.html', {'tipo': 'info', 'm': 'Questionário validado com sucesso!'})

        else:
            messages.error(request, "Ação inválida para o estado atual do questionário.")
    except OperationalError as e:
        messages.success(request, "A base de dados está temporariamente indisponível. Por favor, tente novamente mais tarde.")
        return render(request, 'mensagem.html', {'tipo': 'info', 'm': 'A base de dados está temporariamente indisponível. Por favor, tente novamente mais tarde.'})        
    return redirect('questionario:listar-questionario')

def arquivar_questionario(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    
    questionario = get_object_or_404(Questionario, id=questionario_id)

    if questionario.estado.estado in ['criado', 'validado']:
        questionario.estado.estado = 'arquivado'
        questionario.estado.save()
        questionario.data_validacao = None
        questionario.data_publicacao = None
        questionario.data_arquivo = now()
        questionario.save()
        messages.success(request, "Questionário arquivado com sucesso!")
        return render(request, 'mensagem.html', {'tipo': 'success', 'm': 'Questionário arquivado com sucesso!'})

    else:
        messages.error(request, "Ação inválida para o estado atual do questionário.")
    return redirect('questionario:listar-questionario')

def publicar_questionario(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    
    if Questionario.objects.filter(estado__estado='publicado').exists():
        messages.success(request, "Questionário não pode ser publicado pois já existe um publicado!")
        return render(request, 'mensagem.html', {'tipo': 'warning', 'm': 'Questionário não pode ser publicado pois já existe um publicado!'})

    try:
        questionario = get_object_or_404(Questionario, id=questionario_id)    
        try:
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()  
            server.login('a76999@ualg.pt', '4JC$87E!$') 

            msg = MIMEMultipart()
            msg['From'] = 'a76999@ualg.pt'
            msg['To'] = 'hugofelicio02@gmail.com'
            msg['Subject'] = 'Publicação de Questionário'

            body = 'Questionário já se encontra Publicado!'
            msg.attach(MIMEText(body, 'plain', 'utf-8'))  

            
            server.send_message(msg)
            print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
        finally:
            server.quit()

        if questionario.estado.estado == 'validado':
            questionario.estado.estado = 'publicado'
            questionario.estado.save()
            questionario.data_publicacao = now()
            questionario.data_validacao = None
            questionario.save()
            messages.success(request, "Questionário publicado com sucesso!")

            return render(request, 'mensagem.html', {'tipo': 'success', 'm': 'Questionário publicado com sucesso!'})

        else:
            messages.error(request, "Ação inválida para o estado atual do questionário.")
    except OperationalError as e:
        messages.success(request, "A base de dados está temporariamente indisponível. Por favor, tente novamente mais tarde.")
        return render(request, 'mensagem.html', {'tipo': 'info', 'm': 'A base de dados está temporariamente indisponível. Por favor, tente novamente mais tarde.'})
    return redirect('questionario:listar-questionario')

def remover_publicacao(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')

    try:
        questionario = get_object_or_404(Questionario, id=questionario_id)
        if Resposta.objects.filter(questionario_id=questionario_id, respondida = 1).exists():
            messages.error(request, "Não é possível remover um questionário da publicação que contenha respostas.")
            return render(request, 'mensagem.html', {'tipo':'error', 'm':'Não é possível remover um questionário da publicação que contenha respostas.'})
        try:
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()  
            server.login('a76999@ualg.pt', '4JC$87E!$') 

            msg = MIMEMultipart()
            msg['From'] = 'a76999@ualg.pt'
            msg['To'] = 'hugofelicio02@gmail.com'
            msg['Subject'] = 'Remoção da publicação'

            body = 'Questionário removido da publicação.'
            msg.attach(MIMEText(body, 'plain', 'utf-8'))  

            
            server.send_message(msg)
            print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
        finally:
            server.quit()
        if questionario.estado.estado == 'publicado':
            questionario.estado.estado = 'validado'
            questionario.estado.save()
            questionario.data_validacao = None
            questionario.data_publicacao = None
            questionario.save()
            messages.success(request, "Questionário removido da publicação.")
            return render(request, 'mensagem.html', {'tipo': 'error', 'm': 'Questionário removido da publicação.'})
        else:
            messages.error(request, "Ação inválida para o estado atual do questionário.")
    except OperationalError as e:
        messages.success(request, "A base de dados está temporariamente indisponível. Por favor, tente novamente mais tarde.")
        return render(request, 'mensagem.html', {'tipo': 'info', 'm': 'A base de dados está temporariamente indisponível. Por favor, tente novamente mais tarde.'})        
    return redirect('questionario:listar-questionario')

def rejeitar_questionario(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    try:
        questionario = get_object_or_404(Questionario, id=questionario_id)
        try:
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()  
            server.login('a76999@ualg.pt', '4JC$87E!$') 

            msg = MIMEMultipart()
            msg['From'] = 'a76999@ualg.pt'
            msg['To'] = 'hugofelicio02@gmail.com'
            msg['Subject'] = 'Rejeição de Questionário'

            body = 'Questionário Rejeitado.'
            msg.attach(MIMEText(body, 'plain', 'utf-8'))  

            
            server.send_message(msg)
            print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
        finally:
            server.quit()
        if questionario.estado.estado == 'criado':
            questionario.estado.estado = 'criado'
            questionario.estado.save()
            questionario.data_validacao = None
            questionario.data_publicacao = None
            questionario.save()
            messages.success(request, "Questionário rejeitado")
            return render(request, 'mensagem.html', {'tipo': 'error', 'm': 'Questionário rejeitado'})
        else:
            messages.error(request, "Ação inválida para o estado atual do questionário.")
    except OperationalError as e:
        messages.success(request, "A base de dados está temporariamente indisponível. Por favor, tente novamente mais tarde.")
        return render(request, 'mensagem.html', {'tipo': 'info', 'm': 'A base de dados está temporariamente indisponível. Por favor, tente novamente mais tarde.'})        
    return redirect('questionario:listar-questionario')

def remover_arquivo(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    
    questionario = get_object_or_404(Questionario, id=questionario_id)

    if questionario.estado.estado == 'arquivado':
        questionario.estado.estado = 'criado'
        questionario.estado.save()
        questionario.data_validacao = None
        questionario.data_publicacao = None
        questionario.save()
        messages.success(request, "Questionário removido dos arquivados")
        return render(request, 'mensagem.html', {'tipo': 'info', 'm': 'Questionário removido dos arquivados'})

    else:
        messages.error(request, "Ação inválida para o estado atual do questionário.")
    return redirect('questionario:listar-questionario')
             
def remover_validacao(request, questionario_id):
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    
    questionario = get_object_or_404(Questionario, id=questionario_id)


    if questionario.estado.estado == 'validado':
        questionario.estado.estado = 'criado'
        questionario.estado.save()
        questionario.data_validacao = None
        questionario.data_publicacao = None
        questionario.data_arquivo = None
        questionario.save()
        messages.success(request, "Questionário Desvalidado")
        return render(request, 'mensagem.html', {'tipo': 'info', 'm': 'Questionário Desvalidado.'})

    else:
        messages.error(request, "Ação inválida para o estado atual do questionário.")
    return redirect('questionario:listar-questionario')             

def eliminar_questionario(request, id):
    
    user_check_var = user_check(request=request, user_profile=[Administrador])
    if not user_check_var.get('exists'):
        return user_check_var.get('render')
    
    questionario = get_object_or_404(Questionario, id=id)

    if Resposta.objects.filter(questionario_id=id, respondida = 1).exists():
        messages.error(request, "Não é possível eliminar o questionário porque existem respostas associadas.")
        return render(request, 'mensagem.html', {'tipo':'error', 'm':'Não é possível eliminar um questionário com respostas associadas.'})

    if request.method == 'POST':
        questionario.delete()
        messages.success(request, "Questionário eliminado com sucesso!")
        return render(request, 'mensagem.html', {'tipo':'success', 'm':'Questionário eliminado'}) 
    else:
        return render(request, 'questionarios/confirmar_eliminar.html', {'questionario': questionario})
    
def drawWrappedString(c, text, width, x, y):
    
    lines = simpleSplit(text, "Helvetica", 12, width)
    for line in lines:
        c.drawString(x, y, line)
        y -= 14 
    return y  


def questionario_pdf(request, id):
    questionario = Questionario.objects.get(id=id)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    def check_page(y_pos):
        if y_pos < 100:  # Mais espaço para evitar cortes
            p.showPage()
            return height - 50  # Recomeça mais abaixo do topo da página
        return y_pos

    logo_path = 'questionario/images/logo_fct_1024x512.jpg'
    p.drawImage(logo_path, (width - 200) / 2, height - 150, width=200, height=100, mask='auto')
    y_position = height - 220
    p.setFont("Helvetica-Bold", 14)
    p.drawString((width - p.stringWidth(questionario.titulo, "Helvetica-Bold", 14)) / 2, y_position, questionario.titulo)
    
    y_position -= 40
    y_position = check_page(y_position)
    p.setFont("Helvetica", 12)
    y_position = drawWrappedString(p, questionario.descricao, width-100, 40, y_position)

    p.setLineWidth(1)
    p.setStrokeColor(colors.black)
    p.line(10, y_position-5, width - 10, y_position-5)

    y_position = check_page(y_position)
    if questionario.estado.estado == 'criado':
        p.saveState()
        p.rotate(45)
        p.setFillColor(colors.red)
        p.setFont("Helvetica-Bold", 60)
        
        
        draft_x = 690
        draft_y = 100
        draft_text = "DRAFT"
        
        
        p.drawString(draft_x, draft_y, draft_text)
        p.restoreState()

        
        text_width = p.stringWidth(draft_text, "Helvetica-Bold", 60)

        
        rect_x = draft_x - 10  
        rect_y = draft_y - 20  
        rect_width = text_width + 20  
        rect_height = 80  

        
        p.saveState()
        p.rotate(45)
        p.setStrokeColor(colors.red)
        p.setLineWidth(1)
        p.rect(rect_x, rect_y, rect_width, rect_height, stroke=1, fill=0)
        p.restoreState()

    y_position -= 20  
    for tema in TemaQuestionario.objects.filter(perguntas__questionario=questionario).distinct():
        perguntas = Pergunta.objects.filter(questionario=questionario, tema=tema)
        y_position -= 20
        y_position = check_page(y_position)
        p.setFont("Helvetica-Bold", 12)
        p.drawString((width - p.stringWidth(tema.tema, "Helvetica-Bold", 12)) / 2 + 20, y_position, tema.tema)
        
        p.setFont("Helvetica", 12)
        for index, pergunta in enumerate(perguntas):
            y_position -= 20
            y_position = check_page(y_position)
            p.drawString(50, y_position, f"{index + 1}. {pergunta.texto}")
            if pergunta.tipo == 'porExtenso':
                if y_position < 40: 
                    p.showPage()
                    y_position = height 
                    p.setFont("Helvetica", 12)
                p.rect(30, y_position - 80, 550, 70, fill=0)
                y_position -= 70   
            for opcao in OpcaoResposta.objects.filter(pergunta=pergunta):
                y_position -= 20
                y_position = check_page(y_position)
                p.rect(50, y_position, 10, 10, fill=0)
                p.drawString(60, y_position, f" {opcao.texto}")
            y_position -= 30 
    # Adicionar perguntas finais
    final_questions = [
        "Gostou das respostas deste questionário? Coloque um círculo em uma das opções.",
        "Escala de 1 a 5:",
        "Houve alguma pergunta cuja respostas não tenha gostado?, se sim diga qual e porque ?",
        "Quais as atividades que frequentou ?, Quanto daria de 1 a 5 a cada uma delas ?",
        "Quais as atividades que menos gostou ?, Porque ?"
    ]

    for question in final_questions:
        y_position -= 20
        y_position = check_page(y_position)
        p.drawString(50, y_position, question)
        
        if question == "Escala de 1 a 5:":
            for i in range(1, 6):
                y_position = check_page(y_position)
                p.drawString(150 + i * 20, y_position, str(i))
        y_position -= 30     
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')