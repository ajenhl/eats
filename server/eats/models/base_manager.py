from django.conf import settings
from django.db import models

from eats_topic_map import EATSTopicMap


class BaseManager (models.Manager):

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            self._eats_topic_map = EATSTopicMap.objects.get(
                iri=settings.EATS_TOPIC_MAP)
        return self._eats_topic_map

