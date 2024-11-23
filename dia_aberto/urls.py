"""dia_aberto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from utilizadores.forms import EmailValidationOnForgotPassword
from utilizadores import views
import notifications.urls
from django.conf.urls import handler404,handler500,handler403,handler400
from django.conf import settings # new
from django.conf.urls.static import static # new


handler404 = 'dia_aberto.views.error404'
handler403 = 'dia_aberto.views.error403'
handler400 = 'dia_aberto.views.error400'
handler500 = 'dia_aberto.views.error500'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('atividades/', include('atividades.urls')),
    path('inscricoes/', include('inscricoes.urls')),
    path('utilizadores/', include('utilizadores.urls')),
    path('notificacoes/', include('notificacoes.urls')),
    path('colaboradores/', include('colaboradores.urls')),
    path('configuracao/', include('configuracao.urls')),
    path('coordenadores/', include('coordenadores.urls')),
    path('questionario/', include('questionario.urls')),

    path('', views.home, name='home'),

    path('utilizadores/password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('utilizadores/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('utilizadores/password_reset/', auth_views.PasswordResetView.as_view(
        form_class=EmailValidationOnForgotPassword), name='password_reset'),
    path('utilizadores/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('', include("notifications.urls", namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)