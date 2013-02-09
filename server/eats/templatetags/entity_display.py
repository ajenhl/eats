"""Tag library for displaying an entity according to user
preferences."""

from django import template

from eats.constants import UNNAMED_ENTITY_NAME


register = template.Library()


@register.inclusion_tag('eats/display/duplicate_subject_identifiers.html',
                        takes_context=True)
def display_duplicate_subject_identifiers (context, entity, subject_identifier,
                                           authority=None):
    duplicate_entities = entity.get_duplicate_subject_identifiers(
        subject_identifier, authority)
    duplicate_entity_data = {}
    preferred_authority = context['preferred_authority']
    preferred_language = context['preferred_language']
    preferred_script = context['preferred_script']
    for duplicate_entity in duplicate_entities:
        preferred_name = duplicate_entity.get_preferred_name(
            preferred_authority, preferred_language, preferred_script)
        try:
            preferred_name_form = preferred_name.name.assembled_form
        except AttributeError:
            preferred_name_form = UNNAMED_ENTITY_NAME
        duplicate_entity_data[duplicate_entity.get_id()] = preferred_name_form
    return {'duplicate_entity_data': duplicate_entity_data}

@register.inclusion_tag('eats/display/entity_relationship_property_assertion.html', takes_context=True)
def display_entity_relationship_property_assertion (context, entity,
                                                    entity_relationship):
    """Returns a context dictionary for rendering the template
    displaying `entity_relationship`.

    :param context: the context of the calling template
    :type context: `dict`
    :param entity: the entity being displayed
    :type entity: `Entity`
    :param entity_relationship: the entity relationship to display
    :type entity_relationship: `EntityRelationshipPropertyAssertion`

    """
    domain_entity = entity_relationship.domain_entity
    range_entity = entity_relationship.range_entity
    if entity == domain_entity:
        relationship_type_name = \
            entity_relationship.get_relationship_type_forward_name()
        other_entity = range_entity
    else:
        relationship_type_name = \
            entity_relationship.get_relationship_type_reverse_name()
        other_entity = domain_entity
    try:
        other_entity_name_form = other_entity.get_preferred_name(
            authority=context['preferred_authority'],
            language=context['preferred_language'],
            script=context['preferred_script']).name.assembled_form
    except AttributeError:
        other_entity_name_form = UNNAMED_ENTITY_NAME
    other_entity_id = other_entity.get_id()
    if entity_relationship.certainty == \
            context['property_assertion_full_certainty']:
        certainty = ''
    else:
        certainty = ' (uncertain)'
    return {'certainty': certainty, 'other_entity_id': other_entity_id,
            'other_entity_name_form': other_entity_name_form,
            'relationship_type_name': relationship_type_name}

@register.inclusion_tag('eats/display/entity_search_result.html',
                        takes_context=True)
def display_entity_search_result (context, entity):
    """Returns a context dictionary for rendering the template
    displaying `entity` in a search result context.

    Requires that `context` contains the user preferences.

    """
    dates = entity.get_existence_dates()
    preferred_authority = context['preferred_authority']
    preferred_language = context['preferred_language']
    preferred_script = context['preferred_script']
    preferred_name = entity.get_preferred_name(
        preferred_authority, preferred_language, preferred_script)
    other_names = entity.get_eats_names(exclude=preferred_name)
    try:
        preferred_name_form = preferred_name.name.assembled_form
    except AttributeError:
        preferred_name_form = UNNAMED_ENTITY_NAME
    other_name_values = set()
    for name in other_names:
        other_name_values.add(name.name.assembled_form)
    other_name_values = list(other_name_values)
    other_name_values.sort()
    entity_relationships = entity.get_entity_relationships()
    entity_types = entity.get_entity_types()
    entity_type_values = set()
    for entity_type in entity_types:
        entity_type_values.add(entity_type.entity_type.get_admin_name())
    notes = entity.get_notes()
    return {'dates': dates, 'entity': entity,
            'entity_relationships': entity_relationships,
            'entity_types': entity_type_values, 'notes': notes,
            'other_names': other_name_values,
            'preferred_authority': preferred_authority,
            'preferred_language': preferred_language,
            'preferred_name_form': preferred_name_form,
            'preferred_script': preferred_script,
            'property_assertion_full_certainty':
                context['property_assertion_full_certainty']}

@register.inclusion_tag('eats/display/name_metadata.html')
def display_name_metadata (name):
    """Returns a context dictionary for rendering the template
    displaying the metadata of `name`."""
    return {'language': name.language, 'name_type': name.name_type,
            'script': name.script}

@register.inclusion_tag('eats/display/property_assertion_authority.html')
def display_property_assertion_authority (property_assertion):
    """Returns a context dictionary for rendering the template
    displaying the authority of `property_assertion`."""
    return {'authority': property_assertion.authority}

@register.inclusion_tag('eats/display/property_assertion_dates.html')
def display_property_assertion_dates (property_assertion):
    """Returns a context dictionary for rendering the template
    displaying the dates of `property_assertion`."""
    return {'dates': property_assertion.get_dates()}
