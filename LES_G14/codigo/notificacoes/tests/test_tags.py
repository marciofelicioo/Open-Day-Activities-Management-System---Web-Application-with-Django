from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.template import Context, Template
from django.test import RequestFactory, TestCase
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from django.utils.timezone import localtime, utc
from notifications.base.models import notify_handler
from notifications.signals import notify
from notifications.utils import id2slug
from swapper import load_model
from django.test import override_settings 
from django.urls import reverse
import json
import pytz
from django.contrib.auth.models import Group, User
from notificacoes.models import *
from utilizadores.models import *
from datetime import datetime, timedelta
Notificacao = load_model('notificacoes', 'Notificacao')


class TagTeste(TestCase):
    ''' Testes unitarios para a componente notificacoes - Tags da componente notificações '''
    def setUp(self):
        self.nr_mensagem = 1
        self.emissor = User.objects.create_user(username="emissor", password="andre123456", email="teste@teste.pt")
        self.recetor = User.objects.create_user(username="recetor", password="andre123456", email="teste@teste.pt")
        self.recetor.is_staff = True
        self.recetor.save()
        for _ in range(self.nr_mensagem):
            notify.send(
                self.emissor,
                recipient=self.recetor,
                verb='mensagem',
                action_object=self.emissor,
                url="/",
                other_content="Testes"
            )

    def tag_test(self, template, context, output):
        t = Template('{% load notifications_tags %}'+template)
        c = Context(context)
        self.assertEqual(t.render(c), output)

    def test_has_notification(self):
        template = "{{ user|has_notification }}"
        context = {"user":self.recetor}
        output = u"True"
        self.tag_test(template, context, output)
