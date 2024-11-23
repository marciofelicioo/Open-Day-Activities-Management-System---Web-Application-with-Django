import time
from django.forms import * 
from .models import Atividade, Sessao,Materiais,Tema, Roteiro
from datetime import datetime
from configuracao.models import Campus, Diaaberto, Horario, Espaco, Departamento


def get_choices_time():
    return [(str(t),t) for t in range(30, 361, 30)]  

class DateTimeWidget(DateTimeInput):
    
    def __init__(self, attrs=None, format=None, input_type=None, default=None):
        #input_type = 'datetime-local'
        now = datetime.now()
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            if default is not None:
                self.attrs = {'class': 'input', 'value': default}
            else:
                self.attrs = {'class': 'input', 'value': str(now.date()) + ' ' + str(now.time().strftime('%H:%M'))}
        if format is not None:
            self.format = format
        else: 
            self.format = '%Y-%m-%d'

def get_tema_choices():
    return [(tema.id,tema.tema) for tema in Tema.objects.all()]

class AtividadeForm(ModelForm):
    tema = ChoiceField(choices=get_tema_choices)
    duracaoesperada= ChoiceField(choices=get_choices_time)
    class Meta:  
        model = Atividade  
        exclude = ['professoruniversitarioutilizadorid','datasubmissao', 'dataalteracao','estado','id','diaabertoid','tema','espacoid',]
        widgets = {
            'nome': TextInput(attrs={'class': 'input'}),
            'tipo': Select(),
            'descricao': Textarea(attrs={'class':'textarea'}),
            'publicoalvo': Select(),
            'nrcolaboradoresnecessario': NumberInput(attrs={'class': 'input'}),
            #'tempo': DateField(widget=DateInput(attrs={'class':'timepicker'})),
            'participantesmaximo': NumberInput(attrs={'class': 'input'}),
            'duracaoesperada': Select(),
            }



class MateriaisForm(ModelForm):
    class Meta:
        model = Materiais  
        exclude = ["atividadeid"]
        widgets = {
            'nomematerial': TextInput(attrs={'class': 'input'}),
            }

def get_dep_choices():
    return [(-1,'Mostra todos os Departamentos')] + [(departamento.id,departamento.nome) for departamento in Departamento.objects.all()]


class RoteiroForm(ModelForm):
    inicio = TimeField(label='Horário de ínicio', widget=TimeInput(attrs={'class': 'input', 'type': 'time'}))
    fim = TimeField(label='Horário de fim', widget=TimeInput(attrs={'class': 'input', 'type': 'time'}))
    nparticipantes = IntegerField(label='Nº de participantes', widget=NumberInput(attrs={'class': 'input'}))
    diasessao = DateField(label='Dia da Sessão', widget=Select(attrs={'class': 'select'}))

    class Meta:
        model = Roteiro
        fields = ['nome', 'descricao']
        widgets = {
            'nome': TextInput(attrs={'class': 'input', 'placeholder': 'Nome do Roteiro'}),
            'descricao': Textarea(attrs={'class': 'textarea', 'placeholder': 'Descrição do Roteiro'}),
            # 'diaabertoid': Select(attrs={'class': 'select'}),
        }   

    def clean_inicio(self):
        inicio = self.cleaned_data['inicio']
        diaAbertoInicio = Diaaberto.current().datadiaabertoinicio
        if inicio.hour < diaAbertoInicio.hour or (inicio.hour == diaAbertoInicio.hour and inicio.minute < diaAbertoInicio.minute):
            raise ValidationError(f'O horário de início deve ser no mínimo {diaAbertoInicio.hour}:{diaAbertoInicio.minute}.')
        return inicio

    def clean_fim(self):
        fim = self.cleaned_data['fim']
        diaAbertoFim = Diaaberto.current().datadiaabertofim
        if fim.hour > diaAbertoFim.hour or (fim.hour == diaAbertoFim.hour and fim.minute > diaAbertoFim.minute):
            raise ValidationError(f'O horário de fim deve ser no máximo {diaAbertoFim.hour}:{diaAbertoFim.minute}.')
        return fim
    
    def clean_nparticipantes(self):
        nparticipantes = self.cleaned_data['nparticipantes']
        if nparticipantes <= 0 or nparticipantes > 45:
            raise forms.ValidationError('O número de participantes deve ser um valor positivo até 45.')
        return nparticipantes

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('inicio')
        fim = cleaned_data.get('fim')

        # Validar se o horário de início é menor que o horário de fim
        if inicio and fim:
            if inicio >= fim:
                raise ValidationError('O horário de início deve ser anterior ao horário de fim.')
        return cleaned_data   