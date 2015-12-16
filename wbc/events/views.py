# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.syndication.views import Feed
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from models import *
from serializers import *
from forms import *

from wbc.core.views import ProtectedCreateView, ProtectedUpdateView, ProtectedDeleteView
from wbc.region.models import District
from wbc.events.models import Publication
from wbc.projects.models import Project

from guardian.decorators import permission_required_or_403, permission_required
from guardian.shortcuts import assign_perm, get_perms


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

class DateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DateSerializer
    queryset = Date.objects.all()

class MediaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MediaSerializer
    queryset = Media.objects.all()

class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()

class PublicationFeedMimeType(Rss201rev2Feed):
    mime_type = 'application/xml'

class PublicationCreate(ProtectedCreateView):
    model = Publication
    fields = '__all__'

    def get_initial(self):
        try:
            self.initial['project'] = Project.objects.get(
                pk=self.request.GET.get('project_id', None))
        except Project.DoesNotExist:
            self.initial['project'] = {}
        return self.initial


class PublicationUpdate(ProtectedUpdateView):
    model = Publication
    fields = '__all__'

    def get_initial(self):
        try:
            self.initial.project_events.add(Project.objects.get(
                pk=self.request.GET.get('project_id', None)))
        except Project.DoesNotExist:
            self.initial['project'] = {}
        return self.initial


class PublicationDelete(ProtectedDeleteView):
    model = Publication

    def get_success_url(self):
        return self.object.project.get_absolute_url()

class EventCreate(ProtectedCreateView):
    model = Event
    form_class = EventForm

    def dispatch(self, request, *args, **kwargs):
        @permission_required('%s.add_%s' % (self.model._meta.app_label, self.model._meta.model_name), accept_global_perms=True)
        @permission_required_or_403('%s.change_%s' % ('projects', 'project'), ('projects.project', 'pk', 'project_pk'), accept_global_perms=True)
        def wrapper(request, *args, **kwargs):
            return super(EventCreate, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)


    # def get_initial(self):
    #     initial_data = super(EventCreate, self).get_initial()
    #     try:
    #         initial_data['projects']= [Project.objects.get(pk=self.kwargs['pk'])]
    #     except Project.DoesNotExist:
    #         initial_data['projects'] = []
    #     return initial_data

    def form_valid(self, form):
        self.object = form.save()
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        self.object.projects_events.add(project)

        user = User.objects.get(username=self.request.user)
        assign_perm('change_%s' % (self.model._meta.model_name), user, self.object) 
        assign_perm('delete_%s' % (self.model._meta.model_name), user, self.object) 

        url = project.get_absolute_url()
        return JsonResponse({'redirect': url})

    def form_invalid(self, form):
        response = super(EventCreate, self).form_invalid(form)
        return response

class EventUpdate(ProtectedUpdateView):
    model = Event
    form_class = EventForm
    # fields = '__all__'
    
    def dispatch(self, request, *args, **kwargs):
        modelString = '%s.%s' % (self.model._meta.app_label, self.model._meta.model_name)
        # @permission_required('%s.change__%s' % (self.model._meta.app_label, self.model._meta.model_name), (modelString, 'pk', 'pk'), accept_global_perms=True)
        # @permission_required_or_403('%s.change_%s' % ('projects', 'project'), ('projects.project', 'pk', 'project_pk'), accept_global_perms=True)
        def wrapper(request, *args, **kwargs):
            return super(EventUpdate, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)



    # def get_initial(self):
    #     initial_data = super(EventUpdate, self).get_initial()
    #     # try:
    #     #     initial_data['projects']= self.object.projects_events.all()
    #     # except Project.DoesNotExist:
    #     #     initial_data['projects'] = []
    #     return initial_data
    
    def form_valid(self, form):
        self.object = form.save()
        url = self.object.projects_events.all()[0].get_absolute_url()
        return JsonResponse({'redirect': url})

    def form_invalid(self, form):
        response = super(EventUpdate, self).form_invalid(form)
        return response

class EventDelete(ProtectedDeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        modelString = '%s.%s' % (self.model._meta.app_label, self.model._meta.model_name)
        # @permission_required('%s.delete_%s' % (self.model._meta.app_label, self.model._meta.model_name), (modelString, 'pk', 'pk'), accept_global_perms=True)
        @permission_required_or_403('%s.change_%s' % ('projects', 'project'), ('projects.project', 'pk', 'project_pk'), accept_global_perms=True)
        def wrapper(request, *args, **kwargs):
            return super(EventDelete, self).dispatch(request, *args, **kwargs)
        return wrapper(request, *args, **kwargs)


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        response = super(EventDelete, self).post(request, args, **kwargs)
        if self.request.is_ajax():
            response_data = {"redirect": '/'}
            return JsonResponse(response_data)
        else:
            return response

    def get_success_url(self):
        return "/"

class DateCreate(EventCreate):
    model = Date
    form_class = DateForm

class DateUpdate(EventUpdate):
    model = Date
    form_class = DateForm
    
class DateDelete(EventDelete):
    model = Date


class MediaCreate(EventCreate):
    model = Media
    form_class = MediaForm

class MediaUpdate(EventUpdate):
    model = Media
    form_class = MediaForm

class MediaDelete(EventDelete):
    model = Media


class PubCreate(EventCreate):
    model = Publication
    form_class = PubForm

class PubUpdate(EventUpdate):
    model = Publication
    form_class = PubForm
    
class PubDelete(EventDelete):
    model = Publication


class PublicationFeed(Feed):
    title = settings.FEED_TITLE
    description = settings.FEED_DESCRIPTION
    link = settings.SITE_URL
    feed_url = '/feeds/'
    feed_type = PublicationFeedMimeType

    def get_object(self, request):
        if 'bezirk' in request.GET:
            district = request.GET['bezirk']
            try:
                District.objects.get(name=district)
            except District.DoesNotExist:
                raise Http404
            return Publication.objects.filter(project__entities__name=district)
        return Publication.objects

    def items(self, objs):
        return objs.order_by('-created')[:10]

    def item_title(self, item):
        title = item.process_step.process_type.name + \
            ': ' + item.process_step.name

        l = []
        if item.project.name != '':
            l.append(item.project.name)
        try:
            l.append(item.project.entities.all()[0].name)
        except IndexError:
            pass

        if l != []:
            title += ' (' + ', '.join(l) + ')'

        return title

    def item_description(self, item):
        return item.description

    def item_guid(self, item):
        return str(item.pk)

    def item_pubdate(self, item):
        return item.created

    def item_link(self, item):
        return settings.SITE_URL + reverse('wbc.projects.views.project', args=[item.project.pk])
