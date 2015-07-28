# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150725_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='dateAccepted',
            field=models.DateField(null=True, verbose_name=b'Eingegangen bzw. angelegt am', blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='dateSubmitted',
            field=models.DateField(null=True, verbose_name=b'vorgelegt am', blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='issued',
            field=models.DateField(null=True, verbose_name=b'Ver\xc3\xb6ffentlicht am', blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='media_created',
            field=models.DateField(null=True, verbose_name=b'Medieneintrag erstellt am', blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='modified',
            field=models.DateField(null=True, verbose_name=b'Ge\xc3\xa4ndert am', blank=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='valid',
            field=models.DateField(null=True, verbose_name=b'In Kraft getreten am, g\xc3\xbcltig von bis', blank=True),
        ),
    ]