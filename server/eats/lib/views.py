from django.http import Http404


def get_topic_or_404 (model, topic_id):
    try:
        topic = model.objects.get_by_identifier(topic_id)
    except model.DoesNotExist:
        raise Http404
    return topic

