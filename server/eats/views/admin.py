from urlparse import urljoin

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from tmapi.exceptions import TopicMapExistsException
from tmapi.models import TopicMap, TopicMapSystemFactory

from eats.decorators import add_topic_map
from eats.models import Authority, Calendar, DatePeriod, DateType, EntityRelationshipType, EntityType, Language, NameType, Script
from eats.forms.admin import AuthorityForm, CalendarForm, DatePeriodForm, DateTypeForm, EntityRelationshipForm, EntityTypeForm, LanguageForm, NameTypeForm, ScriptForm


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
    return render_to_response('eats/admin/panel.html', context_data,
                              context_instance=RequestContext(request))

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
    return render_to_response('eats/admin/topic_list.html', context_data,
                              context_instance=RequestContext(request))

@add_topic_map
def topic_add (request, topic_map, model):
    form_class = get_form_class(model)
    opts = model._meta
    if request.method == 'POST':
        form = form_class(topic_map, request.POST)
        if form.is_valid():
            topic = form.save()
            redirect_url = get_redirect_url(form, opts, topic)
            return HttpResponseRedirect(redirect_url)
    else:
        form = form_class(topic_map)
    context_data = {'form': form, 'opts': opts}
    return render_to_response('eats/admin/topic_add.html', context_data,
                              context_instance=RequestContext(request))

@add_topic_map
def topic_change (request, topic_map, topic_id, model):
    try:
        topic = model.objects.get_by_identifier(topic_id)
    except model.DoesNotExist:
        raise Http404
    opts = model._meta
    form_class = get_form_class(model)
    if request.method == 'POST':
        form = form_class(topic_map, request.POST, instance=topic)
        if form.is_valid():
            form.save()
            redirect_url = get_redirect_url(form, opts, topic)
            return HttpResponseRedirect(redirect_url)
    else:
        form = form_class(topic_map, instance=topic)
    context_data = {'form': form, 'opts': opts}
    return render_to_response('eats/admin/topic_change.html', context_data,
                              context_instance=RequestContext(request))

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
    elif model == NameType:
        form_class = NameTypeForm
    elif model == Script:
        form_class = ScriptForm
    return form_class

def get_redirect_url (form, opts, topic):
    object_type = opts.module_name
    redirect_url = reverse(object_type + '-list')
    if '_addanother' in form.data:
        redirect_url = reverse(object_type + '-add')
    elif '_continue' in form.data:
        redirect_url = reverse(object_type + '-change',
                               kwargs={'topic_id': topic.get_id()})
    return redirect_url
