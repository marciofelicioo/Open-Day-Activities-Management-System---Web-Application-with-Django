import django_tables2 as tables
from configuracao.models import *
from django.utils.html import format_html
from django.db.models import Count
from atividades.models import Tema
from questionario.models import TemaQuestionario

class CursoTable(tables.Table):

    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    unidadeorganicaid = tables.Column('Faculdade')
    class Meta:
        model = Curso


    def before_render(self, request):
        self.columns.hide('id')
    
    def render_acoes(self,record):
        return format_html(f"""
            <div> 
                <a id='edit' href="{reverse('configuracao:editarCurso', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                &nbsp;                
                <a onclick="alert.render('Tem a certeza que pretende eliminar este curso?','{reverse('configuracao:eliminarCurso', kwargs={'id':record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a> 
            </div> 
        """)

class TemaTable(tables.Table):

    activity_count = tables.Column('Atividades com o Tema', accessor='num_activities')
    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    class Meta:
        model = Tema


    def before_render(self, request):
        self.columns.hide('id')
    
    def order_activity_count(self, queryset, is_descending):
        queryset = queryset.annotate(count=Count('atividade')
        ).order_by(("" if is_descending else "-") + "count")
        return (queryset, True)

    def render_acoes(self,record):
        return format_html(f"""
            <div>
                <a id='edit' href="{reverse('configuracao:editarTema', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                &nbsp;              
                <a onclick="alert.render('Tem a certeza que pretende eliminar este tema?','{reverse('configuracao:eliminarTema', kwargs={'id':record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a> 
            </div> 
        """)

class DepartamentoTable(tables.Table):
    unidadeorganicaid = tables.Column('Unidade Organica')
    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    class Meta:
        model = Departamento

    def before_render(self, request):
        self.columns.hide('id')

    def render_acoes(self,record):
        print(record)
        return format_html(f"""
            <div>
                <a id='edit' href="{reverse('configuracao:editarDepartamento', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                &nbsp;            
                <a onclick="alert.render('Tem a certeza que pretende eliminar este Departamento? <strong>Isto ira eliminar todos os curso e atividades contidas!</strong>','{reverse('configuracao:eliminarDepartamento', kwargs={'id':record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a>
            </div> 
        """)

class EdificioTable(tables.Table):

    numsalas = tables.Column('Numero de salas', accessor='count_salas')
    acoes = tables.Column('Operações', empty_values=(),orderable=False)

    class Meta:
        model = Edificio

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('image')

    def render_nome(self,record):
        return format_html(str(Edificio.objects.get(id=record.pk)))

    def render_acoes(self,record):
        return format_html(f"""
            <div >
                <a id='edit' href="{reverse('configuracao:editarEdificio', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                &nbsp;             
                <a onclick="alert.render('Tem a certeza que pretende eliminar este Edificio? <strong>Isto ira eliminar todos os espaços e atividades contidas!</strong>','{reverse('configuracao:eliminarEdificio', kwargs={'id':record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a> 
            </div> 
        """)


class UOTable(tables.Table):

    campusid = tables.Column('Campus')
    acoes = tables.Column('Operações', empty_values=(),orderable=False)

    class Meta:
        model = Unidadeorganica

    def before_render(self, request):
        self.columns.hide('id')


    def render_acoes(self,record):
        return format_html(f"""
            <div> 
                <a id='edit' href="{reverse('configuracao:editarUO', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                &nbsp;                
                <a onclick="alert.render('Tem a certeza que pretende eliminar esta Unidade Organica? <strong>Isto ira eliminar todos os departamentos e cursos da respetiva!</strong>','{reverse('configuracao:eliminarUO', kwargs={'id':record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a> 
            </div> 
        """)

class MenuTable(tables.Table):

    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    
    class Meta:
        model = Menu

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('horarioid')
        self.columns.hide('diaaberto')

    def render_acoes(self,record):
        return format_html(f"""
            <div >
                <a id='edit' href="{reverse('configuracao:editarMenu', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                &nbsp;            
                <a onclick="alert.render('Tem a certeza que pretende eliminar este Menu?','{reverse('configuracao:eliminarMenu', kwargs={'id':record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a> 
            </div> 
        """)

class TransporteTable(tables.Table):
    
    identifier = tables.Column('ID',accessor='get_identifier')
    rota = tables.Column('Rota', accessor='trip')
    horario = tables.Column('Horário',accessor='get_trip_time')
    capacidade = tables.Column('Cap.', accessor='get_capacidade')
    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    dia = tables.Column('Dia', accessor='transporte__dia')
    class Meta:
        model = Transportehorario
        sequence = ('identifier','rota','dia','horario','capacidade','acoes')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('horaPartida')
        self.columns.hide('horaChegada')
        self.columns.hide('transporte')
        self.columns.hide('origem')
        self.columns.hide('chegada')

    def render_acoes(self,record):
        opers1 = f"""
            <div style='margin-left: 1.8rem'>  
                <a id='edit' href="{reverse('configuracao:editarTransporte', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                &nbsp;          
                <a onclick="alert.render('Tem a certeza que pretende eliminar este transporte?','{reverse('configuracao:eliminarTransporte', kwargs={'id':record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a> 
            </div> 
        """
        opers2 = f"""
            <div>
                <a id="assign" href="{reverse('configuracao:atribuirTransporte', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-bus-school mdi-24px"></i>
                    </span>
                </a>
                &nbsp;
                <a id='edit' href="{reverse('configuracao:editarTransporte', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                &nbsp;          
                <a onclick="alert.render('Tem a certeza que pretende eliminar este transporte?','{reverse('configuracao:eliminarTransporte', kwargs={'id':record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a> 
            </div> 
        """
        if 'Penha' in str(record.trip) and 'Gambelas' in str(record.trip):
            return format_html(opers1)
        else: return format_html(opers2)

class DiaAbertoTable(tables.Table):

    acoes = tables.Column('Operações', empty_values=(),orderable=False)
    datadiaabertoinicio = tables.Column('Inicio')
    datadiaabertofim = tables.Column('Fim')
    class Meta:
        model = Diaaberto

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('precoalunos')
        self.columns.hide('precoprofessores')
        self.columns.hide('enderecopaginaweb')
        self.columns.hide('descricao')
        self.columns.hide('emaildiaaberto')
        self.columns.hide('datainscricaoatividadesinicio')
        self.columns.hide('datainscricaoatividadesfim')
        self.columns.hide('datapropostasatividadesincio')
        self.columns.hide('dataporpostaatividadesfim')
        self.columns.hide('administradorutilizadorid')
        self.columns.hide('escalasessoes')

    def render_acoes(self,record):
        return format_html(f"""
            <div>
                <a id='edit' href="{reverse('configuracao:editarDia', kwargs={'id':record.pk})}">
                    <span class="icon is-small">
                        <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                    </span>
                </a>
                &nbsp;          
                <a onclick="alert.render('Tem a certeza que pretende eliminar este Dia? <strong>Isto vai eliminar tudo o que depende do dia aberto como as Atividades e as Inscrições</strong>','{reverse('configuracao:eliminarDia', kwargs={'id':record.pk})}')">
                    <span class="icon is-small">
                        <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                    </span>
                </a> 
            </div> 
        """)
    
class TemaQuestionarioTable(tables.Table):

    activity_count = tables.Column('Perguntas relacionadas com o tema', accessor='num_questionarios')  
    acoes = tables.Column('Operações', empty_values=(),orderable=False)

    class Meta:
        model = TemaQuestionario

    def before_render(self, request):
        self.columns.hide('id')
    
    def order_activity_count(self, queryset, is_descending):
        queryset = queryset.annotate(count=Count('tema')
        ).order_by(("" if is_descending else "-") + "count")
        return (queryset, True)

    def render_acoes(self, record):
        if record.num_questionarios > 0:
            return format_html(f"""
                <div>
                    <a id='edit' href="{reverse('configuracao:editarTema', kwargs={'id':record.pk})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                </div> 
            """)
        else:
            return format_html(f"""
                <div>
                    <a id='edit' href="{reverse('configuracao:editarTema', kwargs={'id':record.pk})}">
                        <span class="icon is-small">
                            <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                        </span>
                    </a>
                    &nbsp;              
                    <a onclick="alert.render('Tem a certeza que pretende eliminar este tema?','{reverse('configuracao:eliminarTemaQuestionario', kwargs={'id':record.pk})}')">
                        <span class="icon is-small">
                            <i class="mdi mdi-trash-can-outline mdi-24px" style="color: #ff0000"></i>
                        </span>
                    </a> 
                </div> 
            """)
