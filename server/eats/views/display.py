from django.shortcuts import render_to_response
from django.template import RequestContext

from eats.decorators import add_topic_map
from eats.forms.display import EntitySearchForm
from eats.models import EATSUser


def entity_view (request):
    pass

def get_user_preferences (request):
    """Returns a dictionary of user preferences derived from `request`.

    :rtype: dictionary

    """
    preferences = {'preferred_authority': None,
                   'preferred_language': None,
                   'preferred_script': None}
    try:
        eats_user = request.user.eats_user
        preferences['preferred_authority'] = eats_user.get_authority()
        preferences['preferred_language'] = eats_user.get_language()
        preferences['preferred_script'] = eats_user.get_script()
    except EATSUser.DoesNotExist:
        pass
    return preferences

@add_topic_map
def search (request, topic_map):
    form_data = request.GET or None
    form = EntitySearchForm(data=form_data)
    results = []
    user_preferences = {}
    if form.is_valid():
        name = form.cleaned_data['name']
        results = topic_map.lookup_entities(name)
        user_preferences = get_user_preferences(request)
    context_data = {'search_form': form, 'search_results': results}
    context_data.update(user_preferences)
    return render_to_response('eats/display/search.html', context_data,
                              context_instance=RequestContext(request))
