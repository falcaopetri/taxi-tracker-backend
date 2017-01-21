# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-01-17 11:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corrida',
            name='motorista',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Motorista'),
        ),
        migrations.AlterField(
            model_name='corrida',
            name='passageiro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Passageiro'),
        ),
    ]