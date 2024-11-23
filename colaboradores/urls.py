from django.urls import path, include

from . import views

app_name = 'colaboradores'


urlpatterns = [
    path('consultartarefas', views.consultar_tarefas.as_view(),
         name='consultar-tarefas'),
    path('disponibilidade', views.minha_disponibilidade,
         name='minha-disponibilidade'),
    path('departamentos', views.ver_departamentos,
         name='ver-departamentos'),
    path('preferenciaatividade', views.preferencia_atividade,
         name="preferencia-atividade"),

    path('escolheratividades', views.AtividadesColaborador.as_view(),
         name="escolher-atividades"),
         
    path('atividadesescolhidas', views.AtividadesColaboradorSelecionadas.as_view(),
         name="atividades-escolhidas"),


    path('selecionaratividade/<int:id>', views.selecionar_atividade,
         name="selecionar-atividade"),

     path('retiraratividade/<int:id>', views.retirar_atividade,
         name="retirar-atividade"),

    path('concluirdisponibilidade', views.concluir_disponibilidade,
         name='concluir-disponibilidade'),
    path('concluirtarefa/<int:id>', views.concluir_tarefa, name='concluir-tarefa'),
    path('iniciartarefa/<int:id>', views.iniciar_tarefa, name='iniciar-tarefa'),
    path('cancelartarefa/<int:id>', views.cancelar_tarefa, name='cancelar-tarefa'),
    path('rejeitarcancelamentotarefa/<int:id_notificacao>',
         views.rejeitar_cancelamento_tarefa, name='rejeitar-cancelamento-tarefa'),
    path('validarcancelamentotarefa/<int:id_notificacao>',
         views.validar_cancelamento_tarefa, name='validar-cancelamento-tarefa'),

    path('ajax/addHorarioRow', views.newHorarioRow, name='ajaxAddHorarioRow'),
]
