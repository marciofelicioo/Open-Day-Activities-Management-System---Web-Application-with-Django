from django.forms import *
from .models import *
from atividades.models import *
from datetime import datetime
from datetime import timedelta, timezone
from coordenadores.forms import CustomTimeWidget
from questionario.models import TemaQuestionario

class DateTimeWidget(DateTimeInput):
    def __init__(self, attrs=None, format=None, input_type=None, hours='09', minutes='00', default=None):
        #input_type = 'datetime-local'
        now = datetime.now()
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            if default is not None:
                self.attrs = {'class': 'input', 'value': default}
            if hours and minutes is not None:
                self.attrs = {'class': 'input', 'value': str(now.date()) + ' ' + hours + ':' + minutes}
            else:
                self.attrs = {'class': 'input', 'value': str(now.date()) + ' ' + str(now.time().strftime('%H:%M'))}
        if format is not None:
            self.format = format
        else: 
            self.format = '%Y-%m-%d %H:%M'

class diaAbertoSettingsForm(ModelForm):  
    #descricao = CharField(widget=TinyMCE())
    class Meta:
        now = datetime.now()
        model = Diaaberto
        exclude = ['administradorutilizadorid', 'id']
        widgets = {
            'enderecopaginaweb': TextInput(attrs={'class': 'input'}),
            'emaildiaaberto': EmailInput(attrs={'class': 'input'}),
            'ano': NumberInput(attrs={'class': 'input', 'value': now.year}),
            'datadiaabertoinicio': DateTimeWidget(),
            'datadiaabertofim': DateTimeWidget(hours='17', minutes='00'),
            'datapropostasatividadesincio': DateTimeWidget(hours='23', minutes='55'),
            'dataporpostaatividadesfim': DateTimeWidget(hours='23', minutes='55'),
            'datainscricaoatividadesinicio': DateTimeWidget(hours='23', minutes='55'),
            'datainscricaoatividadesfim': DateTimeWidget(hours='23', minutes='55'),
            'descricao': Textarea(attrs={'class':'textarea'}),
            'precoalunos': NumberInput(attrs={'class':'input', 'step': '0.01','min': '0'}),
            'precoprofessores': NumberInput(attrs={'class':'input','step': '0.01','min': '0'}),
            'escalasessoes': TimeInput(attrs={'class':'input','step': '00:05','min': '00:05', 'max':'00:59','value':'00:05','type':'time'})
        }
    
class diaAbertoFilterForm(Form):
    searchAno = CharField(widget=NumberInput, required=False)
    orderByChoices = [('', 'Nao ordenar'),
        ('ano', 'Ordernar por: Ano'),
        ('-ano', 'Ordernar por: Ano (Decrescente)'),
        ('datadiaabertoinicio', 'Ordernar por: Inicio'),
        ('-datadiaabertoinicio', 'Ordernar por: Inicio (Descrescente)'),
        ('datadiaabertofim', 'Ordernar por: Fim'),
        ('-datadiaabertofim', 'Ordernar por: Fim (Descrescente)'),
    ]
    orderBy = ChoiceField(choices=orderByChoices, widget=Select(), required=False)

    showByChoices = [('','Mostrar todos'),
        ('1','Mostrar: Dias Abertos Ativos'),
        ('2','Mostrar: Submissao de Atividades Ativas'),
        ('3','Mostrar: Submissao de Inscricoes Ativas'),
    ]
    showBy = ChoiceField(choices=showByChoices, widget=Select(), required=False)


def get_diaaberto_choices():
    dia_choices = Diaaberto.objects.all()

    return [('','Escolha um Dia Aberto')]+[(dia.id,dia.ano) for dia in dia_choices]

def get_campus_choices():
    return [(camp.id,camp.nome) for camp in Campus.objects.all()]

class menuForm(ModelForm):
    diaaberto = ChoiceField(choices=get_diaaberto_choices,widget=Select())
    campus = ChoiceField(choices=get_campus_choices,widget=Select())

    def __init__(self,*args, **kwargs):
        super(menuForm, self).__init__(*args, **kwargs)
        self.data = self.data.copy()
        campus = self.data.get('campus')
        diaaberto = self.data.get('diaaberto')
        if campus is not None and diaaberto is not None:
            self.data['campus'] = Campus.objects.get(id=campus).id
            self.data['diaaberto'] = Diaaberto.objects.get(id=diaaberto).id

    def clean(self):
        cleaned_data = super().clean()
        campus_data = cleaned_data.get('campus')
        diaaberto_data = cleaned_data.get('diaaberto')
        dia = cleaned_data.get('dia')
        if campus_data is not None and diaaberto_data is not None:
            cleaned_data['campus'] = Campus.objects.get(id=campus_data)
            cleaned_data['diaaberto'] = Diaaberto.objects.get(id=diaaberto_data)
            self.instance.horarioid = Horario.objects.get(inicio='12:00:00',fim='14:00:00')
        else:
            raise ValidationError('Os campos preenchidos estão incorretos!')
        
    class Meta:
        model = Menu
        exclude = ['id','horarioid']
        widgets = {
            'dia': Select()
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "O conjunto Campus, dia aberto e dia não é unico",
            }
        }


class pratosForm(ModelForm):
    class Meta:
        model = Prato
        exclude = ['id','menuid']
        widgets = {
            'prato': TextInput(attrs={'class':'input'}),
            'nrpratosdisponiveis': NumberInput(attrs={'class':'input'}),
            'tipo': Select()
        }
class menusFilterForm(Form):
    searchAno = CharField(widget=TextInput(attrs={'class': 'input','placeholder':'Ano'}), required=False)
    penha=BooleanField(widget=CheckboxInput(),required=False)
    gambelas=BooleanField(widget=CheckboxInput(),required=False)
    portimao=BooleanField(widget=CheckboxInput(),required=False)

class transporteFilterForm(Form):
    searchId = CharField(widget=TextInput(attrs={'class': 'input','placeholder':'Ano'}), required=False)
    filter_from = ChoiceField(choices = [(None,'De'),('Gambelas','De Gambelas'),('Penha','De Penha'),('Terminal','De Terminal')],
                            widget=Select(),required=False)
    filter_to = ChoiceField(choices = [(None,'Para'),('Gambelas','Para Gambelas'),('Penha','Para Penha'),('Terminal','Para Terminal')],
                            widget=Select(),required=False)


def get_dia_choices():
    dia_aberto = Diaaberto.current()
    dia_choices = []
    if dia_aberto is None:
        dia_choices = [('','')]
    else:
        dia_choices = dia_aberto.days_as_tuples()
    return dia_choices

class transporteForm(ModelForm):
    dia = ChoiceField(choices=get_dia_choices)
    
    def clean(self):
        cleaned_data = super().clean()
        self.instance.diaaberto = Diaaberto().current()

    class Meta:
        model = Transporte
        exclude = ['id','diaaberto']
        widgets = {
            'identificador': TextInput(attrs={'class': 'input'}),
            'dia': Select(),
        }

class transporteUniversitarioForm(ModelForm):

    class Meta:
        model = Transporteuniversitario
        exclude = ['transporte', 'vagas']
        widgets = {
            'capacidade': TextInput(attrs={'class': 'input is-half'})
        }

class EdificioForm(ModelForm):
    class Meta:
        model = Edificio
        exclude = ['id']
        widgets = {
            'nome': TextInput(attrs={'class':'input'}),
        }

class EspacoForm(ModelForm):

    class Meta:
        model = Espaco
        exclude = ['id','edificio']
        widgets = {
            'nome': TextInput(attrs={'class':'input'}),
            'andar': NumberInput(attrs={'class':'input', 'max':'200'}),
            'descricao': TextInput(attrs={'class':'input'}),
        }

class TemaForm(ModelForm):

    class Meta:
        model = Tema
        exclude = ['id']
        widgets = {
            'tema': TextInput(attrs={'class':'input'}),
        }

class TemaQuestionarioForm(ModelForm):

    class Meta:
        model = TemaQuestionario
        exclude = ['id']
        widgets = {
            'tema': TextInput(attrs={'class':'input'}),
        }
