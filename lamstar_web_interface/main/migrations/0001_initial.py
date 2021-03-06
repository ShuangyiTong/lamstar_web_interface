# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-10 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('internal_id', models.CharField(max_length=64, primary_key=True, serialize=False, unique=True)),
                ('displayed_name', models.CharField(max_length=256)),
                ('network_type', models.CharField(max_length=64)),
                ('created_date', models.DateTimeField()),
                ('last_modified', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='NetworkLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('commands', models.CharField(max_length=65536)),
                ('data_sets', models.CharField(max_length=4096)),
                ('results', models.CharField(max_length=256)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Network')),
            ],
        ),
    ]
