# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

from wbc.core.models import Model
from wbc.region.models import Entity
from photologue.models import Photo
from wbc.projects.slug import unique_slugify
from wbc.tags.models import TaggedItems

from taggit.managers import TaggableManager

class StakeholderRole(Model):
    role        = models.CharField(blank=False, max_length=64, verbose_name="Rolle", help_text="Art der Rolle")
    slug        = models.SlugField(unique=True,editable=False)
    description = models.TextField(blank=True,null=True)

    class Meta:
        verbose_name        = 'Rolle'
        verbose_name_plural = 'Rollen'

    def __unicode__(self):
        return unicode(self.role)

    def save(self, *args, **kwargs):
        unique_slugify(self,self.role)
        super(StakeholderRole, self).save(*args, **kwargs)

class Stakeholder(Model):
    name        = models.CharField(blank=False, max_length=64, verbose_name="Name", help_text="Name des Akteurs")
    address     = models.CharField(max_length=256, blank=True, verbose_name="Adresse", help_text="Eine genaue Adresse des Akteur")
    description = models.TextField(blank=True, verbose_name="Beschreibung", help_text="Beschreibung des Stakeholders")
    active      = models.BooleanField(default=True)
    link        = models.URLField(blank=True)
    tags        = TaggableManager(through=TaggedItems, blank=True)
    entities    = models.ManyToManyField(Entity, blank=True, verbose_name="Region", related_name='places_%(class)s')
    slug        = models.SlugField(unique=True,editable=False)
    roles       = models.ManyToManyField(StakeholderRole, blank=True, related_name='roles_%(class)s', verbose_name='Rollen')
    picture     = models.OneToOneField(Photo, blank=True, null=True, verbose_name='Bild')


    def get_absolute_url(self):
        return reverse('stakeholder', kwargs={'slug': self.slug})


    class Meta:
        verbose_name        = 'Akteur'
        verbose_name_plural = 'Akteure'

    def __unicode__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        unique_slugify(self,self.name)
        super(Stakeholder, self).save(*args, **kwargs)

class Department(Stakeholder):

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name        = 'Behörde'
        verbose_name_plural = 'Behörden'
