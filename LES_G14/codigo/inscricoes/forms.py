from . import models
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from configuracao.models import Campus, Diaaberto
import json
from django.utils.translation import gettext as _
import re
from atividades.models import Sessao
from django.core.exceptions import ValidationError
from datetime import date
import pytz
from datetime import datetime


class InfoForm(forms.Form):
    individual = forms.BooleanField(required=False)


class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = models.Responsavel
        exclude = ('inscricao',)


class InscricaoForm(forms.ModelForm):
    nome_escola = forms.CharField(max_length=200)
    local = forms.CharField(max_length=128)
    
    class Meta: 
        model = models.Inscricao
        exclude = ('escola', "ninscricao", 'participante',
                   'meio_transporte', 'hora_chegada', 'local_chegada', 'entrecampi')
        fields = '__all__'

    def clean(self):
        cleaned_data = super(InscricaoForm, self).clean()
        
        if cleaned_data.get('local', False):
            cleaned_data['local'] = cleaned_data['local'].capitalize()
        # Verificar se o dia escolhido faz parte do Dia Aberto
        if not cleaned_data.get('diaaberto', ''):
            hoje = datetime.now(pytz.utc)
            prox_diaaberto = Diaaberto.current()
            if prox_diaaberto:
                raise ValidationError(
                    _(f"""A data que escolheu não faz parte do Dia Aberto. Próximo dia aberto: de {prox_diaaberto.datadiaabertoinicio.strftime("%d/%m/%Y às %H:%M")}, até {prox_diaaberto.datadiaabertofim.strftime("%d/%m/%Y às %H:%M")}."""))
            else:
                raise ValidationError(
                    _(f"A data que escolheu não faz parte do Dia Aberto."))
        if not cleaned_data.get('individual', False) and (not cleaned_data.get('ano', False) or not cleaned_data.get('turma', False) or not cleaned_data.get('areacientifica', False)):
            raise ValidationError(
                _("Por favor, introduza toda a informação da turma."))
        if self.instance:
            inscricaoprato = self.instance.inscricaoprato_set.first()
            if inscricaoprato and inscricaoprato.npratosalunos + inscricaoprato.npratosdocentes > cleaned_data.get('nalunos', 0) + 5:
                raise ValidationError(
                    _("As inscrições nos almoços excedem o número de participantes disponíveis."))
            
            inscricoes_sessao = self.instance.inscricaosessao_set.all()
            for inscricao_sessao in inscricoes_sessao:
                if inscricao_sessao.nparticipantes > cleaned_data.get('nalunos', 0):
                    raise ValidationError(
                        _("As inscrições nas sessões excedem o número de participantes disponíveis."))

    def save(self, commit=True):
        self.instance.escola = models.Escola.objects.get_or_create(
            nome=self.cleaned_data['nome_escola'], local=self.cleaned_data['local'])[0]
        return super(InscricaoForm, self).save(commit=commit)


class TransporteForm(forms.Form):
    meio = forms.ChoiceField(choices=models.Inscricao.MEIO_TRANSPORTE_CHOICES)
    hora_chegada = forms.TimeField(required=False)
    local_chegada = forms.CharField(max_length=200, required=False)
    entrecampi = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(TransporteForm, self).clean()
        if cleaned_data.get('meio', '') != 'outro' and (not cleaned_data.get('hora_chegada', False) or not cleaned_data.get('local_chegada', False)):
            raise forms.ValidationError(
                _("Por favor, indique a hora e o local de chegada."))


class AlmocoForm(forms.ModelForm):

    class CampusField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.nome

    campus = CampusField(queryset=Campus.objects.all(), required=False)
    nalunos = forms.IntegerField()
    nresponsaveis = forms.IntegerField()
    individual = forms.BooleanField(required=False)

    class Meta:
        model = models.Inscricaoprato
        exclude = ('inscricao',)

    def clean(self):
        cleaned_data = super(AlmocoForm, self).clean()
        if cleaned_data.get('campus', False) and cleaned_data.get('npratosalunos', 0) <= 0 and cleaned_data.get('npratosdocentes', 0) <= 0:
            raise forms.ValidationError(
                _("Por favor, indique o número de pessoas se pretendem almoçar num Campus."))
        if (cleaned_data.get('npratosalunos', 0) > 0 or cleaned_data.get('npratosdocentes', 0) > 0) and not cleaned_data.get('campus', False):
            raise forms.ValidationError(
                _("Por favor, indique o Campus se 1 ou mais pessoas pretendem almoçar na Universidade."))
        if not cleaned_data.get('individual', False):
            if cleaned_data.get('npratosalunos', 0) > cleaned_data.get('nalunos', 0):
                raise forms.ValidationError(
                    _("O número de alunos inscritos no almoço excede o número de alunos disponíveis"))
            if cleaned_data.get('npratosdocentes', 0) > cleaned_data.get('nresponsaveis', 0) + 5:
                raise forms.ValidationError(
                    _("O número de docentes inscritos no almoço excede o número de docentes disponíveis"))
        else:
            if cleaned_data.get('npratosalunos', 0) + cleaned_data.get('npratosdocentes', 0) > cleaned_data.get('nalunos', 0):
                raise forms.ValidationError(
                    _("O número de inscritos no almoço excede o número de pessoas disponíveis"))

    def save(self, commit=True):
        if self.cleaned_data.get('campus', False) and (self.cleaned_data.get('npratosalunos', 0) > 0 or self.cleaned_data.get('npratosdocentes', 0) > 0):
            return super(AlmocoForm, self).save(commit=commit)
        return None


def horarios_intersetam(t1start, t1end, t2start, t2end):
    return (t1start <= t2start < t1end) or (t2start <= t1start < t2end)


def verificar_vagas(sessoes, nalunos, dia):
    """
    Retorna ValidationError caso haja conflitos em relação ao número de inscritos nas sessões.
    """
    inscritos_horarios = []
    for sessao in sessoes:
        try:
            horario = Sessao.objects.get(pk=sessao).horarioid
            inscritos_horarios.append({
                'sessao': sessao,
                'inicio': horario.inicio,
                'fim': horario.fim,
                'ninscritos': sessoes[sessao],
            })
        except:
            raise forms.ValidationError(
                _("Ocorreu um erro inesperado. Por favor, tente submeter uma nova inscrição."))
    for sessao in sessoes:
        try:

            nalunos_horario = nalunos
            sessao_obj = Sessao.objects.get(pk=sessao)
        except:
            raise forms.ValidationError(
                _("Ocorreu um erro inesperado. Por favor, tente submeter uma nova inscrição."))
        if sessao_obj.atividadeid.estado != "Aceite":
            raise forms.ValidationError(
                _(f"A seguinte atividade não se encontra validada: \"{sessao_obj.atividadeid.nome}\"."))
        if sessao_obj.dia != dia:
            raise forms.ValidationError(
                _(f"A seguinte sessão não faz parte do dia da inscrição: \"{sessao_obj.atividadeid.nome}\", dia {sessao_obj.dia}, das {sessao_obj.horarioid.inicio.strftime('%H:%M')} às {sessao_obj.horarioid.fim.strftime('%H:%M')}. Dia da inscrição: {dia}"))
        if sessoes[sessao] > sessao_obj.vagas:
            raise forms.ValidationError(
                _(f"O número de inscritos na sessão da atividade \"{sessao_obj.atividadeid.nome}\", das {sessao_obj.horarioid.inicio.strftime('%H:%M')} às {sessao_obj.horarioid.fim.strftime('%H:%M')} ({sessoes[sessao]} inscritos) excede o nº de vagas para essa sessão ({sessao_obj.vagas} vagas). Este erro pode ter ocorrido porque foi submetida entretanto uma outra inscrição que ocupou as vagas pretendidas. Por favor, atualize as suas inscrições nas sessões."))
        if sessoes[sessao] > nalunos:
            raise forms.ValidationError(
                _(f"O número de inscritos na sessão da atividade \"{sessao_obj.atividadeid.nome}\", das {sessao_obj.horarioid.inicio.strftime('%H:%M')} às {sessao_obj.horarioid.fim.strftime('%H:%M')} ({sessoes[sessao]} inscritos) excede o nº de alunos disponíveis nesse horário ({nalunos} alunos)."))
        sessoes_simultaneas = []
        for inscritos_horario in inscritos_horarios:
            if inscritos_horario['sessao'] is not sessao and horarios_intersetam(sessao_obj.horarioid.inicio, sessao_obj.horarioid.fim, inscritos_horario['inicio'], inscritos_horario['fim']):
                nalunos_horario -= inscritos_horario['ninscritos']
                sessoes_simultaneas.append(inscritos_horario)
        if sessoes[sessao] > nalunos_horario:
            quote = '"'
            raise forms.ValidationError(
                _(f"O número de inscritos na sessão da atividade \"{sessao_obj.atividadeid.nome}\", das {sessao_obj.horarioid.inicio.strftime('%H:%M')} às {sessao_obj.horarioid.fim.strftime('%H:%M')} ({sessoes[sessao]} inscritos) excede o nº de alunos disponíveis nesse horário ({nalunos_horario} alunos). Sessões simultâneas: {', '.join([quote + Sessao.objects.get(pk=sessao_simultanea['sessao']).atividadeid.nome + quote + ' das ' + sessao_simultanea['inicio'].strftime('%H:%M') + ' às ' + sessao_simultanea['fim'].strftime('%H:%M') + ' (' + str(sessao_simultanea['ninscritos']) + ' inscritos)' for sessao_simultanea in sessoes_simultaneas])}."))


class SessoesForm(forms.Form):
    sessoes = forms.CharField()
    sessoes_info = forms.CharField()
    nalunos = forms.IntegerField(min_value=1)
    dia = forms.DateField()

    def clean(self):
        cleaned_data = super(SessoesForm, self).clean()
        try:
            cleaned_data['sessoes'] = cleaned_data.get(
                'sessoes', '{}').replace('\\', '')
            pattern = re.compile(
                '\s*{\s*(\"\s*\d+\s*\"\s*:\s*\d+\s*,\s*)*\"\s*\d+\s*\"\s*:\s*\d+\s*}\s*|\s*{\s*}\s*')
            # JSON object like {"4":4}
            if re.match(pattern, cleaned_data.get('sessoes', '{}')) is None:
                raise Exception()
            _sessoes = json.loads(cleaned_data.get('sessoes', '{}'))
            cleaned_data['sessoes'] = {sessao: _sessoes[sessao]
                                       for sessao in _sessoes if _sessoes[sessao] > 0}
        except:
            raise forms.ValidationError(
                _("Ocorreu um erro inesperado. Por favor, tente submeter uma nova inscrição."))
        if not cleaned_data.get('sessoes', False):
            raise forms.ValidationError(
                _("Deve inscrever-se, no mínimo, em uma sessão."))
        
        
        verificar_vagas(cleaned_data['sessoes'],
                        cleaned_data.get('nalunos', 0), cleaned_data.get('dia'))


class MarcarPresencaForm(forms.Form):
    presenca = forms.BooleanField(
        label='Presença Confirmada',
        required=False
    )
    nr_presentes = forms.IntegerField(
        label='Número de Presentes',
        min_value=0
    )