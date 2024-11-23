from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from django.forms import *
from django.contrib.auth.models import User
from django import forms

from utilizadores.models import *



USER_CHOICES = (
    ("Administrador", "Administrador"),
    ("Coordenador", "Coordenador"),
    ("ProfessorUniversitario", "Professor Universitário"),
    ("Participante", "Participante"),
    ("Colaborador", "Colaborador"),
)

class UtilizadorFiltro(Form):
    filtro_tipo = ChoiceField(
        choices=USER_CHOICES,
        widget=Select(),
        required=True,
    )



USER_CHOICES_PARTICIPANTE = (
    ("Administrador", "Administrador"),
)

class UtilizadorFiltroParticipante(Form):
    filtro_tipo = ChoiceField(
        choices=USER_CHOICES_PARTICIPANTE,
        widget=Select(),
        required=True,
    )


USER_CHOICES_UO = (
    ("Administrador", "Administrador"),
    ("Coordenador", "Coordenador"),
    ("ProfessorUniversitario", "Professor Universitário"),
    ("Colaborador", "Colaborador"),
)

class UtilizadorFiltroUO(Form):
    filtro_tipo = ChoiceField(
        choices=USER_CHOICES_UO,
        widget=Select(),
        required=True,
    )

class MensagemFormIndividualAdmin(forms.Form):
    email = CharField(widget=TextInput(), max_length=255, required=False)
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    def clean(self):
        email = self.cleaned_data.get('email')
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        # email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(f'Este email não é válido!')
        if email == "" or titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')


class MensagemFormGrupoAdmin(forms.Form):
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    def clean(self):
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        if titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')

class MensagemFormIndividualUO(forms.Form):
    email = CharField(widget=TextInput(), max_length=255, required=False)
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)

    def clean(self):
        email = self.cleaned_data.get('email')
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(f'Este email não é válido!')
        if email == "" or titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')


class MensagemFormGrupoUO(forms.Form):
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    def clean(self):
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        if titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')


class MensagemFormIndividualParticipante(forms.Form):
    email = CharField(widget=TextInput(), max_length=255, required=False)
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    def clean(self):
        email = self.cleaned_data.get('email')
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        # email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(f'Este email não é válido!')
        temp = Utilizador.objects.get(email=email)
        if not temp.emailValidoParticipante():
            raise forms.ValidationError(f'Este email não pertence a um administrador!')            
        if email == "" or titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')


class MensagemFormGrupoParticipante(forms.Form):
    titulo = CharField(widget=TextInput(), max_length=255, required=False)
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    def clean(self):
        titulo = self.cleaned_data.get('titulo')
        mensagem = self.cleaned_data.get('mensagem')
        if titulo=="" or mensagem=="":
            raise forms.ValidationError(f'Todos os campos são obrigatórios!')






class MensagemResposta(forms.Form):
    mensagem = CharField(widget=forms.Textarea, max_length=255, required=False)
    msg_atual = forms.CharField(widget=forms.HiddenInput())
    def clean(self):
        mensagem = self.cleaned_data.get('mensagem')
        if mensagem=="":
            raise forms.ValidationError(f'A mensagem não pode ser vazia!')
