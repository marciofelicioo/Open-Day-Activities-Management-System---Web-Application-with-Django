### Pre-requisitos

* [Python 3.8.2](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

### Instalação

1. Abrir o terminal na pasta onde vai ser guardado o projeto

e.g.:
```SH
cd ~/Documentos/Universidade/LES
```

2. Clonar o projeto do github

```SH
git clone https://github.com/6135/dia-aberto-new.git
```

3. Entrar na pasta do projeto

```SH
cd dia-aberto-new
```

4. Criar o ambiente do projeto (venv)

**Atenção: A versão de Python com a qual criar o ambiente do projeto deve ser igual para todos (v3.8.2)**

Para verificar se a versão de Python instalada é a indicada:

Linux:
```SH
python3.8 -V
```

Windows:
```SH
python -V
```

Se o comando anterior não devolver `Python 3.8.2`, há que mudar a versão antes de criar o ambiente.

Se a versão do Python estiver correta, segue a criação do ambiente (na pasta do projeto):

Linux:
```SH
python3.8 -m venv env
```

Windows:
```SH
python -m venv env
```

5. Ativar o ambiente no terminal

Linux:
```SH
source env/bin/activate
```

Windows:
```SH
env\Scripts\activate
```

Em Windows às vezes há problemas neste passo. Se der ErrorSecurityPolicy, ou algo do género, tentar isto na mesma shell:
```SH
Set-ExecutionPolicy Unrestricted -Force
env\Scripts\activate
```

A extensão padrão de Python do VSCode tem a opção de ativar automaticamente o ambiente em novos terminais. Para ativar a funcionalidade, há que abrir a **Palete de Comandos (F1)**,  **Python: Selecionar Interpretador** e escolher a opção cuja localização comece com `./env` ou `.\env`.

6. Atualizar as dependências iniciais do ambiente

```SH
pip install --upgrade pip setuptools
```

7. Instalar as dependências do projeto

```SH
pip install -r requirements.txt
```

8. Criar um ficheiro .env dentro da pasta dia_aberto (a mesma que tem o settings.py), com as informações sensíveis, como credenciais de acesso à base de dados

O ficheiro .env deve ter o mesmo género de formato do ficheiro já criado "example.env".

As informações de acesso à base de dados do servidor do Gui devem-lhe ser solicitadas.

Para ligar a uma base de dados MySQL local, por exemplo, o .env pode ser:

```
DATABASE_URL=mysql://user:password@localhost:3306/db
SECRET_KEY=q1^j3mv#y9-n&^*j)-rd3@lqqu@jv49p_99$mefzljeuz#fra3
EMAIL_HOST_USER=suporte.dia.aberto@gmail.com
EMAIL_HOST_PASSWORD=password # Pedir ao Barrocas
```

9. Gerar uma nova SECRET_KEY aleatória (https://djecrety.ir/) e substituí-la no .env

10. Criar uma DB vazia e substituir no .env

```SH
mysql -u [user] -p
CREATE DATABASE diaAberto
```
    
11. Gerar os ficheiros de migrações

```SH
python manage.py makemigrations notificacoes
python manage.py makemigrations atividades
python manage.py makemigrations colaboradores
python manage.py makemigrations configuracao
python manage.py makemigrations coordenadores
python manage.py makemigrations inscricoes
python manage.py makemigrations notifications
python manage.py makemigrations auth
python manage.py makemigrations utilizadores
```

12. Gerar as tabelas da DB

```SH
python manage.py migrate
```

13. Criar os grupos

```SH
python manage.py create_groups
```

14. Criar o primeiro administrador

```SH
python manage.py create_admin [password]
```


## Comandos fundamentais

#### Ativar o ambiente virtual no terminal

Linux:
```SH
source env/bin/activate
```

Windows:
```SH
env\Scripts\activate
```

#### Desativar o ambiente virtual no terminal

```SH
deactivate
```

#### Iniciar o servidor localmente

```SH
python manage.py runserver
```

#### Gerar migrações automaticamente através dos modelos

```SH
python manage.py makemigrations
```

#### Aplicar as migrações à base de dados

```SH
python manage.py migrate
```

#### Instalar nova dependência

```SH
pip install nome_da_dependência && pip freeze > requirements.txt
```

#### Instalar lista de dependências necessárias

```SH
pip install -r requirements.txt
```

#### Criar nova app (cada "componente" vai ser uma "app")

```SH
python manage.py startapp nome_da_app
```

#### Gerar automaticamente modelos através de tabelas da base de dados

```SH
python manage.py inspectdb tabela1 tabela2 > nome_da_app/models.py
```


## Dependências

| Dependência              | Descrição / (Dependência Pai)         |
| ------------------------ | ------------------------------------- |
| pip                      | Gestor de Pacotes (Python)            |
| setuptools               | Ferramentas (Python)                  |
| Django                   | Web Framework                         |
| sqlparse                 | (Django)                              |
| pytz                     | (Django)                              |
| asgiref                  | (Django)                              |
| mysqlclient              | Conector de Python a MySQL            |
| autopep8                 | Python Formatter                      |
| pycodestyle              | (autopep8)                            |
| django-environ           | Suporte de .env                       |
| django-filter            | Django Filters                        |
| django-formtools         | SessionWizard e outras Formtools      |
| pyquery                  | (django-formtools)                    |
| cssselect                | (pyquery)                             |
| lxml                     | (pyquery)                             |
| django-phonenumber-field | PhoneNumberField                      |
| phonenumbers             | (django-phonenumber-field)            |
| Babel                    | (django-phonenumber-field)            |
| django-tables2           | Filtros/Sorting/Pagination de tabelas |