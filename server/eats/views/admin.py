from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render

from tmapi.exceptions import TopicMapExistsException
from tmapi.models import TopicMap, TopicMapSystemFactory

from eats.decorators import add_topic_map
from eats.lib.views import get_topic_or_404
from eats.models import (Authority, Calendar, DatePeriod, DateType, EATSUser,
                         EntityRelationshipType, EntityType, Language,
                         NamePartType, NameType, Script)
from eats.forms.admin import (AuthorityForm, CalendarForm, DatePeriodForm,
                              DateTypeForm, EntityRelationshipForm,
                              EntityTypeForm, LanguageForm, NamePartTypeForm,
                              NameTypeForm, ScriptForm)


def administration_panel (request):
    """Show the EATS administration panel."""
    context_data = {'has_tm': False}
    context_data['tm_create_status'] = request.GET.get('tm_create')
    tm = None
    try:
        tm = TopicMap.objects.get(iri=settings.EATS_TOPIC_MAP)
    except AttributeError:
        # The EATS_TOPIC_MAP setting is not set.
        context_data['tm_status'] = 'no_setting'
    except TopicMap.DoesNotExist:
        context_data['tm_status'] = 'no_tm'
    if tm is not None:
        context_data['has_tm'] = True
    return render(request, 'eats/admin/panel.html', context_data)

def create_topic_map (request):
    """Creates the topic map to be used by the EATS application, and
    populates it with the base ontological data. Returns a status
    message.

    :rtype: string

    """
    if request.method == 'GET':
        return redirect('administration-panel')
    factory = TopicMapSystemFactory.new_instance()
    tms = factory.new_topic_map_system()
    try:
        tms.create_topic_map(settings.EATS_TOPIC_MAP)
        status = 'created'
    except TopicMapExistsException:
        status = 'exists'
    except:
        status = 'failed'
    redirect_url = urljoin(reverse('administration-panel'), '?tm_create=' +
                           status)
    return HttpResponseRedirect(redirect_url)

@add_topic_map
def topic_list (request, topic_map, model):
    topics = model.objects.all()
    context_data = {'opts': model._meta, 'topics': topics}
    return render(request, 'eats/admin/topic_list.html', context_data)

@add_topic_map
def topic_add (request, topic_map, model):
    form_class = get_form_class(model)
    opts = model._meta
    if request.method == 'POST':
        form = form_class(topic_map, model, request.POST)
        if form.is_valid():
            topic = form.save()
            redirect_url = get_redirect_url(form, opts, topic)
            return HttpResponseRedirect(redirect_url)
    else:
        form = form_class(topic_map, model)
    context_data = {'form': form, 'opts': opts}
    return render(request, 'eats/admin/topic_add.html', context_data)

@add_topic_map
def topic_change (request, topic_map, topic_id, model):
    topic = get_topic_or_404(model, topic_id)
    opts = model._meta
    form_class = get_form_class(model)
    if request.method == 'POST':
        form = form_class(topic_map, model, request.POST, instance=topic)
        if form.is_valid():
            form.save()
            redirect_url = get_redirect_url(form, opts, topic)
            return HttpResponseRedirect(redirect_url)
    else:
        form = form_class(topic_map, model, instance=topic)
    context_data = {'form': form, 'opts': opts, 'name': topic.get_admin_name()}
    return render(request, 'eats/admin/topic_change.html', context_data)

@add_topic_map
def topic_delete (request, topic_map, topic_id, model):
    topic = get_topic_or_404(model, topic_id)

def get_form_class (model):
    """Returns the class of the admin form to use for `model` topics.

    :param model: model class
    :type model: `Model`
    :rtype: class

    """
    if model == Authority:
        form_class = AuthorityForm
    elif model == Calendar:
        form_class = CalendarForm
    elif model == DatePeriod:
        form_class = DatePeriodForm
    elif model == DateType:
        form_class = DateTypeForm
    elif model == EntityType:
        form_class = EntityTypeForm
    elif model == EntityRelationshipType:
        form_class = EntityRelationshipForm
    elif model == Language:
        form_class = LanguageForm
    elif model == NamePartType:
        form_class = NamePartTypeForm
    elif model == NameType:
        form_class = NameTypeForm
    elif model == Script:
        form_class = ScriptForm
    return form_class

def get_redirect_url (form, opts, topic):
    object_type = opts.model_name
    if '_addanother' in form.data:
        redirect_url = reverse(object_type + '-add')
    elif '_continue' in form.data:
        redirect_url = reverse(object_type + '-change',
                               kwargs={'topic_id': topic.get_id()})
    else:
        redirect_url = reverse(object_type + '-list')
    return redirect_url

def user_list (request):
    eats_users = EATSUser.objects.all()
    django_users = User.objects.filter(eats_user__isnull=True)
    context_data = {'eats_users': eats_users, 'django_users': django_users}
    return render(request, 'eats/admin/user_list.html', context_data)

def user_change (request, eats_user_id):
    # This is a ridiculous workaround Django failing the
    # create_topic_map test if, in the course of reversing the
    # appropriate URL, it comes across a model form containing fields
    # that reference a topic. Bravo!
    from eats.forms.admin_model import EATSUserForm
    try:
        eats_user = EATSUser.objects.get(pk=eats_user_id)
    except EATSUser.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        form = EATSUserForm(request.POST, instance=eats_user)
        if form.is_valid():
            form.save()
            if '_continue' in form.data:
                redirect_url = reverse('user-change', kwargs={
                        'eats_user_id': eats_user.pk})
            else:
                redirect_url = reverse('user-list')
            return HttpResponseRedirect(redirect_url)
    else:
        form = EATSUserForm(instance=eats_user)
    context_data = {'form': form, 'user': eats_user.user}
    return render(request, 'eats/admin/user_change.html', context_data)

def user_activate (request):
    """Creates an EATS user for the POSTed Django user ID."""
    redirect_url = reverse('user-list')
    if request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        if user_id is not None:
            try:
                user = User.objects.get(id=user_id)
                try:
                    eats_user = user.eats_user
                except EATSUser.DoesNotExist:
                    eats_user = EATSUser(user=user)
                    eats_user.save()
                    redirect_url = reverse('user-change', kwargs={
                            'eats_user_id': user_id})
            except User.DoesNotExist:
                pass
    return HttpResponseRedirect(redirect_url)
