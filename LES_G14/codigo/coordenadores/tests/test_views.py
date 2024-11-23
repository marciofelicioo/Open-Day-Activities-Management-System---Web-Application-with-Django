from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import *
from configuracao.models import *
from utilizadores.models import *
from colaboradores.models import *
from coordenadores.models import *
from notificacoes.models import *
from inscricoes.models import *
from configuracao.tests.test_models import create_open_day
from utilizadores.tests.test_models import create_Administrador_0 
import json
import urllib

def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.parse.urlencode(kwargs) # for Python 3, use urllib.parse.urlencode instead
