from django.http import Http404

from eats.constants import UNNAMED_ENTITY_NAME
from eats.models import Entity


def get_entity_assertion (request, entity_id, assertion_id):
    entity = get_topic_or_404(Entity, entity_id)
    # Note that entity.get_assertion only gets Association assertions,
    # which happens to be what is wanted when restricting assertions
    # to those that can carry dates or notes.
    assertion = entity.get_assertion(assertion_id)
    if assertion is None:
        raise Http404
    authority = assertion.authority
    if authority != request.user.eats_user.get_current_authority():
        raise Http404
    return entity, assertion, authority

def get_preferred_name (user_preferences, entity):
    preferred_name_assertion = entity.get_preferred_name(
        user_preferences['preferred_authority'],
        user_preferences['preferred_language'],
        user_preferences['preferred_script'])
    if preferred_name_assertion:
        preferred_name = preferred_name_assertion.name.assembled_form
    else:
        preferred_name = UNNAMED_ENTITY_NAME
    return preferred_name

def get_topic_or_404 (model, topic_id):
    try:
        topic = model.objects.get_by_identifier(topic_id)
    except model.DoesNotExist:
        raise Http404
    return topic
