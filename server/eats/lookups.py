from selectable.base import LookupBase
from selectable.registry import registry

from eats.constants import UNNAMED_ENTITY_NAME
from eats.decorators import add_topic_map
from eats.models import Entity


class EntityLookup (LookupBase):

    @add_topic_map
    def get_query (self, topic_map, request, term):
        return topic_map.lookup_entities(term)

    def get_item (self, value):
        return Entity.objects.get_by_identifier(value)

    def get_item_id (self, item):
        return item.get_id()

    def get_item_label (self, item):
        try:
            name_assertion = item.get_eats_names()[0]
            label = name_assertion.name.assembled_form
        except IndexError:
            label = UNNAMED_ENTITY_NAME
        return label

    def get_item_value (self, item):
        try:
            name_assertion = item.get_eats_names()[0]
            label = name_assertion.name.assembled_form
        except IndexError:
            label = UNNAMED_ENTITY_NAME
        return label

registry.register(EntityLookup)
