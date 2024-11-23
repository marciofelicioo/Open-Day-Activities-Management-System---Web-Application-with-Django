from django.forms import * 
from .models import *
from atividades.models import Atividade,Sessao
from utilizadores.models import Colaborador,Coordenador
from configuracao.models import Departamento, Diaaberto, Horario, Espaco
from datetime import datetime,timezone,timedelta
from inscricoes.models import Inscricao,Inscricaosessao

def get_dias():
    try:
        today= datetime.now(timezone.utc) 
        diaaberto=Diaaberto.objects.get(datadiaabertoinicio__gte=today,datadiaabertofim__gte=today)
        diainicio= diaaberto.datadiaabertoinicio.date()
        diafim= diaaberto.datadiaabertofim.date()
        totaldias= diafim-diainicio+timedelta(days=1)
        return [('','Escolha o dia')]+[(diainicio+timedelta(days=d),diainicio+timedelta(days=d))for d in range(totaldias.days)]
    except:
        return [('','Escolha o dia')]

class CustomTimeWidget(TimeInput):

    def __init__(self, attrs=None, format=None, input_type=None, default=None):
        input_type = 'time'
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            if default is not None:
                self.attrs = {'class': 'input', 'value': default}
        if format is not None:
            self.format = format
        else: 
            self.format = '%H:%M'

def get_atividades_choices(fac):
    return [("",'Escolha a Atividade')]+[(atividade.id,atividade.nome) for atividade in Atividade.tarefas_get_atividades(fac)]

class TarefaAuxiliarForm(Form):
    atividade = ChoiceField(widget=Select(attrs={'onchange':'diasSelect();'}))
    dia = DateField(widget=Select(attrs={'onchange':'sessoesSelect()'}))
    sessao = IntegerField(widget=Select(attrs={'onchange':'colaboradoresSelect()'}))
    colab = CharField(widget=Select(),required=False)

    def __init__(self,facul,*args, **kwargs):
        super(TarefaAuxiliarForm,self).__init__(*args, **kwargs)
        self.fields['atividade'] =  ChoiceField(widget=Select(attrs={'onchange':'diasSelect();'}),choices = get_atividades_choices(facul))

    def save(self,user,id=None):
        data = self.cleaned_data
        estado = 'naoConcluida'
        
        sessao = Sessao.objects.get(id = data.get('sessao'))
        if data.get('colab') == '':
            estado = 'naoAtribuida'
            colab = None
        else:
            colab = Colaborador.objects.get(id = data.get('colab'))
        atividade = Atividade.objects.get(id = data.get('atividade'))
        nome = 'Auxiliar na atividade ' + atividade.nome
        if id is None:
            tarefa=Tarefa.objects.create(nome= nome,estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=sessao.horarioid.inicio)
            TarefaAuxiliar.objects.create(tarefaid=tarefa,sessao=sessao)
            return tarefa.id
        else:
            Tarefa.objects.filter(id=id).update(nome= nome,estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=sessao.horarioid.inicio)
            TarefaAuxiliar.objects.filter(tarefaid=id).update(sessao=sessao)
            return id
        


def get_inscricao_choices(facul):
    return [('','Escolha um grupo')]+[(grupo.id,'Grupo '+str(grupo.id)) for grupo in Inscricao.get_tarefa_grupos(facul)]

class TarefaAcompanharForm(Form):
    grupo = ChoiceField(widget=Select(attrs={'onchange':'diasGrupo();grupoInfo();grupoHorario();grupoOrigem();grupoDestino();'}))
    dia = DateField(widget=Select(attrs={'onchange':'grupoHorario()'}))
    horario = TimeField(widget=Select(attrs={'onchange':'grupoOrigem()'}))
    origem = CharField(widget=Select(attrs={'onchange':'grupoDestino()'}))
    destino = CharField(widget=Select(attrs={'onchange':'colaboradoresSelect()'}))
    colab = CharField(widget=Select(),required=False)

    def __init__(self,facul,*args, **kwargs):
        super(TarefaAcompanharForm,self).__init__(*args, **kwargs)
        self.fields['grupo'] =  ChoiceField(widget=Select(attrs={'onchange':'diasGrupo();grupoInfo();grupoHorario();grupoOrigem();grupoDestino();'}),choices = get_inscricao_choices(facul))
    
    def save(self,user,id):
        data = self.cleaned_data
        nome = 'Acompanhar o grupo ' + data.get('grupo')
        grupo = Inscricao.objects.get(id=data.get('grupo'))
        
        destino = Espaco.objects.filter(id=int(data.get('destino'))).first()
        
        estado = 'naoConcluida'
        if data.get('colab') == '':
            estado = 'naoAtribuida'
            colab = None
        else:
            colab = Colaborador.objects.get(id = data.get('colab'))

        origem = data.get('origem')
        

        if  origem != 'Check in':
            local = Espaco.objects.get(id=int(origem))
            origem = str(local.id)  
        
        if id is None:
            tarefa = Tarefa.objects.create(nome= nome,estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=data.get('horario'))
            TarefaAcompanhar.objects.create(tarefaid=tarefa,origem=origem,destino=str(destino.id),inscricao=grupo)
            return tarefa.id
        else:
            Tarefa.objects.filter(id=id).update(nome= nome,estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=data.get('horario'))
            TarefaAcompanhar.objects.filter(tarefaid=id).update(origem=origem,destino=str(destino.id),inscricao=grupo)
            return id
    
    


class TarefaOutraForm(Form):
    dia = ChoiceField(widget=Select(attrs={'onchange':'colaboradoresSelect()'}),choices=get_dias())
    horario = TimeField(widget=TimeInput(attrs={'class':'input','type':'time','min':'09:00','max':'18:00','onchange':'colaboradoresSelect();'}))
    descricao = CharField(widget=Textarea(attrs={'class':'textarea'}))
    colab = CharField(widget=Select(),required=False)

    def save(self,user,id=None):
        data = self.cleaned_data
        nome = self.data.get('descricao')
        estado = 'naoConcluida'
        if data.get('colab') == '':
            estado = 'naoAtribuida'
            colab = None
        else:
            colab = Colaborador.objects.get(id = data.get('colab'))
        if id is None:
            tarefa = Tarefa.objects.create(nome= nome[0:18] + '...',estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=data.get('horario'))
            TarefaOutra(tarefaid=tarefa,descricao=data.get('descricao')).save()
            return tarefa.id
        elif id:
            Tarefa.objects.filter(id=id).update(nome= nome[0:18] + '...',estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=data.get('horario'))
            TarefaOutra.objects.filter(tarefaid=id).update(descricao=data.get('descricao'))
            return id
