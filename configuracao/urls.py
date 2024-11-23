from django.contrib import admin
from django.urls import path
from . import views

app_name = 'configuracao'

urlpatterns = [

    #-diaAberto
    path('diasabertos', views.viewDays.as_view(), name='diasAbertos'),
    path('editardia/<int:id>', views.newDay, name='editarDia'),
    path('inserirdiaaberto', views.newDay,name='novoDia' ),
    path('deldia/<int:id>', views.delDay, name='eliminarDia'),
    #path('daysjson', views.view_days_as_json, name='daysjson'),

    #-almoco
    path('menus',views.verMenus.as_view(), name='verMenus'),
    path('delmenu/<int:id>', views.delMenu, name='eliminarMenu'),
    path('editarmenu/<int:id>',views.newMenu, name='editarMenu'),
    path('novomenu', views.newMenu, name='novoMenu'),

    #-Transporte
    path('transportes', views.verTransportes.as_view(), name='verTransportes'),
    path('criartransporte', views.criarTransporte, name='criarTransporte'),
    path('editartransporte/<int:id>', views.criarTransporte, name='editarTransporte'),
    path('atribuirtransporte/<int:id>', views.atribuirTransporte, name='atribuirTransporte'),
    path('eliminaratribuicao/<int:id>', views.eliminarAtribuicao, name='eliminarAtribuicao'),
    path('eliminartransporte/<int:id>', views.eliminarTransporte, name='eliminarTransporte'),
    
    #-Utility
    path('imagens/edificio/<int:id>', views.verEdificioImagem, name='verEdificioImagem'),
    path('edificios', views.verEdificios.as_view(), name='verEdificios'),
    path('adicionaredificio', views.configurarEdificio, name='adicionarEdificio'),
    path('editaredificio/<int:id>', views.configurarEdificio, name='editarEdificio'),
    path('eliminaredificio/<int:id>', views.eliminarEdificio,name='eliminarEdificio'),

    path('uos', views.verUOs.as_view(), name='verUOs'),
    path('adicionaruo', views.configurarUO, name='adicionarUO'),
    path('editaruo/<int:id>', views.configurarUO, name='editarUO'),
    path('eliminaruo/<int:id>', views.eliminarUO,name='eliminarUO'),

    path('temas', views.verTemas.as_view(), name='verTemas'),
    path('temasQuestionario', views.verTemasQuestionario.as_view(), name='verTemasQuestionario'),
    path('adicionarTemasQuestionario', views.configurarTemasQuestionario, name='adicionarTemasQuestionario'),
    path('editarTema/<int:id>', views.configurarTema, name='editarTema'),
    path('eliminarTema/<int:id>', views.eliminarTema,name='eliminarTema'),
    path('adicionarTema', views.configurarTema, name='adicionarTema'),
    #path('editarTema/<int:id>', views.configurarTema, name='editarTema'),
    path('eliminarTemaqQuestionario/<int:id>', views.eliminarTemaQuestionario,name='eliminarTemaQuestionario'),

    path('departamentos', views.verDepartamentos.as_view(), name='verDepartamentos'),
    path('adicionarDepartamento', views.configurarDepartamento, name='adicionarDepartamento'),
    path('editarDepartamento/<int:id>', views.configurarDepartamento, name='editarDepartamento'),
    path('eliminarDepartamento/<int:id>', views.eliminarDepartamento,name='eliminarDepartamento'),

    path('cursos', views.verCursos.as_view(), name='verCursos'),
    path('adicionarCurso', views.configurarCurso, name='adicionarCurso'),
    path('editarCurso/<int:id>', views.configurarCurso, name='editarCurso'),
    path('eliminarCurso/<int:id>', views.eliminarCurso,name='eliminarCurso'),

    #ajax ----------
    path('ajax/getDias', views.getDias, name='getDias'),
    path('ajax/addHorarioRow', views.newHorarioRow, name='ajaxAddHorarioRow'),
    path('ajax/addPratoRow', views.newPratoRow, name='ajaxAddPratoRow'),
    path('ajax/addEspacoRow', views.newEspacoRow, name='ajaxAddEspacoRow'),
    path('ajax/addUORow', views.newUORow, name='ajaxAddUORow'),
    path('ajax/addDepartamentoRow', views.newDepartamentoRow, name='ajaxAddDepartamentoRow'),
    path('ajax/addCursoRow', views.newCursoRow, name='ajaxAddCursoRow'),

    #Relatórios
    path('relatoriosTransportes',views.relatoriosTransportes, name='relatoriosTransportes'),
    path('dias_disponiveis', views.dias_disponiveis,name='dias_disponiveis'),
    path('relatoriosTransportesPDF',views.relatoriosTransportesPDF, name='relatoriosTransportesPDF'),
    path('relatoriosTransportesCSV',views.relatoriosTransportesCSV, name='relatoriosTransportesCSV'),
]
