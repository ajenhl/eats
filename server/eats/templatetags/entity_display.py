"""Tag library for displaying an entity according to user
preferences."""

from django import template


register = template.Library()

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
    relationship_type = entity_relationship.entity_relationship_type
    if entity == domain_entity:
        relationship_type_name = relationship_type.get_admin_forward_name()
        other_entity = range_entity
    else:
        relationship_type_name = relationship_type.get_admin_reverse_name()
        other_entity = domain_entity
    other_entity_name = other_entity.get_preferred_name(
        authority=context['preferred_authority'],
        language=context['preferred_language'],
        script=context['preferred_script'])
    other_entity_id = other_entity.get_id()
    return {'other_entity_id': other_entity_id,
            'other_entity_name': other_entity_name.name,
            'relationship_type_name': relationship_type_name}

@register.inclusion_tag('eats/display/entity_search_result.html',
                        takes_context=True)
def display_entity_search_result (context, entity):
    """Returns a context dictionary for rendering the template
    displaying `entity` in a search result context.

    Requires that `context` contains the user preferences.
    
    """
    dates = entity.get_existence_dates()
    preferred_name = entity.get_preferred_name(context['preferred_authority'],
                                               context['preferred_language'],
                                               context['preferred_script'])
    other_names = entity.get_eats_names(exclude=preferred_name)
    notes = entity.get_notes()
    return {'dates': dates, 'entity': entity, 'notes': notes,
            'other_names': other_names,
            'preferred_name': preferred_name.name.assembled_form}

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
