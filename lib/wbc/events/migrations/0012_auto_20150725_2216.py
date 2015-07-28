# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150725_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='stakeholder',
            field=models.ManyToManyField(help_text=b'Lorem_ipsum_Test_Help_Text', related_name='stakeholders_event', verbose_name=b'stakeholders_%(class)s', to='stakeholder.Stakeholder', blank=True),
        ),
    ]