# Generated by Django 5.1.3 on 2024-11-11 23:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgendadorScripts', '0002_scripts_remove_agendamento_caminho_script_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agendamento',
            name='script',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agendamentos', to='AgendadorScripts.scripts'),
        ),
    ]
