from . import views
from django.urls import path
from django.urls import re_path as pattern


app_name = 'notificacoes'

urlpatterns = [


    path('detalhes/<int:id>', views.sem_notificacoes,
         name='sem-notificacoes'),
    path('detalhes/<int:id>/<int:nr>', views.categorias_notificacao_automatica,
         name='categorias-notificacao-automatica'),
    path('apagarnotificacao/<int:id>/<int:nr>', views.apagar_notificacao_automatica,
         name='apagar-notificacao-automatica'),

    path('limpar/<int:id>', views.limpar_notificacoes,
         name='limpar-notificacoes'),
    path('marcarcomolida', views.marcar_como_lida,
         name='ler-notificacoes'),
    #     path('notificar_teste/<str:sigla>/<int:id>', views.enviar_notificacao_automatica,
    #          name='notificar'),

    ################################ Mensagens ###########################

    path('escolhertipo', views.escolher_tipo, name="enviar-notificacao"),
    path('criarmensagem/<int:id>', views.criar_mensagem, name="escrever-mensagem"),
    path('criarmensagemuo/<int:id>',
         views.criar_mensagem_uo, name="criar-mensagem-uo"),
    path('criarmensagemadmin/<int:id>',
         views.criar_mensagem_admin, name="criar-mensagem-admin"),
    path('criarmensagemparticipante/<int:id>',
         views.criar_mensagem_participante, name="criar-mensagem-participante"),
    path('mensagens/<int:id>', views.sem_mensagens,
         name='sem-mensagens'),
    path('concluirenvio', views.concluir_envio,
         name='concluir-envio'),
    path('mensagens/<int:id>/<int:nr>', views.detalhes_mensagens,
         name='detalhes-mensagem'),
    path('apagarmensagem/<int:id>/<int:nr>', views.apagar_mensagem,
         name='apagar-mensagem'),
    path('limparmensganes/<int:id>', views.limpar_mensagens,
         name='limpar-mensagens'),
    path('marcarmensagemcomolida/<int:id>', views.mensagem_como_lida,
         name='ler-mensagens'),
]
