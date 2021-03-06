# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0005_auto_20170818_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase', models.CharField(choices=[(b'QA', b'Quality assurance'), (b'CHANGES', b'Changes'), (b'CLOSURE', b'Project closure'), (b'DEVT', b'Development'), (b'IMPLEMENTATION', b'Implementation'), (b'PLAN', b'Planning'), (b'TEST', b'Testing'), (b'REQM', b'Requirements management'), (b'CONTROL', b'Monitoring and control')], max_length=100)),
                ('task', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[(b'REQM', b'Requirement'), (b'TASK', b'Task'), (b'CHANGE', b'Changes')], max_length=20)),
                ('complexity', models.CharField(choices=[(b'VERY HIGH', b'Very high'), (b'HIGH', b'High'), (b'MEDIUM', b'Medium'), (b'LOW', b'Low'), (b'VERY LOW', b'Very low')], max_length=20)),
                ('percentage_of_completion', models.IntegerField()),
                ('planned_hours', models.FloatField()),
                ('real_hours', models.FloatField()),
                ('planned_cost', models.FloatField()),
                ('real_cost', models.FloatField()),
                ('planned_start_date', models.DateTimeField()),
                ('planned_end_date', models.DateTimeField()),
                ('real_start_date', models.DateTimeField(blank=True)),
                ('real_end_date', models.DateTimeField(blank=True)),
                ('resource', models.CharField(choices=[(b'MAURICIO', b'Mauricio Mendonza'), (b'HECTOR', b'Hector Guerrero'), (b'GERARDO', b'Gerardo'), (b'JOSHUA', b'Joshua Mendonza'), (b'ANTONIO', b'Antonio Nava')], max_length=50)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tool.Project')),
            ],
        ),
    ]
