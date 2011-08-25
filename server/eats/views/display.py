from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from eats.decorators import add_topic_map
from eats.forms.display import EntitySearchForm
from eats.models import EATSUser, Entity


def entity_view (request, entity_id):
    try:
        entity = Entity.objects.get_by_identifier(entity_id)
    except Entity.DoesNotExist:
        raise Http404
    user_preferences = get_user_preferences(request)
    preferred_authority = user_preferences['preferred_authority']
    preferred_language = user_preferences['preferred_language']
    preferred_script = user_preferences['preferred_script']
    preferred_name = entity.get_preferred_name(
        authority=preferred_authority, language=preferred_language,
        script=preferred_script).name
    existence_dates = entity.get_existence_dates()
    entity_type_pas = entity.get_entity_types()
    name_pas = entity.get_eats_names()
    relationship_pas = entity.get_entity_relationships()
    note_pas = entity.get_notes()
    context_data = {'entity': entity,
                    'preferred_authority': preferred_authority,
                    'preferred_language': preferred_language,
                    'preferred_name': preferred_name,
                    'preferred_script': preferred_script,
                    'existence_dates': existence_dates,
                    'entity_type_pas': entity_type_pas, 'name_pas': name_pas,
                    'note_pas': note_pas, 'relationship_pas': relationship_pas}
    return render_to_response('eats/display/entity.html', context_data,
                              context_instance=RequestContext(request))

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
    except (AttributeError, EATSUser.DoesNotExist):
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
