from django.shortcuts import render_to_response

from eats.decorators import add_topic_map


@add_topic_map
def create_entity (request, tm):
    """Creates a new entity with an existence assertion, using details
    from the logged in user's defaults. On successful creation,
    redirects to the edit page for the new entity."""
    context_data = {'error_heading': 'Not an error'}
    return render_to_response('eats/error.html', context_data)
