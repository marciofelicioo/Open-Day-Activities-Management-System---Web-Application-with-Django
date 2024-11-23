import django_tables2 as django_tables
from utilizadores.models import Administrador, Utilizador
from django.utils.html import format_html
from django.urls import reverse


class UtilizadoresTable(django_tables.Table):

    nome = django_tables.Column(
        empty_values=(), order_by=("first_name", "last_name"))
    email = django_tables.Column(
        'Email')
    valido = django_tables.Column('Estado', attrs={"th": {"width": "130"}})
    tipo = django_tables.Column(accessor='firstProfile', orderable=False)
    acoes = django_tables.Column('Ações', empty_values=(),
                                 orderable=False, attrs={"th": {"width": "150"}})

    class Meta:
        model = Utilizador
        sequence = ('nome', 'email', 'contacto', 'tipo', 'valido', 'acoes')

    def before_render(self, request):
        self.columns.hide('id')
        self.columns.hide('password')
        self.columns.hide('last_login')
        self.columns.hide('is_superuser')
        self.columns.hide('username')
        self.columns.hide('first_name')
        self.columns.hide('last_name')
        self.columns.hide('is_staff')
        self.columns.hide('is_active')
        self.columns.hide('date_joined')
        self.columns.hide('user_ptr')

    def render_nome(self, record):
        return f"{record.first_name} {record.last_name}"

    def render_tipo(self, value):
        return "Professor Universitário" if value == "ProfessorUniversitario" else value

    def render_valido(self, value):
        if(value == 'True'):
            estado = "Confirmado"
            cor = "is-success"
        elif(value == 'False'):
            estado = "Por confirmar"
            cor = "is-warning"
        elif(value == 'Rejeitado'):
            estado = "Rejeitado"
            cor = "is-danger"
        return format_html(f"""
        <span class="tag {cor}" style="font-size: small; min-width: 110px;">
        {estado}
        </span>
        """)

    def render_acoes(self, record):
        primeiro_botao = """<span class="icon"></span>"""
        if self.request.user != record.user_ptr and not (record.firstProfile == 'Administrador' and not self.request.user.groups.filter(name='Administrador').exists()):
            if record.valido == "Rejeitado":
                primeiro_botao = f"""
                <a data-tooltip="Validar" href="{reverse('utilizadores:validar', args=[record.first_name, record.id])}">
                    <span class="icon">
                        <i class="fas fa-check" style="color: #32CD32"></i>
                    </span>
                </a>
                """
            elif record.valido == "True":
                primeiro_botao = f"""
                <a data-tooltip="Rejeitar" onclick="alert.render('Tem a certeza que pretende rejeitar este utilizador?','{reverse('utilizadores:rejeitar', args=[record.first_name, record.id])}')">
                    <span class="icon has-text-danger">
                        <i class="fas fa-ban"></i>
                    </span>
                </a>
                """
            else:
                primeiro_botao = f"""
                <a data-tooltip="Validar" href="{reverse('utilizadores:validar', args=[record.first_name, record.id])}">
                    <span class="icon">
                        <i class="fas fa-check" style="color: #32CD32"></i>
                    </span>
                </a>
                <a data-tooltip="Rejeitar" onclick="alert.render('Tem a certeza que pretende rejeitar este utilizador?','{reverse('utilizadores:rejeitar', args=[record.first_name, record.id])}')">
                    <span class="icon has-text-danger">
                        <i class="fas fa-ban"></i>
                    </span>
                </a>
                """
        segundo_botao = ""
        if self.request.user.groups.filter(name='Administrador').exists():
            segundo_botao = f"""
            <a href='{reverse('utilizadores:alterar-utilizador-admin', args=[record.id])}'
                data-tooltip="Editar">
                <span class="icon">
                    <i class="mdi mdi-circle-edit-outline mdi-24px"></i>
                </span>
            </a>
            """
        terceiro_botao = ""
        if record.firstProfile == 'Participante':
            alerta = "Tem a certeza que pretende eliminar este utilizador?<br><br><b>Atenção!</b><br><br>A <b>incrição</b> deste participante será apagada permanentemente."
        elif record.firstProfile == 'Colaborador':
            alerta = "Tem a certeza que pretende eliminar este utilizador?<br><br><b>Atenção!</b><br><br>As suas <b>tarefas</b> deixarão de estar atribuídas."
        elif record.firstProfile == 'ProfessorUniversitario':
            alerta = "Tem a certeza que pretende eliminar este utilizador?<br><br><b>Atenção!</b><br><br>As <b>atividades</b> pelo qual este professor está responsável serão apagadas permanentemente."
        elif record.firstProfile == 'Coordenador':
            alerta = "Tem a certeza que pretende eliminar este utilizador?<br><br><b>Atenção!</b><br><br> As <b>atividades dos departamentos</b> pelo qual este coordenador está responsável serão apagadas permanentemente.<br><br>As <b>tarefas dos colaboradores</b> pelo qual este coordenador está responsável serão apagadas permanentemente."
        elif record.firstProfile == 'Administrador':
            if not self.request.user.groups.filter(name='Administrador').exists():
                terceiro_botao = " "
            elif record.valido != "True" or Administrador.objects.filter(valido="True").count() > 1:
                alerta = "Tem a certeza que pretende eliminar este utilizador?<br><br><b>Atenção!</b><br><br>Todas as informações relativas aos dias abertos pelo qual este administrador está responsável serão apagadas permanentemente!"
            elif self.request.user != record.user_ptr:
                terceiro_botao = """
                <a onclick="alert.warning('Não pode apagar este administrador porque é o unico que existe.')"
                    data-tooltip="Apagar">
                    <span class="icon has-text-danger">
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </span>
                </a>
                """
        if self.request.user != record.user_ptr and terceiro_botao == "":
            terceiro_botao = f"""
                <a onclick="alert.render('{alerta}','{reverse('utilizadores:apagar-utilizador', args=[record.id])}')"
                    data-tooltip="Apagar">
                    <span class="icon has-text-danger">
                        <i class="mdi mdi-trash-can mdi-24px"></i>
                    </span>
                </a>
            """
        return format_html(f"""
        <div>
            {primeiro_botao}
            {segundo_botao}
            {terceiro_botao}
        </div>
        """)
