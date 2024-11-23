# Generated by Django 3.0.7 on 2024-03-15 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracao', '0005_auto_20200702_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transportehorario',
            name='chegada',
            field=models.CharField(blank=True, choices=[('Penha', 'Penha'), ('Terminal', 'Terminal'), ('Gambelas', 'Gambelas')], db_column='Chegada', max_length=32),
        ),
        migrations.AlterField(
            model_name='transportehorario',
            name='origem',
            field=models.CharField(blank=True, choices=[('Penha', 'Penha'), ('Terminal', 'Terminal'), ('Gambelas', 'Gambelas')], db_column='Origem', max_length=32),
        ),
    ]