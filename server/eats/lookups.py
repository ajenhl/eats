from selectable.base import LookupBase
from selectable.registry import registry

from eats.decorators import add_topic_map


class EntityLookup (LookupBase):

    @add_topic_map
    def get_query (self, topic_map, request, term):
        return topic_map.lookup_entities(term)

    def get_item_id (self, item):
        return item.get_id()
    
    def get_item_label (self, item):
        name_assertion = item.get_eats_names()[0]
        name = item.get_entity_name(name_assertion)
        return name.name_value

    def get_item_value (self, item):
        name_assertion = item.get_eats_names()[0]
        name = item.get_entity_name(name_assertion)
        return name.name_value

registry.register(EntityLookup)
