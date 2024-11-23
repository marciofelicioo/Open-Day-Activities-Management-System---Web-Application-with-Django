from django.urls import path, include
from .views import consultar_utilizadores
from .views import escolher_perfil
from .views import criar_utilizador
from .views import apagar_utilizador
from .views import alterar_utilizador
from .views import concluir_registo
from .views import home
from .views import login_action
from .views import logout_action
from .views import mensagem
from .views import alterar_password

from . import views

app_name = 'utilizadores'


urlpatterns = [
    path('consultarutilizadores', consultar_utilizadores.as_view(),name='consultar-utilizadores'),
    path('escolherperfil', escolher_perfil,name='escolher-perfil'),    
    path('criarutilizadores/<int:id>', criar_utilizador, name='criar-utilizador'),
    path('alterarpassword',alterar_password,name='alterar-password'),

    path('apagarproprioutilizador', views.apagar_proprio_utilizador,name='apagar-conta'),
    path('apagarutilizador/<int:id>', views.apagar_utilizador,name='apagar-utilizador'),
    path('alterarutilizadoradmin/<int:id>', views.alterar_utilizador_admin,name='alterar-utilizador-admin'),
    path('alterarutilizador', views.alterar_utilizador,name='alterar-utilizador'),
    path('validarutilizador/<int:id>', views.validar_utilizador,name='validar-utilizador'),
    path('rejeitarutilizador/<int:id>', views.rejeitar_utilizador,name='rejeitar-utilizador'),
    path('alteraridioma', views.alterar_idioma,name='alterar-idioma'),


    path('concluirregisto/<int:id>', concluir_registo,name='concluir-registo'),
    path('mensagem/<int:id>', mensagem,name='mensagem'),
    path('validar/<str:nome>/<int:id>', views.enviar_email_validar,name='validar'),
    path('rejeitar/<str:nome>/<int:id>', views.enviar_email_rejeitar,name='rejeitar'),
    path("logout", logout_action, name="logout"), 
    path("login", login_action, name="login"),   

    
    path('mudarperfilescolha/<int:id>', views.mudar_perfil_escolha_admin,name='mudar-perfil-escolha-admin'),    
    path('mudarperfil/<int:tipo>/<int:id>', views.mudar_perfil_admin, name='mudar-perfil-admin'),

    path('mudarmeuperfilescolha', views.mudar_perfil_escolha,name='mudar-perfil-escolha'),    
    path('mudarmeuperfil/<int:tipo>', views.mudar_perfil, name='mudar-perfil'),

    path('ajax/load-departamentos/', views.load_departamentos, name='ajax_load_departamentos'),
    path('ajax/load-cursos/', views.load_cursos, name='ajax_load_cursos'),

]       
