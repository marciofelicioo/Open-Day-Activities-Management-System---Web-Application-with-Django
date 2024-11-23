from django.utils.html import format_html
import django_tables2 as tables
from django_tables2.utils import A
from .models import Questionario
from django.urls import reverse
from django.utils.html import format_html, escape

class QuestionarioTable(tables.Table):
    
    titulo = tables.Column(accessor='titulo', verbose_name='Título', orderable=False)
    def render_titulo(self, value):
        
        return format_html('<div title="{}">{}</div>', value, value)
    
    estado = tables.Column(empty_values=(), orderable=False)  

    editar = tables.LinkColumn('questionario:editar-questionario', args=[tables.A('pk')], attrs={
        'class': 'button is-small is-danger',
    }, text='Editar', orderable=False)

    def render_editar(self, record):
        if record.estado.estado == 'publicado' or record.estado.estado == 'validado':
            
            return format_html('')
        else:
            return format_html(
                '<a href="{0}" class="button is-small is-info" style="padding: 3px 2px; font-size: 0.75rem;">Editar</a>',
                reverse('questionario:editar-questionario', args=[record.pk]),
            )
    

    eliminar = tables.LinkColumn('questionario:eliminar-questionario', args=[tables.A('pk')], attrs={
        'class': 'button is-small is-danger',
    }, text='Eliminar', orderable=False)

    def render_eliminar(self, value, record):
        if record.estado.estado == 'publicado' or record.estado.estado == 'validado':
            
            return format_html('')
        else:
            return format_html(
                '<a href="{0}" class="button is-small is-warning">Eliminar</a>',
                reverse('questionario:eliminar-questionario', args=[record.pk]),
            )
        
    arquivar = tables.LinkColumn('questionario:arquivar_questionario', args=[tables.A('pk')], attrs={
        'class': 'button is-small is-info',
    }, text='Arquivar', orderable=False)

    def render_arquivar(self, value, record):
        if record.estado.estado == 'arquivado' :
            return format_html(
                '<a href="{0}" class="button is-small is-danger">Remover Arquivo</a>',
                reverse('questionario:remover_arquivo', args=[record.pk]),
            )  
        elif record.estado.estado == 'publicado':
            
            return format_html('')
        else:
            return format_html(
                '<a href="{0}" class="button is-small is-info">Arquivar</a>',
                reverse('questionario:arquivar_questionario', args=[record.pk]),
            )    

    publicar = tables.LinkColumn('questionario:publicar_questionario', args=[tables.A('pk')], attrs={
        'class': 'button is-small is-danger',
    }, text='Remover Publicação', orderable=False)

    def render_publicar(self, record):
        if record.estado.estado == 'arquivado' or record.estado.estado == 'criado':
            
            return format_html('')
        elif record.estado.estado == 'publicado':
             return format_html(
                '<a href="{0}" class="button is-small is-danger">Remover Publicação</a>',
                reverse('questionario:remover_publicacao', args=[record.pk]),
            )   
        else:
            return format_html(
                '<a href="{0}" class="button is-small is-success">publicar</a>',
                reverse('questionario:publicar_questionario', args=[record.pk]),
            )    
    consultar = tables.Column(empty_values=(), orderable=False) 
    def render_consultar(self, value, record):
        return format_html(
            '<a href="{0}" class="button is-small is-info">Consultar</a>',
            reverse('questionario:consultar_questionario', args=[record.pk]),
        )

    obter_pdf = tables.LinkColumn('questionario:questionario-pdf', args=[tables.A('pk')], attrs={
        'class': 'button is-small is-danger is-light',
    }, text='Obter_PDF', orderable=False)

    def Obter_PDF(self, record):
        return format_html(
            '<a href="{0}" class="button is-small is-danger is-light">Obter_Pdf</a>',
            reverse('questionario:questionario-pdf', args=[record.pk]),
        ) 
    

    class Meta:
        model = Questionario
        template_name = "django_tables2/bootstrap.html"
        fields = ("titulo","consultar")
