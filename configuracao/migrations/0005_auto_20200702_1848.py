# Generated by Django 3.0.7 on 2020-07-02 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracao', '0004_auto_20200702_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportehorario',
            name='chegada',
            field=models.CharField(blank=True, choices=[('Gambelas', 'Gambelas'), ('Terminal', 'Terminal'), ('Penha', 'Penha')], db_column='Chegada', max_length=32),
        ),
        migrations.AlterField(
            model_name='transportehorario',
            name='origem',
            field=models.CharField(blank=True, choices=[('Gambelas', 'Gambelas'), ('Terminal', 'Terminal'), ('Penha', 'Penha')], db_column='Origem', max_length=32),
        ),
    ]
