:: Componente Utilizadores

python manage.py test utilizadores.tests.funcionais.test_login_ok
python manage.py test utilizadores.tests.funcionais.test_login_nao_existe
python manage.py test utilizadores.tests.funcionais.test_login_pass_errada
python manage.py test utilizadores.tests.funcionais.test_logout
python manage.py test utilizadores.tests.funcionais.test_alterar_pass_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_pass_erro
python manage.py test utilizadores.tests.funcionais.test_criar_utilizador_ok
python manage.py test utilizadores.tests.funcionais.test_criar_utilizador_erro
python manage.py test utilizadores.tests.funcionais.test_alterar_utilizador_ok
python manage.py test utilizadores.tests.funcionais.test_alterar_utilizador_erro
python manage.py test utilizadores.tests.funcionais.test_consultar_utilizadores
python manage.py test utilizadores.tests.funcionais.test_rejeitar_utilizador
python manage.py test utilizadores.tests.funcionais.test_validar_utilizador


:: Componente Colaboradores

python manage.py test colaboradores.tests.funcionais.test_consultar_tarefas


:: Componente Notificacoes

python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_individual
python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_participante_grupo
python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_unidade_organica_grupo
python manage.py test notificacoes.tests.funcionais.test_enviar_mensagem_admin_grupo
python manage.py test notificacoes.tests.funcionais.test_receber_mensagem