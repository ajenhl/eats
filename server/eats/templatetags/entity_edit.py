"""Tag library for editing an entity."""

from django import template


register = template.Library()

@register.inclusion_tag('eats/edit/entity_relationship_non_editable.html',
                        takes_context=True)
def display_entity_relationship_non_editable (context, entity,
                                              entity_relationship):
    """Returns a context dictionary for rendering the template
    displaying `entity_relationship` as a non-editable property
    assertion.

    :param context: the context of the calling template
    :type context: `dict`
    :param entity: the entity being displayed
    :type entity: `Entity`
    :param entity_relationship: the entity relationship to display
    :type entity_relationship: `EntityRelationshipPropertyAssertion`

    """
    # QAZ: This is almost exactly the same code as in
    # entity_display.py.
    authority_name = entity_relationship.authority.get_admin_name()
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
    return {'authority_name': authority_name,
            'other_entity_id': other_entity_id,
            'other_entity_name': other_entity_name.name.assembled_form,
            'relationship_type_name': relationship_type_name}
