from django.urls import path
from django.conf.urls import url
from coordenadores import views

app_name = 'coordenadores'

urlpatterns = [
    path('adicionartarefa/',views.adicionartarefa,name="adicionarTarefa"),
    path('alterartarefa/<int:id>',views.adicionartarefa,name="alterarTarefa"),
    path('consultartarefa/',views.ConsultarTarefas.as_view(),name="consultarTarefa"),
    path('ajax/adicionarsessoes/', views.sessoesAtividade, name='sessoesAtividade'),
    path('ajax/adicionardias/', views.diasAtividade, name='diasAtividade'),
    path('ajax/adicionarcolaboradores/', views.colaboradores, name='colaboradores'),
    path('ajax/tipotarefa/', views.tipoTarefa, name='tipoTarefa'),
    path('ajax/grupoinfo/', views.grupoInfo, name='grupoInfo'),
    path('ajax/diasgrupo/', views.diasGrupo, name='diasGrupo'),
    path('ajax/horariogrupo/', views.horarioGrupo, name='horarioGrupo'),
    path('ajax/origemgrupo/', views.locaisOrigem, name='locaisOrigem'),
    path('ajax/destinogrupo/', views.locaisDestino, name='locaisDestino'),
    path('eliminartarefa/<int:id>',views.eliminartarefa,name="eliminarTarefa"),
    path("atribuircolaborador/<int:id>",views.atribuirColaborador,name="atribuirColaborador"),
]
