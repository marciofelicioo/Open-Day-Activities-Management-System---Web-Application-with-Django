from django.db import models
from django.utils import timezone
from notifications.base.models import AbstractNotification


class Notificacao(AbstractNotification):
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    class Meta(AbstractNotification.Meta):
        abstract = False
        db_table = 'Notificacao'
        app_label = 'notificacoes'






# Coloca temporariamente notificações geradas automaticamente com conteúdo informativo, quando passam 5 dias a notificação é enviada 
# e é apagada desta tabela da base de dados
class InformacaoNotificacao(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    data = models.DateTimeField(default=timezone.now, db_index=True)
    pendente = models.BooleanField(db_column='pendente', null=False)
    titulo 	= models.CharField(db_column='titulo', max_length=255)
    descricao = models.CharField(db_column='descricao', max_length=255)
    emissor = models.ForeignKey('utilizadores.Utilizador', models.CASCADE, db_column='emissorid', related_name='envia',null=True)  
    recetor = models.ForeignKey('utilizadores.Utilizador', models.CASCADE, db_column='recetorid', related_name='recebe',null=True,blank=True)  
    tipo = models.CharField(db_column='tipo', max_length=255)	
    lido = models.BooleanField(db_column='lido', null=False)	
    class Meta:
        db_table = 'InformacaoNotificacao'


# Informação da mensagem que pode ser enviada ou recebida
class InformacaoMensagem(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    data = models.DateTimeField(default=timezone.now, db_index=True)
    pendente = models.BooleanField(db_column='pendente', null=False)
    titulo 	= models.CharField(db_column='titulo', max_length=255)
    descricao = models.CharField(db_column='descricao', max_length=255)
    emissor = models.ForeignKey('utilizadores.Utilizador', models.CASCADE, db_column='emissorid', related_name='envia_mensagem',null=True)  
    recetor = models.ForeignKey('utilizadores.Utilizador', models.CASCADE, db_column='recetorid', related_name='recebe_mensagem',null=True,blank=True)  
    tipo = models.CharField(db_column='tipo', max_length=255)	
    lido = models.BooleanField(db_column='lido', null=False)	
    class Meta:
        db_table = 'InformacaoMensagem'





class MensagemRecebida(models.Model):
    mensagem = models.ForeignKey(
        InformacaoMensagem, models.CASCADE)

    class Meta:
        db_table = 'MensagemRecebida'



class MensagemEnviada(models.Model):
    mensagem = models.ForeignKey(
        InformacaoMensagem, models.CASCADE)

    class Meta:
        db_table = 'MensagemEnviada'