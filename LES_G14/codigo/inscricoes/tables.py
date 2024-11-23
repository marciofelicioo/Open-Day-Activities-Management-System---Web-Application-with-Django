import django_tables2 as tables
from .models import Inscricao, Escola
from configuracao.models import Diaaberto, Departamento, Unidadeorganica, Campus
from atividades.models import Atividade
import itertools
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Max, Min, OuterRef, Subquery
from inscricoes.models import Inscricaosessao
from django.utils.safestring import mark_safe

class InscricoesTable(tables.Table):
    grupo = tables.Column('Grupo', accessor='id', attrs={"th": {"width": "65"}})
    horario = tables.Column(verbose_name='Horário')
    nalunos = tables.Column(verbose_name='Qtd', attrs={
                            "abbr": {"title": "Quantidade"}, "th": {"width": "48"}})
    acoes = tables.Column('Ações', empty_values=(),
                          orderable=False, attrs={"th": {"width": "85"}})
    turma = tables.Column(empty_values=())

    class Meta:
        model = Inscricao
        sequence = ('grupo', 'dia', 'horario', 'escola', 'areacientifica',
                    'turma', 'nalunos', 'acoes', 'presenca', 'nr_presentes')
        
        #exclude = ('presenca','nr_presentes',)
    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('ano')
        self.columns.hide('areacientifica')
        self.columns.hide('participante')
        self.columns.hide('diaaberto')
        self.columns.hide('meio_transporte')
        self.columns.hide('hora_chegada')
        self.columns.hide('local_chegada')
        self.columns.hide('entrecampi')
        self.columns.hide('individual')

    def order_horario(self, queryset, is_descending):
        queryset = queryset.annotate(inicio=Subquery(
            Inscricaosessao.objects.filter(inscricao=OuterRef('pk'))
            .values('inscricao')
            .annotate(inicio=Min('sessao__horarioid__inicio'))
            .values('inicio')
        )).order_by(("-" if is_descending else "") + "inicio")
        return (queryset, True)

    def render_turma(self, value, record):
        if not record.ano:
            return format_html("(Individual)")
        return format_html(f"{record.ano}º {value}, {record.areacientifica}")

    def render_acoes(self, record):
        links = []

        # Link para editar inscrição
        editar_link = format_html(
            '<a href="{}" data-tooltip="Editar"><span class="icon"><i class="mdi mdi-circle-edit-outline mdi-24px"></i></span></a>',
            reverse("inscricoes:consultar-inscricao", kwargs={"pk": record.pk})
        )
        links.append(editar_link)

        # Link para apagar inscrição
        apagar_link = format_html(
            '<a onclick="alert.render(\'Tem a certeza que pretende eliminar esta inscrição?\',\'{}\')" data-tooltip="Apagar"><span class="icon has-text-danger"><i class="mdi mdi-trash-can mdi-24px"></i></span></a>',
            reverse("inscricoes:apagar-inscricao", kwargs={"pk": record.pk})
        )
        links.append(apagar_link)
        
        # Verifica se o usuário é administrador
        if self.request.user.groups.filter(name='Administrador').exists():
            # Link para marcar presença, apenas se a presença ainda não estiver confirmada
            if not record.presenca:
                marcar_presenca_link = format_html(
                    '<a href="{}" data-tooltip="Registrar Presenças"><span class="icon has-text-success"><i class="mdi mdi-account-check mdi-24px"></i></span></a>',
                    reverse("inscricoes:marcarPresenca", kwargs={"pk": record.pk})
                )
                links.append(marcar_presenca_link)
            else:
                alterar_presenca_link = format_html(
                    '<a href="{}" data-tooltip="Alterar Presenças"><span class="icon has-text-dark"><i class="mdi mdi-pencil mdi-24px"></i></span></a>',
                    reverse("inscricoes:marcarPresenca", kwargs={"pk": record.pk})
                )
                links.append(alterar_presenca_link)

        # Combine todos os links em um div
        return format_html('<div style="display: flex; align-items: right; gap: 2px;">{}</div>', mark_safe(''.join(links)))