from django.conf import settings
from django.shortcuts import render_to_response

from eats.models import EATSTopicMap


def add_topic_map (fn):
    """Decorator that calls the decorated function with the EATS topic
    map as an argument, or else returns an appropriate error response.

    :param fn: Function to be decorated
    :type fn: function
    :rtype: function
    
    """
    def wrapper (request, *args, **kwargs):
        try:
            tm = EATSTopicMap.objects.get(iri=settings.EATS_TOPIC_MAP)
        except AttributeError:
            # The EATS_TOPIC_MAP setting is not set.
            context_data = {'error_heading': 'EATS configuration error',
                            'error_text': 'The EATS_TOPIC_MAP setting must be set before EATS can be used.'}
            return render_to_response('eats/error.html', context_data)
        except EATSTopicMap.DoesNotExist:
            context_data = {'error_heading': 'EATS database error',
                            'error_text': 'No topic map matching the EATS_TOPIC_MAP setting URI exists.'}
            return render_to_response('eats/error.html', context_data)
        return fn(request, tm, *args, **kwargs)
    return wrapper

