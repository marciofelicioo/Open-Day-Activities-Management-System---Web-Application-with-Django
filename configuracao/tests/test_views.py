from django.test import TestCase, Client
from django.urls import reverse
from atividades.models import *
from configuracao.models import *
from utilizadores.models import *
from colaboradores.models import *
from coordenadores.models import *
from notificacoes.models import *
from inscricoes.models import *
from configuracao.tests.test_models import create_campus, create_curso, create_dep, create_edificio, create_horario, create_menu, create_open_day, create_prato, create_sala, create_transporteH, create_transporteU, create_uo
from utilizadores.tests.test_models import create_Administrador_0, create_Coordenador_0
from atividades.tests.test_models import create_tema
from datetime import time
import json

import urllib
import pytz

def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.parse.urlencode(kwargs) # for Python 3, use urllib.parse.urlencode instead

class TestViews(TestCase): 
    
    def setUp(self):
        self.client = Client()
        self.diaaberto = create_open_day()
        self.campus = create_campus()
        self.uo = create_uo(self.campus)
        self.dep = create_dep(self.uo)
        self.curso = create_curso(self.uo)
        self.lunchTime = create_horario(inicio=time(12,0),fim=time(14,0))
        self.menu = create_menu(
            campus=self.campus,
            horario=self.lunchTime,
            diaaberto=self.diaaberto
        )
        self.prato = create_prato(menu=self.menu)
        self.edificio = create_edificio(self.campus)
        self.espaco = create_sala(self.edificio)
        self.transporteH = create_transporteH(self.diaaberto)
        self.transporte = self.transporteH.transporte
        self.transporteU = create_transporteU(self.transporte)
        self.admin = create_Administrador_0()
        self.tema = create_tema()
        

    def test_ver_dias(self):
        client  = self.client

        response = client.get(reverse('configuracao:diasAbertos'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:diasAbertos'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=self.admin) #now we test with loggin
        response = client.get(reverse('configuracao:diasAbertos'))

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'configuracao/listaDiaAberto.html')
        self.assertContains(response,status_code=200,text=str(self.diaaberto.ano)) #vemos se o dia aparece na lista
        self.assertContains(response,status_code=200,text=str(self.diaaberto.descricao))
        self.assertContains(response,status_code=200,text='Criar novo Dia Aberto')
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:') #vemos se o dia aparece na lista

        #agora testamos se o filtro funciona, como so vai haver um ano, podemos verifica se apenas um ano aparece, ou nenhum
        #print(url_with_querystring(path=reverse('configuracao:diasAbertos'), ano=datetime.now().year))
        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), ano=datetime.now().year)) #apenas um ano
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=1) #vemos se o dia aparece na lista

        #print(url_with_querystring(path=reverse('configuracao:diasAbertos'), diainicio=str(date(1970,1,1))))
        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'),diainicio=str(date(1970,1,1)))) #agora as datas
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=1) #vemos se o dia aparece na lista

        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), diafim=str(date(2040,1,2)) ))
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=1) #vemos se o dia aparece na lista
       
        #no day filter

        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), ano=(datetime.now().year +1) )) #apenas um ano
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=0) #vemos se o dia aparece na lista

        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), diainicio=str(date(2299,5,27)))) #agora as datas
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=0) #vemos se o dia aparece na lista

        response = client.get(path=url_with_querystring(path=reverse('configuracao:diasAbertos'), diafim=str(date(2299,5,27))))
        self.assertContains(response,status_code=200,text='Inicio submissao Atividades:',count=0) #vemos se o dia aparece na lista

    def test_novo_dia(self):
        client = self.client

        response = client.get(reverse('configuracao:novoDia'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:novoDia'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')


        client.force_login(user=self.admin) #now we test with loggin
        response = client.get(reverse('configuracao:novoDia'))

        self.assertNotEquals(response.status_code,200)
        self.assertEquals(response.status_code,302)
        self.assertTemplateNotUsed(response, 'configuracao/diaAbertoForm.html') #it cant be right because current day is still open


        response = client.get(reverse('configuracao:novoDia'),follow=True)#if we follow the redirect...

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'configuracao/listaDiaAberto.html') 
       
    def test_new_day_POST(self):
        client = self.client

        client.force_login(user=self.admin) #now we test with loggin
        Diaaberto.objects.all().delete()
        data = {
            'precoalunos': 2,
            'precoprofessores': 2,
            'enderecopaginaweb': 'web.com',
            'descricao': 'Dia Aberto',
            'emaildiaaberto': 'web@web.com',
            'ano': '1970',
            'datadiaabertoinicio': '1970-01-01 9:30',
            'datadiaabertofim': '2040-01-02 9:30',
            'datainscricaoatividadesinicio': '1970-01-01 09:30',
            'datainscricaoatividadesfim': '2040-01-02 09:30',
            'datapropostasatividadesincio': '1970-01-01 09:30',
            'dataporpostaatividadesfim': '2040-01-02 09:30',
            'escalasessoes': '00:31',
        }
        response = client.post(reverse('configuracao:novoDia'), data=data)
        self.assertEquals(response.status_code,302) #302 means it inserted a redirected
        
        self.assertEquals(len(Diaaberto.objects.filter()),1)  
        self.assertEquals(Diaaberto.objects.filter(ano='1970').first().escalasessoes,time(0,31))

        Diaaberto.objects.all().delete()
        data['ano'] = '1971'
        data['datadiaabertoinicio'] = '2040-01-02 1287:30' #formato errado, deve falhar
        response = client.post(reverse('configuracao:novoDia'), data=data)
        self.assertContains(response, status_code=200 ,text = 'Introduza uma data') #back to same page with error
        self.assertEquals(len(Diaaberto.objects.filter()),0)        

    def test_del_day(self):
        client = self.client
        response = client.get(reverse('configuracao:eliminarDia', kwargs={'id':self.diaaberto.id}))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:eliminarDia', kwargs={'id':self.diaaberto.id}),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:eliminarDia', kwargs={'id':self.diaaberto.id}))
        self.assertEquals(response.status_code,200) #200 means it printed the error message on return (success is a redirect)

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:eliminarDia', kwargs={'id':self.diaaberto.id}))
        self.assertEquals(response.status_code,302) #redirect means it worked
        self.assertEquals(len(Diaaberto.objects.filter()),0) #must be empty!

    def test_view_menus(self):
        client = self.client

        response = client.get(reverse('configuracao:verMenus'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:verMenus'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:verMenus'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:verMenus'))
        self.assertContains(response,status_code=200,text='Feijoada')
        self.assertContains(response,status_code=200,text='Carne')

        
    def test_menus_POST(self):
        client = self.client
        data = {
            'campus': [str(self.campus.id)],
            'diaaberto': [str(self.diaaberto.id)],
            'dia': ['2021-05-23'],
            'form-TOTAL_FORMS': ['1'],
            'form-INITIAL_FORMS': ['0'],
            'form-MIN_NUM_FORMS': ['1'],
            'form-MAX_NUM_FORMS': ['1000'],
            'form-0-id': [''],
            'form-0-prato':['Carne Alentejana'],
            'form-0-tipo': ['Carne'],
            'form-0-nrpratosdisponiveis': ['1']          
        }

        response = client.get(reverse('configuracao:novoMenu'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:novoMenu'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:novoMenu'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        Menu.objects.all().delete()
        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.post(reverse('configuracao:novoMenu'),data=data)
        #print(response)
        self.assertEquals(len(Menu.objects.all()),1)
        self.assertEquals(Menu.objects.all().first().dia, date(2021,5,23))

        menuId = Menu.objects.filter().first().id
        #lets edit it
        data['dia'] = ['2021-05-24']
        response = client.post(reverse('configuracao:editarMenu', kwargs={'id':menuId}),data=data)
        self.assertEquals(Menu.objects.filter().first().dia, date(2021,5,24))
        Menu.objects.all().delete()

    def test_menu_delete(self):
        client = self.client
        response = client.get(reverse('configuracao:eliminarMenu', kwargs={'id':self.menu.id}))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:eliminarMenu', kwargs={'id':self.menu.id}),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:eliminarMenu', kwargs={'id':self.menu.id}))
        self.assertEquals(response.status_code,200) #200 means it printed the error message on return (success is a redirect)

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:eliminarMenu', kwargs={'id':self.menu.id}))
        self.assertEquals(response.status_code,302) #redirect means it worked
        self.assertEquals(len(Menu.objects.filter()),0) #must be empty!

    def test_view_temas(self):
        client = self.client

        response = client.get(reverse('configuracao:verTemas'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:verTemas'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:verTemas'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:verTemas'))
        self.assertContains(response,status_code=200,text='Farmacia')

        
    def test_temas_POST(self):
        client = self.client
        data = {
            'tema': ['Tecnologia'],         
        }

        response = client.get(reverse('configuracao:adicionarTema'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:adicionarTema'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:adicionarTema'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        Tema.objects.all().delete()
        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.post(reverse('configuracao:adicionarTema'),data=data)
        #print(response)
        self.assertEquals(len(Tema.objects.all()),1)
        self.assertEquals(Tema.objects.all().first().tema, 'Tecnologia')

        temaId = Tema.objects.filter().first().id
        #lets edit it
        data['tema'] = ['Informatica']
        response = client.post(reverse('configuracao:editarTema', kwargs={'id':temaId}),data=data)
        self.assertEquals(Tema.objects.filter().first().tema, 'Informatica')
        Tema.objects.all().delete()

    def test_tema_delete(self):
        client = self.client
        response = client.get(reverse('configuracao:eliminarTema', kwargs={'id':self.tema.id}))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:eliminarTema', kwargs={'id':self.tema.id}),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:eliminarTema', kwargs={'id':self.tema.id}))
        self.assertEquals(response.status_code,200) #200 means it printed the error message on return (success is a redirect)

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:eliminarTema', kwargs={'id':self.tema.id}))
        self.assertEquals(response.status_code,302) #redirect means it worked
        self.assertEquals(len(Tema.objects.filter()),0) #must be empty!

    def test_view_uos(self):
        client = self.client

        response = client.get(reverse('configuracao:verUOs'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:verUOs'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:verUOs'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:verUOs'))
        self.assertContains(response,status_code=200,text='Faculdade de Ciencias e Tecnologias')

        
    def test_uos_POST(self):
        client = self.client
        data = {
           'form-TOTAL_FORMS': ['1'],
           'form-INITIAL_FORMS': ['0'],
           'form-MIN_NUM_FORMS': ['1'],
           'form-MAX_NUM_FORMS': ['1000'],
           'form-0-id': [''],
           'form-0-sigla': ['FT'],
           'form-0-nome': ['Faculdade de TESTE'],
           'form-0-campusid': [str(self.campus.id)] 
        }

        response = client.get(reverse('configuracao:adicionarUO'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:adicionarUO'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:adicionarUO'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        Unidadeorganica.objects.all().delete()
        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.post(reverse('configuracao:adicionarUO'),data=data)
        #print(Unidadeorganica.objects.all().first().id)
        self.assertEquals(len(Unidadeorganica.objects.all()),1)
        self.assertEquals(Unidadeorganica.objects.all().first().nome, 'Faculdade de TESTE')

        uoId = Unidadeorganica.objects.filter().first().id
        #lets edit it
        data['form-INITIAL_FORMS'] = ['1']
        data['form-0-nome'] = ['Faculdade']
        data['form-0-id'] = [str(uoId)]
        response = client.post(reverse('configuracao:editarUO', kwargs={'id':uoId}),data=data)
        self.assertEquals(Unidadeorganica.objects.filter().first().nome, 'Faculdade')
        Unidadeorganica.objects.all().delete()

    def test_uo_delete(self):
        client = self.client
        response = client.get(reverse('configuracao:eliminarUO', kwargs={'id':self.uo.id}))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:eliminarUO', kwargs={'id':self.uo.id}),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:eliminarUO', kwargs={'id':self.uo.id}))
        self.assertEquals(response.status_code,200) #200 means it printed the error message on return (success is a redirect)

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:eliminarUO', kwargs={'id':self.uo.id}))
        self.assertEquals(response.status_code,302) #redirect means it worked
        self.assertEquals(len(Unidadeorganica.objects.filter()),0) #must be empty!
       
    def test_view_deps(self):
        client = self.client

        response = client.get(reverse('configuracao:verDepartamentos'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:verDepartamentos'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:verDepartamentos'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:verDepartamentos'))
        self.assertContains(response,status_code=200,text='Departamento de Engenharia Informatica e Eletronica')

        
    def test_deps_POST(self):
        client = self.client
        data = {
           'form-TOTAL_FORMS': ['1'],
           'form-INITIAL_FORMS': ['0'],
           'form-MIN_NUM_FORMS': ['1'],
           'form-MAX_NUM_FORMS': ['1000'],
           'form-0-id': [''],
           'form-0-sigla': ['DEEI'],
           'form-0-nome': ['Departamento de Engenharia Informatica e Eletronica'],
           'form-0-unidadeorganicaid': [str(self.uo.id)] 
        }

        response = client.get(reverse('configuracao:adicionarDepartamento'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:adicionarDepartamento'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:adicionarDepartamento'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        Departamento.objects.all().delete()
        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.post(reverse('configuracao:adicionarDepartamento'),data=data)

        self.assertEquals(len(Departamento.objects.all()),1)
        self.assertEquals(Departamento.objects.all().first().nome, 'Departamento de Engenharia Informatica e Eletronica')

        depId = Departamento.objects.filter().first().id
        #lets edit it
        data['form-0-id'] = [str(depId)]
        data['form-INITIAL_FORMS'] = ['1']
        data['form-0-nome'] = ['Departamento de Engenharia Informatica']
        response = client.post(reverse('configuracao:editarDepartamento', kwargs={'id':depId}),data=data)
        self.assertEquals(Departamento.objects.filter().first().nome, 'Departamento de Engenharia Informatica')
        Departamento.objects.all().delete()

    def test_dep_delete(self):
        client = self.client
        response = client.get(reverse('configuracao:eliminarDepartamento', kwargs={'id':self.dep.id}))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:eliminarDepartamento', kwargs={'id':self.dep.id}),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:eliminarDepartamento', kwargs={'id':self.dep.id}))
        self.assertEquals(response.status_code,200) #200 means it printed the error message on return (success is a redirect)

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:eliminarDepartamento', kwargs={'id':self.dep.id}))
        self.assertEquals(response.status_code,302) #redirect means it worked
        self.assertEquals(len(Departamento.objects.filter()),0) #must be empty!

    def test_view_edificios(self):
        client = self.client

        response = client.get(reverse('configuracao:verEdificios'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:verEdificios'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:verEdificios'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:verEdificios'))
        self.assertContains(response,status_code=200,text='C1')

        
    def test_edificios_POST(self):
        client = self.client
        data = {
            'nome': ['C1'],
            'campus': [str(self.campus.id)],
            'form-TOTAL_FORMS': ['1'],
            'form-INITIAL_FORMS': ['0'],
            'form-MIN_NUM_FORMS': ['1'],
            'form-MAX_NUM_FORMS': ['1000'],
            'form-0-id': [''],
            'form-0-nome': [str(self.espaco.nome)],
            'form-0-andar': [str(self.espaco.andar)],
            'form-0-descricao': [str(self.espaco.descricao)]
        }

        response = client.get(reverse('configuracao:adicionarEdificio'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:adicionarEdificio'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:adicionarEdificio'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        Edificio.objects.all().delete()
        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.post(reverse('configuracao:adicionarEdificio'),data=data)
        #print(response)
        self.assertEquals(len(Edificio.objects.all()),1)
        self.assertEquals(Edificio.objects.all().first().nome, 'C1')

        edificioId = Edificio.objects.filter().first().id
        #lets edit it
        #'nome': ['C2'], 'campus': ['1'], 'image': [''], 'form-TOTAL_FORMS': ['1'], 'form-INITIAL_FORMS': ['1'], 'form-MIN_NUM_FORMS': ['1'], 'form-MAX_NUM_FORMS': ['1000'], 'form-0-id': ['7'], 'form-0-nome': ['Sala 2'], 'form-0-andar': ['2'], 'form-0-descricao': ['Sala de Aula']}>
        data['nome'] = ['C2']
        data['form-INITIAL_FORMS'] = ['1']
        data['form-0-id'] = [str(edificioId)]
        data['form-0-nome'] = ['2']
        response = client.post(reverse('configuracao:editarEdificio', kwargs={'id':edificioId}),data=data)
        self.assertEquals(Edificio.objects.get(id=edificioId).nome, 'C2')
        self.assertEquals(Espaco.objects.get(edificio__id=edificioId).nome, '2')
        Edificio.objects.all().delete()

    def test_edificio_delete(self):
        client = self.client
        response = client.get(reverse('configuracao:eliminarEdificio', kwargs={'id':self.edificio.id}))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:eliminarEdificio', kwargs={'id':self.edificio.id}),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:eliminarEdificio', kwargs={'id':self.edificio.id}))
        self.assertEquals(response.status_code,200) #200 means it printed the error message on return (success is a redirect)

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:eliminarEdificio', kwargs={'id':self.edificio.id}))
        self.assertEquals(response.status_code,302) #redirect means it worked
        self.assertEquals(len(Edificio.objects.filter()),0) #must be empty!

    def test_view_curso(self):
        client = self.client

        response = client.get(reverse('configuracao:verCursos'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:verCursos'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:verCursos'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:verCursos'))
        self.assertContains(response,status_code=200,text='Licensiatura Engenharia Informatica')

        
    def test_curso_POST(self):
        client = self.client
        data = {
            'form-TOTAL_FORMS': ['1'],
            'form-INITIAL_FORMS': ['0'],
            'form-MIN_NUM_FORMS': ['1'],
            'form-MAX_NUM_FORMS': ['1000'],
            'form-0-id': [''],
            'form-0-nome': [str(self.curso.nome)],
            'form-0-sigla': [str(self.curso.sigla)],
            'form-0-unidadeorganicaid': [str(self.curso.unidadeorganicaid.id)]
        }

        response = client.get(reverse('configuracao:adicionarCurso'))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:adicionarCurso'),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:adicionarCurso'))
        self.assertContains(response,status_code=200,text='Não tem permissões para aceder a esta página!')

        Curso.objects.all().delete()
        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.post(reverse('configuracao:adicionarCurso'),data=data)
        #print(response)
        self.assertEquals(len(Curso.objects.all()),1)
        self.assertEquals(Curso.objects.all().first().nome, 'Licensiatura Engenharia Informatica')

        cursoId = Curso.objects.filter().first().id
        #lets edit it
        data['form-0-nome'] = ['Licensiatura Engenharia Eletronica']
        data['form-INITIAL_FORMS'] = ['1']
        data['form-0-id'] = [str(cursoId)]
        response = client.post(reverse('configuracao:editarCurso', kwargs={'id':cursoId}),data=data)
        self.assertEquals(Curso.objects.get(id=cursoId).nome, 'Licensiatura Engenharia Eletronica')
        Curso.objects.all().delete()

    def test_curso_delete(self):
        client = self.client
        response = client.get(reverse('configuracao:eliminarCurso', kwargs={'id':self.curso.id}))
        self.assertEquals(response.status_code,302) #Redirect if user not logged in

        response = client.get(reverse('configuracao:eliminarCurso', kwargs={'id':self.curso.id}),follow=True)#Not logged in goes to message
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'utilizadores/login.html')

        client.force_login(user=create_Coordenador_0()) #now we test with wrong loggin
        response = client.get(reverse('configuracao:eliminarCurso', kwargs={'id':self.curso.id}))
        self.assertEquals(response.status_code,200) #200 means it printed the error message on return (success is a redirect)

        client.force_login(user=self.admin) #now we test with proper loggin
        response = client.get(reverse('configuracao:eliminarCurso', kwargs={'id':self.curso.id}))
        self.assertEquals(response.status_code,302) #redirect means it worked
        self.assertEquals(len(Curso.objects.filter()),0) #must be empty!

#<
#QueryDict: {'csrfmiddlewaretoken': ['wnVI0xRKO8X7DGgbZS9g24r16kiAdEj6dIepN9xrt337AV3ioOgBm1FcB5cUKO7I'], 
#'campus': ['1'],
#'diaaberto': ['10']
#'dia': ['2021-05-23']
#'form-TOTAL_FORMS': ['1']
#'form-INITIAL_FORMS': ['1']
#'form-MIN_NUM_FORMS': ['1']
#'form-MAX_NUM_FORMS': ['1000'],
#'form-0-id': ['24'],
#'form-0-prato':['Carne Alentejana'],
#'form-0-tipo': ['Carne'],
#'form-0-nrpratosdisponiveis': ['1']}
#>



