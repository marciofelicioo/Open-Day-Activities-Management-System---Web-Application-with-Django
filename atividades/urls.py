from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'atividades'

urlpatterns = [
    path('minhasatividades',views.AtividadesProfessor.as_view(),name="minhasAtividades"),
    path('atividadadesUOrganica',views.AtividadesCoordenador.as_view(),name="atividadesUOrganica"),
    path('alteraratividade/<int:id>',views.alterarAtividade,name='alterarAtividade'),
    path('sessao/<int:id>',views.inserirsessao,name='inserirSessao'),
    path('eliminaratividade/<int:id>',views.eliminarAtividade,name='eliminarAtividade'),
    path('eliminarsessao/<int:id>',views.eliminarSessao,name='eliminarSessao'),
    path('proporatividade',views.proporatividade,name='proporAtividade'),
    path('validaratividade/<int:id>/<int:action>',views.validaratividade,name='validarAtividade'),
    path('veredificios',views.veredificios,name="verEdificios"),
    path('versalas',views.versalas,name="verSalas"),
    path('verhorarios',views.verhorarios,name="verHorarios"),
    path('verresumo/<int:id>',views.verresumo,name='verResumo'),
    path('confirmar/<int:id>',views.confirmarResumo,name='confirmarResumo'),
    path('atividadesadmin',views.AtividadesAdmin.as_view(),name="atividadesAdmin"),
    path('verdeps',views.verdeps,name="verDepartamentos"),
    path('veruos',views.verfaculdades,name="verFaculdades"),
    path('consultarRoteiros',views.ConsultarRoteiros.as_view(),name="consultarRoteiros"),
    path('verDetalheRoteiro/<int:id>',views.verDetalheRoteiro, name='verDetalheRoteiro'),
    path('criarRoteiro', views.criar_roteiro, name='criarRoteiro'),
    path('adicionarAtividades/<int:id>', views.adicionar_atividades, name='adicionarAtividades'),
    path('eliminarAtividadeRoteiro/<int:id>',views.eliminarAtividadeRoteiro, name='eliminarAtividadeRoteiro'),
    path('eliminarSessaoRoteiro/<int:id>',views.eliminarSessaoRoteiro, name='eliminarSessaoRoteiro'),
    path('verresumoRoteiro/<int:id>',views.verresumo_roteiro, name='verResumoRoteiro'),
    path('eliminarRoteiro/<int:id>',views.eliminar_roteiro,name="eliminarRoteiro"),
    path('alterarRoteiro/<int:id>',views.alterarRoteiro, name='alterarRoteiro'),
    path('<int:id>/pdf',views.RoteiroPDF,name="roteiro-pdf"),
    path('duplicarAtiviade/<int:id>',views.duplicarAtividade,name='duplicarAtividade'),
    path('duplicarRoteiro/<int:id>',views.duplicarRoteiro, name="duplicarRoteiro"),
    path('relatoriosRoteiros',views.relatoriosRoteiros, name='relatoriosRoteiros'),
    path('dias_disponiveis', views.dias_disponiveis,name='dias_disponiveis'),
    path('relatorioRoteirosPDF',views.relatorioRoteirosPDF, name='relatorioRoteirosPDF'),
    path('relatorioRoteirosCSV', views.relatorioRoteirosCSV, name='relatorioRoteirosCSV'),
]

