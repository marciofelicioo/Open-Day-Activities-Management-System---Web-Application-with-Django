# Generated by Django 3.0.7 on 2020-07-02 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuracao', '0003_auto_20200702_1848'),
        ('utilizadores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anfiteatro',
            fields=[
                ('espacoid', models.OneToOneField(db_column='EspacoID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='configuracao.Espaco')),
                ('espacoedificio', models.CharField(db_column='EspacoEdificio', max_length=255)),
            ],
            options={
                'db_table': 'Anfiteatro',
            },
        ),
        migrations.CreateModel(
            name='Arlivre',
            fields=[
                ('espacoid', models.OneToOneField(db_column='EspacoID', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='configuracao.Espaco')),
                ('espacoedificio', models.CharField(db_column='EspacoEdificio', max_length=255)),
            ],
            options={
                'db_table': 'ArLivre',
            },
        ),
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nome', models.CharField(db_column='Nome', max_length=255)),
                ('descricao', models.TextField(db_column='Descricao')),
                ('publicoalvo', models.CharField(choices=[('Ciencias e Tecnologia', 'Ciências e Tecnologia'), ('Linguas e Humanidades', 'Linguas e Humanidades'), ('Economia', 'Economia')], db_column='Publicoalvo', default='', max_length=255)),
                ('nrcolaboradoresnecessario', models.IntegerField(db_column='nrColaboradoresNecessario', default=0)),
                ('tipo', models.CharField(choices=[('Atividade Laboratorial', 'Atividade Laboratorial'), ('Tertulia', 'Tertulia'), ('Palestra', 'Palestra')], db_column='Tipo', default='Palestra', max_length=64)),
                ('estado', models.CharField(db_column='Estado', max_length=64)),
                ('datasubmissao', models.DateTimeField(auto_now_add=True, db_column='dataSubmissao')),
                ('dataalteracao', models.DateTimeField(auto_now=True, db_column='dataAlteracao')),
                ('duracaoesperada', models.IntegerField(db_column='duracaoEsperada')),
                ('participantesmaximo', models.IntegerField(db_column='participantesMaximo')),
                ('diaabertoid', models.ForeignKey(db_column='diaAbertoID', on_delete=django.db.models.deletion.CASCADE, to='configuracao.Diaaberto')),
                ('espacoid', models.ForeignKey(db_column='EspacoID', on_delete=django.db.models.deletion.CASCADE, to='configuracao.Espaco')),
                ('professoruniversitarioutilizadorid', models.ForeignKey(db_column='ProfessorUniversitarioUtilizadorID', on_delete=django.db.models.deletion.CASCADE, to='utilizadores.ProfessorUniversitario')),
            ],
            options={
                'db_table': 'Atividade',
            },
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('tema', models.CharField(db_column='Tema', max_length=64)),
            ],
            options={
                'db_table': 'Tema',
            },
        ),
        migrations.CreateModel(
            name='Sessao',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('ninscritos', models.IntegerField(db_column='NInscritos')),
                ('vagas', models.IntegerField(db_column='Vagas')),
                ('dia', models.DateField(blank=True, db_column='Dia', null=True)),
                ('atividadeid', models.ForeignKey(db_column='AtividadeID', on_delete=django.db.models.deletion.CASCADE, to='atividades.Atividade')),
                ('horarioid', models.ForeignKey(db_column='HorarioID', on_delete=django.db.models.deletion.DO_NOTHING, to='configuracao.Horario')),
            ],
            options={
                'db_table': 'Sessao',
            },
        ),
        migrations.CreateModel(
            name='Materiais',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nomematerial', models.CharField(blank=True, db_column='nome', max_length=255, null=True)),
                ('atividadeid', models.ForeignKey(db_column='AtividadeID', on_delete=django.db.models.deletion.CASCADE, to='atividades.Atividade')),
            ],
            options={
                'db_table': 'Materiais',
            },
        ),
        migrations.AddField(
            model_name='atividade',
            name='tema',
            field=models.ForeignKey(db_column='Tema', on_delete=django.db.models.deletion.CASCADE, to='atividades.Tema'),
        ),
    ]
