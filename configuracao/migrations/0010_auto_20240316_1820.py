# Generated by Django 3.0.7 on 2024-03-16 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracao', '0009_auto_20240316_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportehorario',
            name='chegada',
            field=models.CharField(blank=True, choices=[('Terminal', 'Terminal'), ('Gambelas', 'Gambelas'), ('Penha', 'Penha')], db_column='Chegada', max_length=32),
        ),
        migrations.AlterField(
            model_name='transportehorario',
            name='origem',
            field=models.CharField(blank=True, choices=[('Terminal', 'Terminal'), ('Gambelas', 'Gambelas'), ('Penha', 'Penha')], db_column='Origem', max_length=32),
        ),
    ]