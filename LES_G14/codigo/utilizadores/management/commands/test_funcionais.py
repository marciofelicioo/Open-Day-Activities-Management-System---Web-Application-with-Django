import logging

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from utilizadores.models import Administrador
from django.core.management import call_command
from dia_aberto.utils import init_driver


class Command(BaseCommand):
    help = 'Corre testes funcionais. Exemplo: manage.py test_funcionais tests_path firefox [--custom]'

    def add_arguments(self, parser):
        parser.add_argument('tests_path', type=str,
                            help='Especifica os sítios ou app dos testes')
        parser.add_argument('browser', type=str,
                            help='O browser no qual correr os testes')

        # Optional arguments
        parser.add_argument('-c', '--custom', action='store_true',
                            help='Utiliza o driver que estiver na PATH')
        parser.add_argument('-k', '--keepdb', action='store_true',
                            help='Manter a db')

    def handle(self, *args, **options):
        browser = options['browser']
        tests_path = options['tests_path']
        custom = options['custom']
        keepdb = options['keepdb']

        if custom:
            init_driver(browser, use_custom_driver=True)
        else:
            init_driver(browser)

        _args = []
        if keepdb:
            _args.append('--keepdb')

        if not '.' in tests_path:
            tests_path = f'{tests_path}.tests.funcionais'

        call_command(
            'test', tests_path, *_args)
