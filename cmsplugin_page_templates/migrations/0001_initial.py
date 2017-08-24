# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-02-24 14:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('template', models.TextField(help_text="The template has to be compatible with Django's templating engine", verbose_name='HTML Template')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='site_templates', to='sites.Site')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Page Template',
                'verbose_name_plural': 'Page Templates',
            },
        ),
        migrations.AlterUniqueTogether(
            name='pagetemplate',
            unique_together=set([('site', 'name')]),
        ),
    ]