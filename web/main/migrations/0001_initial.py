# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 12:07
from __future__ import unicode_literals

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=30)),
                ('zabbix_user', models.CharField(blank=True, max_length=100, null=True)),
                ('zabbix_pass', models.CharField(blank=True, max_length=100, null=True)),
                ('token', models.CharField(default=main.models.token_generator, max_length=100)),
            ],
        ),
    ]
