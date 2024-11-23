from datetime import datetime, timezone
import django_tables2 as tables
from atividades.models import *
from django.utils.html import format_html
from django.db.models import Count

from configuracao.models import Diaaberto

class CoordAtividadesTable(tables.Table):
    
    acoes = tables.Column('Operações', empty_values=())
    professoruniversitarioutilizadorid = tables.Column('Professor')
    datasubmissao = tables.Column('Data de Submissão')
    class Meta:
        model = Atividade
        sequence = ('nome','professoruniversitarioutilizadorid','tipo','datasubmissao','estado', 'acoes')
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('nrcolaboradoresnecessario')
        self.columns.hide('publicoalvo')
        #self.columns.hide('tipo')
        self.columns.hide('dataalteracao')
        self.columns.hide('duracaoesperada')
        self.columns.hide('participantesmaximo')
        self.columns.hide('espacoid')
        self.columns.hide('tema')
        self.columns.hide('diaabertoid')

    def render_estado(self,record):
        fancy_box = ""
        if record.estado == 'Aceite':
            fancy_box = f"""
            <span class="tag text is-success" style="width: 7rem;font-size: small;">Aceite</span>
            """
        elif record.estado == 'Pendente':
            fancy_box = f"""
            <span class="tag text is-warning" style="width: 7rem;font-size: small;">Pendente</span>
            """
        else:
            fancy_box = f"""
            <span class="tag text is-danger" style="width: 7rem;font-size: small;">Recusada</span>
            """          
        return format_html(fancy_box)


    def render_professoruniversitarioutilizadorid(self,record):
        return str(record.professoruniversitarioutilizadorid.full_name)
    
    def render_acoes(self,record):
        if record.diaabertoid.id != Diaaberto.current().id:
            # Adicionar ação de duplicar atividade
            return format_html(f"""
            <div>
                <a onclick="alert.render('Tem a certeza que pretende duplicar esta atividade?','{reverse('atividades:duplicarAtividade', kwargs={'id': record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-content-duplicate mdi-24px" style="color: #007bff"></i>
                    </span>
                </a>
            </div>    
            """)
        else:
            return format_html(f"""
            <div></div
            """)

class ProfAtividadesTable(tables.Table):
    
    acoes = tables.Column('Operações', empty_values=())
    datasubmissao = tables.Column('Data de Submissão')
    coordenador = tables.Column('Coordenador Responsavel', empty_values=())
    class Meta:
        model = Atividade
        sequence = ('nome','tipo','datasubmissao','coordenador','estado', 'acoes')
        
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('nrcolaboradoresnecessario')
        self.columns.hide('publicoalvo')
        self.columns.hide('professoruniversitarioutilizadorid')
        self.columns.hide('dataalteracao')
        self.columns.hide('duracaoesperada')
        self.columns.hide('participantesmaximo')
        self.columns.hide('espacoid')
        self.columns.hide('tema')
        self.columns.hide('diaabertoid')

    def render_estado(self,record):
        fancy_box = ""
        if record.estado == 'Aceite':
            fancy_box = f"""
            <span class="tag text is-success" style="width: 7rem;font-size: small;">Aceite</span>
            """
        elif record.estado == 'Pendente':
            fancy_box = f"""
            <span class="tag text is-warning" style="width: 7rem;font-size: small;">Pendente</span>
            """
        else:
            fancy_box = f"""
            <span class="tag text is-danger" style="width: 7rem;font-size: small;">Recusada</span>
            """          
        return format_html(fancy_box)


    def render_coordenador(self,record):
        if record.get_coord() is not None:
            return format_html(record.get_coord().full_name)



    def render_acoes(self,record):
        sessoes= Sessao.objects.filter(atividadeid=record)
        for sessao in sessoes:
            if sessao.vagas != record.participantesmaximo:
                return format_html(f"""
                <div></div>
                 """)
        actions_html = f"""
        <div>
            <a id='edit' href="{reverse('atividades:alterarAtividade', kwargs={'id':record.pk})}" data-tooltip="Editar">
                <span class="icon is-small">
                    <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                </span>
            </a>
            &nbsp;
            <a onclick="alert.render('Tem a certeza que pretende eliminar esta Atividade?','{reverse('atividades:eliminarAtividade', kwargs={'id':record.pk})}')" data-tooltip="Eliminar">
                <span class="icon is-small">
                    <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                </span>
            </a> 
        """
        if record.diaabertoid.id != Diaaberto.current().id:
            # Adicionar ação de duplicar atividade
            actions_html += f"""
                &nbsp;
                <a onclick="alert.render('Tem a certeza que pretende duplicar esta atividade?','{reverse('atividades:duplicarAtividade', kwargs={'id': record.pk})}')" data-tooltip="Duplicar">
                    <span class="icon is-small">
                        <i class="mdi mdi-content-duplicate mdi-24px" style="color: #007bff"></i>
                    </span>
                </a>
            """

        actions_html += "</div>"
        return format_html(actions_html)



class AdminAtividadesTable(tables.Table):
    
    professoruniversitarioutilizadorid = tables.Column('Professor')
    datasubmissao = tables.Column('Data de Submissão')
    class Meta:
        model = Atividade
        sequence = ('nome','professoruniversitarioutilizadorid','tipo','datasubmissao','estado')
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('nrcolaboradoresnecessario')
        self.columns.hide('publicoalvo')
        self.columns.hide('dataalteracao')
        self.columns.hide('duracaoesperada')
        self.columns.hide('participantesmaximo')
        self.columns.hide('espacoid')
        self.columns.hide('tema')
        self.columns.hide('diaabertoid')

    def render_estado(self,record):
        fancy_box = ""
        if record.estado == 'Aceite':
            fancy_box = f"""
            <span class="tag text is-success" style="width: 7rem;font-size: small;">Aceite</span>
            """
        elif record.estado == 'Pendente':
            fancy_box = f"""
            <span class="tag text is-warning" style="width: 7rem;font-size: small;">Pendente</span>
            """
        else:
            fancy_box = f"""
            <span class="tag text is-danger" style="width: 7rem;font-size: small;">Recusada</span>
            """          
        return format_html(fancy_box)


    def render_professoruniversitarioutilizadorid(self,record):
        return str(record.professoruniversitarioutilizadorid.full_name)
    

class RoteiroTable(tables.Table):
    acoes = tables.Column('Operações', empty_values=(), orderable=False)
    coord = tables.Column(verbose_name='Coordenador')
    created_at = tables.Column(verbose_name='Data de criação')
    numero_de_atividades = tables.Column('Nº de atividades')
    # Adicione as colunas adicionais conforme necessário para o seu modelo Roteiro

    class Meta:
        model = Roteiro
        # Defina a ordem das colunas como desejar
        sequence = ('nome', 'ano', 'coord', 'created_at' , 'numero_de_atividades', 'acoes')

    def before_render(self, request):
        # Esconda colunas que não deseja exibir na tabela
        self.columns.hide('id')
        self.columns.hide('descricao')
        self.columns.hide('diaabertoid')
        self.columns.hide('updated_at')

    def render_acoes(self, record):
        actions_html = f"""
            <div style="margin-left: 1.8rem">
                <a id='novo' href="{reverse('atividades:verDetalheRoteiro', kwargs={'id': record.pk})}" data-tooltip="Ver mais detalhes">
                    <span class="icon is-small">
                        <i class="mdi mdi-plus mdi-24px"></i>
                    </span>
                </a>
                &nbsp
                <a id='edit' href="{reverse('atividades:alterarRoteiro', kwargs={'id':record.pk})}" data-tooltip="Editar">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
        """
        
        # Caso o horário de propostas de atividades tenha passado já nao pode eliminar o roteiro 
        if record.diaabertoid.dataporpostaatividadesfim > datetime.now(timezone.utc): 
            actions_html +=f"""
                &nbsp;            
                <a onclick="alert.render('Tem a certeza que pretende eliminar este roteiro?','{reverse('atividades:eliminarRoteiro', kwargs={'id': record.id})}')" data-tooltip="Eliminar">               
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a> 
            """

        # Verifica se o diaabertoid do roteiro é diferente do dia aberto atual
        if record.diaabertoid.id != Diaaberto.current().id:
            actions_html += f"""
                &nbsp;
                <a onclick="alert.render('Tem a certeza que pretende duplicar este roteiro?','{reverse('atividades:duplicarRoteiro', kwargs={'id': record.id})}')" data-tooltip="Duplicar">
                    <span class="icon is-small">
                        <i class="mdi mdi-content-duplicate mdi-24px" style="color: #007bff"></i>
                    </span>
                </a>
            """

        actions_html += "</div>"
        return format_html(actions_html)


    # Defina métodos de renderização adicionais conforme necessário para outras colunas    