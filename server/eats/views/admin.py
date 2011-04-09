from urlparse import urljoin

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from tmapi.exceptions import TopicMapExistsException
from tmapi.models import TopicMap, TopicMapSystemFactory

from eats.decorators import add_topic_map
from eats.forms.admin import AuthorityForm, LanguageForm, ScriptForm


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
def topic_list (request, topic_map, type_iri, name):
    topics = topic_map.get_topics_by_type(type_iri)
    topics_data = [(topic, topic_map.get_admin_name(topic))
                   for topic in topics]
    context_data = {'topics': topics_data, 'name': name}
    return render_to_response('eats/admin/topic_list.html', context_data,
                              context_instance=RequestContext(request))

@add_topic_map
def topic_add (request, topic_map, type_iri, name):
    form_class = get_form_class(name)
    if request.method == 'POST':
        form = form_class(topic_map, None, request.POST)
        if form.is_valid():
            topic = topic_map.create_typed_topic(type_iri, form.cleaned_data)
            redirect_url = get_redirect_url(form, name, topic.identifier.id)
            return HttpResponseRedirect(redirect_url)
    else:
        form = form_class(topic_map, None)
    context_data = {'form': form, 'name': name}
    return render_to_response('eats/admin/topic_add.html', context_data,
                              context_instance=RequestContext(request))

@add_topic_map
def topic_change (request, topic_map, topic_id, type_iri, name):
    topic = topic_map.get_topic_by_id(topic_id, type_iri)
    if topic is None:
        raise Http404
    form_class = get_form_class(name)
    if request.method == 'POST':
        form = form_class(topic_map, topic_id, request.POST)
        if form.is_valid():
            topic_map.update_topic_by_type(topic, type_iri, form.cleaned_data)
            redirect_url = get_redirect_url(form, name, topic_id)
            return HttpResponseRedirect(redirect_url)
    else:
        data = topic_map.get_topic_data(topic, type_iri)
        form = form_class(topic_map, topic_id, data)
    context_data = {'form': form, 'name': name}
    return render_to_response('eats/admin/topic_change.html', context_data,
                              context_instance=RequestContext(request))

def get_form_class (name):
    """Returns the class of the admin form to use for `name` topics.

    :param name: name of topic type
    :type name: string
    :rtype: class

    """
    if name == 'authority':
        form_class = AuthorityForm
    elif name == 'language':
        form_class = LanguageForm
    elif name == 'script':
        form_class = ScriptForm
    return form_class

def get_redirect_url (form, object_type, identifier):
    redirect_url = reverse(object_type + '-list')
    if '_addanother' in form.data:
        redirect_url = reverse(object_type + '-add')
    elif '_continue' in form.data:
        redirect_url = reverse(object_type + '-change',
                               kwargs={'topic_id': identifier})
    return redirect_url
