import django_tables2 as tables
from coordenadores.models import *
from django.utils.html import format_html
from django.db.models import Count
from coordenadores.models import TarefaAuxiliar
from datetime import time
from django.urls import reverse

class TarefaTable(tables.Table):
    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    tipo = tables.Column('Tipo',accessor='tipo_frontend')
    colab = tables.Column('Colaborador',default='N/A')
    class Meta:
        model = Tarefa
        sequence = ('nome','colab','dia','horario','estado','tipo','acoes')
    
    def before_render(self,request):
        self.columns.hide('id')
        self.columns.hide('coord')
        self.columns.hide('created_at')
        self.columns.hide('diaaberto')

    def render_acoes(self,record):
        if record.estado == "Concluida":
            return  format_html(f"""
                <div style="margin-left:1.8rem">
                    <a onclick="alert.render('Tem a certeza que pretende eliminar esta tarefa?','{reverse('coordenadores:eliminarTarefa', kwargs={'id':record.id})}')">               
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
                </div> 
            """)
        elif record.estado == "Iniciada":
            return  format_html(f"""
            """)
        else:
            return  format_html(f"""
                <div>
                    <a id='edit' href="{reverse('coordenadores:alterarTarefa', kwargs={'id':record.id})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                    &nbsp;
                    <a onclick="alert.render('Tem a certeza que pretende eliminar esta tarefa?','{reverse('coordenadores:eliminarTarefa', kwargs={'id':record.id})}')">               
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
                </div> 
            """)

    def render_estado(self,record):
        if record.estado == "naoConcluida":
            return format_html(f"""
                <span class="tag text is-warning" data-value="naoConcluida" style="width: 7rem;font-size: small;">Não Concluida</span>
                """)
        elif record.estado == "Concluida":
            return format_html(f"""                    
                <span class="tag text is-success" data-value="Concluida" style="width: 7rem;font-size: small;">Concluida</span>
                """)
        elif record.estado == "naoAtribuida":
            return format_html(f"""                    
                <span class="tag text is-danger" data-value="naoAtrbuida" style="width: 7rem;font-size: small;">Não Atribuida</span>
                """)
        elif record.estado == "Iniciada":
            return format_html(f"""
                <span class="tag text is-primary is-loading" data-value="Iniciada" style="width: 7rem;font-size: small;">Iniciada</span>
            """)
        elif record.estado == 'Cancelada':
            return format_html(f"""
                <span class="tag text is-danger " data-value="Cancelada" style="width: 7rem;font-size: small;">Cancelada</span>
            """)              

    def render_horario(self,record):
        if record.tipo == 'tarefaAuxiliar':
            tarefa = TarefaAuxiliar.objects.get(tarefaid=record.id)
            return time.strftime(tarefa.sessao.horarioid.inicio,"%H:%M") + ' - ' + time.strftime(tarefa.sessao.horarioid.fim,"%H:%M")
        else: return record.horario       
    
    def render_colab(self,record):
        return record.colab.full_name