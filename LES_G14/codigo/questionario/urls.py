from . import views
from django.urls import path


app_name = 'questionario'

urlpatterns = [
    path('criar', views.criar_questionario, name='criar-questionario'),
    path('editar/<int:id>', views.editar_questionario, name='editar-questionario'),
    path('eliminar/<int:id>', views.eliminar_questionario, name='eliminar-questionario'),
    path('questionario/<int:id>/pdf', views.questionario_pdf, name='questionario-pdf'),
    path('listar', views.listar_questionarios, name='listar-questionario'),
    path('remover_pergunta/', views.remover_pergunta, name='remover_pergunta'),
    path('consultar-questionario/<int:id>',views.consultar_questionario,name='consultar_questionario'),
    path('arquivar-questionario/<int:questionario_id>', views.arquivar_questionario, name='arquivar_questionario'),
    path('validar-questionario/<int:questionario_id>', views.validar_questionario, name='validar_questionario'),
    path('publicar-questionario/<int:questionario_id>', views.publicar_questionario, name='publicar_questionario'),
    path('remover_publicacao/<int:questionario_id>', views.remover_publicacao, name='remover_publicacao'),
    path('remover_arquivo/<int:questionario_id>', views.remover_arquivo, name='remover_arquivo'),
    path('rejeitar_questionario/<int:questionario_id>', views.rejeitar_questionario, name='rejeitar_questionario'),
    path('remover_validacao/<int:questionario_id>', views.remover_validacao, name='remover_validacao'),
]
