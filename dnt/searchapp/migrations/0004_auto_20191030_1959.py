# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2019-10-30 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchapp', '0003_translationmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translationmodel',
            name='translation',
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation0',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation1',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation2',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation3',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation4',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation5',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation6',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation7',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation8',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='translationmodel',
            name='translation9',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
