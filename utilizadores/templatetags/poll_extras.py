from django import template
from utilizadores.models import Utilizador, ProfessorUniversitario, Participante, Colaborador, Coordenador, Administrador
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
register = template.Library()

@register.filter(name='get_due_date_string')
def get_due_date_string(value):
    delta = value - date.today()

    if delta.days == 0:
        return "Today!"
    elif delta.days < 1:
        return "%s %s ago!" % (abs(delta.days),
            ("day" if abs(delta.days) == 1 else "days"))
    elif delta.days == 1:
        return "Tomorrow"
    elif delta.days > 1:
        return "In %s days" % delta.days


@register.filter(name='get_user_name') 
def get_user_name(id):
    try:
        user = User.objects.get(id=id)
        nome = user.first_name+" "+user.last_name
        return nome  
    except :
        return "Esta notificação foi gerada automáticamente"


@register.filter(name='get_email') 
def get_email(id):
    try:
        user = User.objects.get(id=id)
        email = user.email
        return email  
    except :
        return ""

@register.filter(name='get_user_type') 
def get_user_type(id):
    try:
        user = User.objects.get(id=id)

        if user.groups.filter(name="Participante").exists():
            result = "Participante"  
        elif user.groups.filter(name="ProfessorUniversitario").exists():
            result =  "Professor Universitário"   
        elif user.groups.filter(name="Colaborador").exists():
            result =  "Colaborador"
        elif user.groups.filter(name="Coordenador").exists():
            result =  "Coordenador" 
        elif user.groups.filter(name="Administrador").exists():
            result =  "Administrador"  
        else: 
            result = ""
        return result
    except :
        return 0             

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()        


@register.filter(name='get_faculdade_pu') 
def get_faculdade_pu(user,id):
    utilizador = ProfessorUniversitario.objects.get(id=id)
    return utilizador.faculdade.nome

@register.filter(name='get_departamento_pu') 
def get_departamento_pu(user,id):
    utilizador = ProfessorUniversitario.objects.get(id=id)
    return utilizador.departamento.nome    

@register.filter(name='get_gabinete_pu') 
def get_gabinete_pu(user,id):
    utilizador = ProfessorUniversitario.objects.get(id=id)
    return utilizador.gabinete     




@register.filter(name='get_faculdade_coord') 
def get_faculdade_coord(user,id):
    utilizador = Coordenador.objects.get(id=id)
    return utilizador.faculdade.nome

@register.filter(name='get_departamento_coord') 
def get_departamento_coord(user,id):
    utilizador = Coordenador.objects.get(id=id)
    return utilizador.departamento.nome    

@register.filter(name='get_gabinete_coord') 
def get_gabinete_coord(user,id):
    utilizador = Coordenador.objects.get(id=id)
    return utilizador.gabinete   






@register.filter(name='get_faculdade_colaborador') 
def get_faculdade_colaborador(user,id):
    utilizador = Colaborador.objects.get(id=id)
    return utilizador.faculdade.nome

@register.filter(name='get_departamento_colaborador') 
def get_departamento_colaborador(user,id):
    utilizador = Colaborador.objects.get(id=id)
    return utilizador.departamento.nome    

@register.filter(name='get_curso_colaborador') 
def get_curso_colaborador(user,id):
    utilizador = Colaborador.objects.get(id=id)
    return utilizador.curso.nome   





@register.filter(name='get_gabinete_admin') 
def get_gabinete_admin(user,id):
    utilizador = Administrador.objects.get(id=id)
    return utilizador.gabinete  



@register.filter(name='apagar_admin') 
def apagar_admin(user,id):
    utilizadores = Administrador.objects.filter(valido="True")
    return len(utilizadores)>1    



@register.filter(name='apagar_coordenador') 
def apagar_coordenador(user,id):
    utilizadores = Coordenador.objects.filter(valido="True")
    return len(utilizadores)>1    