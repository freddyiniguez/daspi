# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 16:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requirement', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('complexity', models.IntegerField()),
                ('role', models.CharField(max_length=200)),
                ('required_hours', models.IntegerField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estimates', to='tool.Project')),
            ],
        ),
    ]
