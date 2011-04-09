from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from eats.lib.property_assertions import EntityTypePropertyAssertions, ExistencePropertyAssertions
from eats.constants import AUTHORITY_TYPE_IRI
from eats.decorators import add_topic_map
from eats.forms.edit import CreateEntityForm, create_choice_list


@add_topic_map
def entity_add (request, topic_map):
    # QAZ: this needs to change to provide only the authorities
    # available to the user. This whole view needs to be restricted to
    # logged in users who can create new entities.
    authorities = topic_map.get_authorities()
    if request.method == 'POST':
        form = CreateEntityForm(topic_map, authorities, request.POST)
        if form.is_valid():
            authority_id = form.cleaned_data['authority']
            authority = topic_map.get_topic_by_id(authority_id,
                                                  AUTHORITY_TYPE_IRI)
            entity = topic_map.create_entity(authority)
            redirect_url = reverse('entity-change',
                                   kwargs={'entity_id': entity.get_id()})
            return HttpResponseRedirect(redirect_url)
    else:
        form = CreateEntityForm(topic_map, authorities)
    context_data = {'form': form}
    return render_to_response('eats/edit/entity_add.html', context_data,
                              context_instance=RequestContext(request))

@add_topic_map
def entity_change (request, topic_map, entity_id):
    entity = topic_map.get_entity(entity_id)
    if entity is None:
        raise Http404
    context_data = {'entity': entity}
    # QAZ: this needs to change to provide only the authorities
    # available to the user. This whole view needs to be restricted to
    # logged in users who can edit entities.
    authorities = topic_map.get_authorities()
    authority_choices = create_choice_list(topic_map, authorities)
    post_data = request.POST or None
    existences = ExistencePropertyAssertions(topic_map, entity, authorities,
                                             authority_choices, post_data)
    context_data['existence_non_editable'] = existences.non_editable
    context_data['existence_formset'] = existences.formset
    entity_types = EntityTypePropertyAssertions(topic_map, entity, authorities,
                                                authority_choices, post_data)
    context_data['entity_type_non_editable'] = entity_types.non_editable
    context_data['entity_type_formset'] = entity_types.formset
    # Create the lists of assertions, both editable (forms) and not.
    return render_to_response('eats/edit/entity_change.html', context_data,
                              context_instance=RequestContext(request))

