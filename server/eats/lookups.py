from selectable.base import LookupBase
from selectable.registry import registry

from eats.decorators import add_topic_map


class EntityLookup (LookupBase):

    @add_topic_map
    def get_query (self, topic_map, request, term):
        return topic_map.lookup_entities(term)

    @add_topic_map
    def get_item (self, topic_map, value):
        return topic_map.get_entity(value)
    
    def get_item_id (self, item):
        return item.get_id()
    
    def get_item_label (self, item):
        try:
            name_assertion = item.get_eats_names()[0]
            label = name_assertion.name.display_form
        except IndexError:
            label = '[unnamed entity]'
        return label

    def get_item_value (self, item):
        try:
            name_assertion = item.get_eats_names()[0]
            label = name_assertion.name.display_form
        except IndexError:
            label = '[unnamed entity]'
        return label

registry.register(EntityLookup)
