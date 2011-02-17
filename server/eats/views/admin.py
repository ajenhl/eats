from urlparse import urljoin

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from tmapi.exceptions import TopicMapExistsException
from tmapi.models import TopicMap, TopicMapSystemFactory

from eats.api.authority import get_authority_admin_name
from eats.api.topic_map import create_authority, get_authorities, get_authority
from eats.decorators import add_topic_map
from eats.forms.admin import AuthorityForm


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
def authority_list (request, topic_map):
    authorities = [(authority, get_authority_admin_name(topic_map, authority))
                   for authority in get_authorities(topic_map)]
    context_data = {'authorities': authorities}
    return render_to_response('eats/admin/authority_list.html', context_data,
                              context_instance=RequestContext(request))

@add_topic_map
def authority_add (request, topic_map):
    if request.method == 'POST':
        form = AuthorityForm(topic_map, None, request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            authority = create_authority(topic_map, name)
            redirect_url = reverse('authority-list')
            if '_addanother' in form.data:
                redirect_url = reverse('authority-add')
            elif '_continue' in form.data:
                redirect_url = reverse(
                    'authority-change', kwargs={
                        'authority_id': authority.identifier.id})
            return HttpResponseRedirect(redirect_url)
    else:
        form = AuthorityForm(topic_map, None)
    context_data = {'form': form}
    return render_to_response('eats/admin/authority_add.html', context_data,
                              context_instance=RequestContext(request))

@add_topic_map
def authority_change (request, topic_map, authority_id):
    authority = get_authority(topic_map, authority_id)
    if authority is None:
        raise Http404
    if request.method == 'POST':
        form = AuthorityForm(topic_map, authority_id, request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            get_authority_admin_name(topic_map, authority).set_value(name)
            redirect_url = reverse('authority-list')
            if '_addanother' in form.data:
                redirect_url = reverse('authority-add')
            elif '_continue' in form.data:
                redirect_url = reverse(
                    'authority-change', kwargs={
                        'authority_id': authority_id})
            return HttpResponseRedirect(redirect_url)
    else:
        data = {'name': get_authority_admin_name(topic_map, authority)}
        form = AuthorityForm(topic_map, authority_id, data)
    context_data = {'form': form}
    return render_to_response('eats/admin/authority_change.html', context_data,
                              context_instance=RequestContext(request))
