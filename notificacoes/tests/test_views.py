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


class NotificacaoTestEnviarMensagens(TestCase):
    ''' Testes unitarios para a componente notificacoes - Testes enviar mensagens '''
    def setUp(self):
        self.user_recipient = Utilizador(username="andreeee1", password="andre123456", email="test_notificacoes@test_notificacoes.pt",contacto="+351967321393",valido="True")
        self.user_emissor = Utilizador(username="andreeeeeeee1", password="andre123456", email="test_notificacoes@test_notificacoes.pt",contacto="+351967321393",valido="True")
        self.user_recipient.save()
        self.user_emissor.save()



    def test_criar_mensagem(self):

        info = InformacaoMensagem(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
                              descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
        info.save()
        self.assertEqual("teste", info.descricao)




class NotificacaoTestInformacaoNotificacao(TestCase):
    ''' Testes unitarios para a componente notificacoes - Testes à tabela InformacaoNotificacao para notificações que demorem mais de 5 dias a ser recebidas.
    Este tipo de notificações são recebidas apenas se ainda fizer sentido o seu envio '''
    def setUp(self):
        self.user_recipient = Utilizador(username="andreeee", password="andre123456", email="test_notificacoes@test_notificacoes.pt",contacto="+351967321393",valido="True")
        self.user_emissor = Utilizador(username="andreeeeeeee", password="andre123456", email="test_notificacoes@test_notificacoes.pt",contacto="+351967321393",valido="True")
        self.user_recipient.save()
        self.user_emissor.save()



    def test_criar_notificacao_informacao_temporaria(self):

        info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
                              descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
        info.save()
        self.assertEqual("teste", info.descricao)


    def test_nao_enviar_notificacao_informacao_temporaria(self):

        info = InformacaoNotificacao(data=timezone.now() + timedelta(days=5), pendente=True, titulo = "teste",
                              descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
        info.save()
        self.assertEqual(False, timezone.now() >= info.data)
        

    def test_enviar_notificacao_informacao_temporaria(self):

        info = InformacaoNotificacao(data=timezone.now() , pendente=True, titulo = "teste",
                              descricao = "teste", emissor = self.user_emissor , recetor = self.user_recipient, tipo = "register" , lido = False)
        info.save()
        self.assertEqual(True, timezone.now() >= info.data)
            

class NotificacaoTestGrupos(TestCase):
    ''' Testes unitarios para a componente notificacoes - Grupos e listas de utilizadores '''
    def setUp(self):
        self.nr_mensagem = 10
        self.other_user = User.objects.create(username="andre1", password="andre123456", email="test_notificacoes@test_notificacoes.pt")
        self.emissor = User.objects.create(username="andre2", password="andre123456", email="test_notificacoes@test_notificacoes.pt")
        self.recetor = User.objects.create(username="andre3", password="andre123456", email="test_notificacoes@test_notificacoes.pt")
        self.to_group = Group.objects.create(name="grupo_teste")
        self.recetor_list = User.objects.all()
        self.to_group.user_set.add(self.recetor)
        self.to_group.user_set.add(self.other_user)

        for _ in range(self.nr_mensagem):
            notify.send(self.emissor, recipient=self.recetor, verb='mensagem', action_object=self.emissor)
        # Enviar notificacao a grupo
        notify.send(self.emissor, recipient=self.to_group, verb='mensagem', action_object=self.emissor)
        self.nr_mensagem += self.to_group.user_set.count()
        # Enviar notificacao a lista
        notify.send(self.emissor, recipient=self.recetor_list, verb='mensagem', action_object=self.emissor)
        self.nr_mensagem += len(self.recetor_list)



    def test_notificar_enviar(self):
        results = notify.send(self.emissor, recipient=self.recetor, verb='mensagem', action_object=self.emissor)
        for result in results:
            if result[0] is notify_handler:
                self.assertEqual(len(result[1]), 1)
                self.assertEqual(type(result[1][0]), Notificacao)




    def test_notificar_enviar_grupo(self):  
        results = notify.send(self.emissor, recipient=self.to_group, verb='mensagem', action_object=self.emissor)
        for result in results:
            if result[0] is notify_handler:
                self.assertEqual(len(result[1]), self.to_group.user_set.count())
                for notification in result[1]:
                    self.assertEqual(type(notification), Notificacao)



    def test_unread(self):
        self.assertEqual(Notificacao.objects.unread().count(), self.nr_mensagem)
        notification = Notificacao.objects.filter(recipient=self.recetor).first()
        notification.mark_as_read()
        self.assertEqual(Notificacao.objects.unread().count(), self.nr_mensagem-1)
        for notification in Notificacao.objects.unread():
            self.assertTrue(notification.unread)




    def test_read(self):
        self.assertEqual(Notificacao.objects.unread().count(), self.nr_mensagem)
        notification = Notificacao.objects.filter(recipient=self.recetor).first()
        notification.mark_as_read()
        self.assertEqual(Notificacao.objects.read().count(), 1)
        for notification in Notificacao.objects.read():
            self.assertFalse(notification.unread)




    def test_marcar_como_lido(self):
        self.assertEqual(Notificacao.objects.unread().count(), self.nr_mensagem)
        Notificacao.objects.filter(recipient=self.recetor).mark_all_as_read()
        self.assertEqual(self.recetor.notifications.unread().count(), 0)




    @override_settings(DJANGO_NOTIFICATIONS_CONFIG={
        'SOFT_DELETE': True
    })  
    def test_marcar_como_lido_com_soft_delete(self):
        to_delete = Notificacao.objects.filter(recipient=self.recetor).order_by('id')[0]
        to_delete.deleted = True
        to_delete.save()
        self.assertTrue(Notificacao.objects.filter(recipient=self.recetor).order_by('id')[0].unread)
        Notificacao.objects.filter(recipient=self.recetor).mark_all_as_read()
        self.assertFalse(Notificacao.objects.filter(recipient=self.recetor).order_by('id')[0].unread)




    def test_marcar_como_nao_lido(self):
        self.assertEqual(Notificacao.objects.unread().count(), self.nr_mensagem)
        Notificacao.objects.filter(recipient=self.recetor).mark_all_as_read()
        self.assertEqual(self.recetor.notifications.unread().count(), 0)
        Notificacao.objects.filter(recipient=self.recetor).mark_all_as_unread()
        self.assertEqual(Notificacao.objects.unread().count(), self.nr_mensagem)




    def test_marcar_tudo_como_apagado_soft_delete(self):  
        self.assertRaises(ImproperlyConfigured, Notificacao.objects.active)
        self.assertRaises(ImproperlyConfigured, Notificacao.objects.active)
        self.assertRaises(ImproperlyConfigured, Notificacao.objects.mark_all_as_deleted)
        self.assertRaises(ImproperlyConfigured, Notificacao.objects.mark_all_as_active)




    @override_settings(DJANGO_NOTIFICATIONS_CONFIG={
        'SOFT_DELETE': True
    })
    def test_marcar_tudo_como_apagado(self):
        notification = Notificacao.objects.filter(recipient=self.recetor).first()
        notification.mark_as_read()
        self.assertEqual(Notificacao.objects.read().count(), 1)
        self.assertEqual(Notificacao.objects.unread().count(), self.nr_mensagem-1)
        self.assertEqual(Notificacao.objects.active().count(), self.nr_mensagem)
        self.assertEqual(Notificacao.objects.deleted().count(), 0)

        Notificacao.objects.mark_all_as_deleted()
        self.assertEqual(Notificacao.objects.read().count(), 0)
        self.assertEqual(Notificacao.objects.unread().count(), 0)
        self.assertEqual(Notificacao.objects.active().count(), 0)
        self.assertEqual(Notificacao.objects.deleted().count(), self.nr_mensagem)

        Notificacao.objects.mark_all_as_active()
        self.assertEqual(Notificacao.objects.read().count(), 1)
        self.assertEqual(Notificacao.objects.unread().count(), self.nr_mensagem-1)
        self.assertEqual(Notificacao.objects.active().count(), self.nr_mensagem)
        self.assertEqual(Notificacao.objects.deleted().count(), 0)




class NotificacaoTestTimezone(TestCase):


    ''' Testes unitarios para a componente notificacoes - Timezone '''
    @override_settings(USE_TZ=True)
    @override_settings(TIME_ZONE='Europe/Lisbon')
    def test_timezone(self):
        emissor = User.objects.create(username="andre", password="andre123456", email="test_notificacoes@test_notificacoes.pt")
        recetor = User.objects.create(username="recetor", password="andre123456", email="test_notificacoes@test_notificacoes.pt")
        notify.send(emissor, recipient=recetor, verb='mensagem', action_object=emissor)
        notification = Notificacao.objects.get(recipient=recetor)
        delta = (
            timezone.now().replace(tzinfo=utc) - localtime(notification.timestamp, pytz.timezone(settings.TIME_ZONE))
        )
        self.assertTrue(delta.seconds < 60)




    @override_settings(USE_TZ=False)
    @override_settings(TIME_ZONE='Europe/Lisbon')
    def test_disable_timezone(self):
        emissor = User.objects.create(username="andre2", password="andre123456", email="test_notificacoes@test_notificacoes.pt")
        recetor = User.objects.create(username="recetor2", password="andre123456", email="test_notificacoes@test_notificacoes.pt")
        notify.send(emissor, recipient=recetor, verb='mensagem', action_object=emissor)
        notification = Notificacao.objects.get(recipient=recetor)
        delta = timezone.now() - notification.timestamp
        self.assertTrue(delta.seconds < 60)




