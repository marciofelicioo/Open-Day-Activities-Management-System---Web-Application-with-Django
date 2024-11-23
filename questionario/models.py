from django.db import models
from configuracao.models import Diaaberto
from atividades.models import Atividade

class TemaQuestionario(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    tema = models.CharField(db_column='Tema', max_length=64)

    @property
    def num_questionarios(self):
        return Pergunta.objects.filter(tema=self).count()

    def __str__(self):
        return str(self.tema)

    class Meta:
        db_table = 'TemaQuestionario'

class Estado(models.Model):
    ESTADO_CHOICES = [
        ('criado', 'Criado'),
        ('validado', 'Validado'),
        ('publicado', 'Publicado'),
        ('arquivado', 'Arquivado'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='criado')
    questionario = models.ForeignKey('Questionario', on_delete=models.CASCADE, related_name='historico_estados')

    def __str__(self):
        return self.get_estado_display()

    class Meta:
        db_table = 'Estado'

class Questionario(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    diaaberto = models.ForeignKey(Diaaberto, on_delete=models.CASCADE, related_name='questionarios')
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True, blank=True, related_name='current_estado')
    created_at = models.DateTimeField(auto_now_add=True)
    data_publicacao = models.DateTimeField(null=True, blank=True)
    data_validacao = models.DateTimeField(null=True, blank=True) 
    data_arquivo = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'Questionario'

        
class Pergunta(models.Model):
    TIPO_PERGUNTA_CHOICES = [
        ('escolhaMultipla', 'Escolha Múltipla'),
        ('inteiro', 'Inteiro'), 
        ('porExtenso', 'Por Extenso'),
    ]
    texto = models.CharField(max_length=300)
    questionario = models.ForeignKey('Questionario', related_name='perguntas', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=30, choices=TIPO_PERGUNTA_CHOICES, default='extenso')
    tema = models.ForeignKey(TemaQuestionario, related_name='perguntas', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'Pergunta'

class OpcaoResposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, related_name='opcoes_resposta', on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)
    class Meta:
        db_table = 'OpcaoResposta'

class Resposta(models.Model):
    questionario = models.ForeignKey('Questionario', on_delete=models.CASCADE, related_name='respostas')
    respondida = models.BooleanField(default=False)  # Verdadeiro se o questionário foi respondido, falso caso contrário
    
    class Meta:
        db_table = 'Resposta'