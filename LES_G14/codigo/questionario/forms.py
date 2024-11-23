from django import forms
from django.forms import DateInput
from configuracao.models import Diaaberto
from .models import Questionario, Pergunta, OpcaoResposta
from django.utils.timezone import now

class QuestionarioForm(forms.ModelForm):
    class Meta:
        model = Questionario
        fields = ['titulo', 'descricao']

    def clean(self):
        cleaned_data = super().clean()
        titulo = cleaned_data.get('titulo')
        descricao = cleaned_data.get('descricao')

        return cleaned_data
class PerguntaForm(forms.ModelForm):
    class Meta:
        model = Pergunta
        fields = ['texto', 'questionario','tipo','tema']
        labels = {
            'texto': 'Texto da Pergunta',
            'questionario': 'Questionário',
            'tipo': 'tipo da pergunta',
            'tema': 'tema da pergunta'
        }

class OpcaoRespostaForm(forms.ModelForm):
    class Meta:
        model = OpcaoResposta
        fields = ['texto', 'pergunta']
        labels = {
            'texto': 'Texto da Opção de Resposta',
            'pergunta': 'Pergunta',
        }

class PublicarQuestionarioForm(forms.Form):
    data_publicacao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))