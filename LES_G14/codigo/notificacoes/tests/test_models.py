from django.test import TestCase
from utilizadores.models import *
from configuracao.models import *
from django.core.management import call_command
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from notificacoes.models import InformacaoMensagem, InformacaoNotificacao, MensagemEnviada, MensagemRecebida, Notificacao
from utilizadores.tests.test_models import create_Administrador_0, create_Colaborador_1, create_Coordenador_0, create_Coordenador_1, create_Participante_0, create_ProfessorUniversitario_0, create_Utilizador_0, create_Utilizador_1
from datetime import datetime
import pytz
from notifications.signals import notify


def create_InformacaoNotificacao_0():
    return InformacaoNotificacao.objects.get_or_create(
        data=datetime.now(pytz.UTC) + timedelta(days=5),
        pendente=True,
        titulo="teste",
        descricao="teste",
        emissor=create_Administrador_0(),
        recetor=create_Coordenador_0(),
        tipo="register",
        lido=False
    )[0]


def create_InformacaoNotificacao_1():
    return InformacaoNotificacao.objects.get_or_create(
        data=datetime.now(pytz.UTC) + timedelta(days=7),
        pendente=True,
        titulo="teste1",
        descricao="teste1",
        emissor=create_Administrador_0(),
        recetor=create_Coordenador_1(),
        tipo="register",
        lido=False
    )[0]


def create_InformacaoMensagem_0():
    return InformacaoMensagem.objects.get_or_create(
        data=datetime.now(pytz.UTC) + timedelta(days=5),
        pendente=True,
        titulo="teste2",
        descricao="teste2",
        emissor=create_Utilizador_0(),
        recetor=create_Utilizador_1(),
        tipo="register",
        lido=False
    )[0]


def create_InformacaoMensagem_1():
    return InformacaoMensagem.objects.get_or_create(
        data=datetime.now(pytz.UTC) + timedelta(days=5),
        pendente=True,
        titulo="teste3",
        descricao="teste3",
        emissor=create_Participante_0(),
        recetor=create_Coordenador_1(),
        tipo="register",
        lido=False
    )[0]


def create_MensagemRecebida_0():
    return MensagemRecebida.objects.get_or_create(
        mensagem=create_InformacaoMensagem_0()
    )[0]


def create_MensagemRecebida_1():
    return MensagemRecebida.objects.get_or_create(
        mensagem=create_InformacaoMensagem_1()
    )[0]


def create_MensagemEnviada_0():
    return MensagemEnviada.objects.get_or_create(
        mensagem=create_InformacaoMensagem_0()
    )[0]


def create_MensagemEnviada_1():
    return MensagemEnviada.objects.get_or_create(
        mensagem=create_InformacaoMensagem_1()
    )[0]


class TestNotificacoesModels(TestCase):
    ''' Testes para as notificacoes - funções dos modelos da componente notificacoes '''

    def test_Notificacao_model(self):
        """ Testes do modelo "Notificacao" """
        professor = create_ProfessorUniversitario_0()
        notify.send(create_Administrador_0(),
                    recipient=professor,
                    verb='O seu registo foi validado')
        assert professor.notifications.unread().count() == 1
        notify.send(create_Coordenador_0(),
                    recipient=professor,
                    verb='A sua atividade foi aceite')
        assert professor.notifications.unread().count() == 2

    def test_InformacaoNotificacao_model(self):
        """ Testes do modelo "InformacaoNotificacao" """
        notificacoes = [
            create_InformacaoNotificacao_0(),
            create_InformacaoNotificacao_1(),
        ]

    def test_InformacaoMensagem_model(self):
        """ Testes do modelo "InformacaoMensagem" """
        mensagens = [
            create_InformacaoMensagem_0(),
            create_InformacaoMensagem_1(),
        ]

    def test_MensagemRecebida_model(self):
        """ Testes do modelo "MensagemRecebida" """
        mensagens = [
            create_MensagemRecebida_0(),
            create_MensagemRecebida_1(),
        ]

    def test_MensagemEnviada_model(self):
        """ Testes do modelo "MensagemEnviada" """
        mensagens = [
            create_MensagemEnviada_0(),
            create_MensagemEnviada_1(),
        ]
