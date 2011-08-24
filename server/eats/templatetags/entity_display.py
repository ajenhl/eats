"""Tag library for displaying an entity according to user
preferences."""

from django import template


register = template.Library()


@register.inclusion_tag('eats/display/entity_search_result.html',
                        takes_context=True)
def display_entity_search_result (context, entity):
    """Returns a dictionary to be the context for rendering the
    template displaying `entity` in a search result context.

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
