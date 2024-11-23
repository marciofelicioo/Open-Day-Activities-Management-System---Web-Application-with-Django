from inscricoes.tests.test_models import create_Inscricao_0, create_Responsavel_0
from django.test import TestCase
from inscricoes.utils import enviar_mail_confirmacao_inscricao, render_pdf
from django.core import mail
import threading

def test_concurrently(times):
    """
    Add this decorator to small pieces of code that you want to test
    concurrently to make sure they don't raise exceptions when run at the
    same time.  E.g., some Django views that do a SELECT and then a subsequent
    INSERT might fail when the INSERT assumes that the data has not changed
    since the SELECT.
    """
    def test_concurrently_decorator(test_func):
        def wrapper(*args, **kwargs):
            exceptions = []
            def call_test_func():
                try:
                    test_func(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    raise
            threads = []
            for i in range(times):
                threads.append(threading.Thread(target=call_test_func))
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            if exceptions:
                raise Exception('test_concurrently intercepted %s exceptions: %s' % (len(exceptions), exceptions))
        return wrapper
    return test_concurrently_decorator


class TestUtils(TestCase):
    """ Teste suite do módulo utils da app "inscricoes" """

    @classmethod
    def setUpTestData(cls):
        cls.inscricao = create_Inscricao_0()
        cls.responsavel = create_Responsavel_0()
        cls.responsavel.inscricao = cls.inscricao
        cls.responsavel.save()

    def test_render_pdf(self):
        """ Teste a função 'render_pdf' """
        context = {
            'inscricao': self.inscricao,
            'ano': self.inscricao.diaaberto.ano,
        }
        pdf = render_pdf('inscricoes/pdf.html', context, 'dummy.pdf')
        self.assertEquals(pdf.status_code, 200)

    def test_enviar_mail_confirmacao_inscricao(self):
        """ Teste a função 'enviar_mail_confirmacao_inscricao' """
        enviar_mail_confirmacao_inscricao(None, self.inscricao.pk)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f'Confirmação da Inscrição no Dia Aberto de {self.inscricao.diaaberto.ano} da Universidade do Algarve.')
