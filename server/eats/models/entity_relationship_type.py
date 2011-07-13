from tmapi.models import Topic

from infrastructure import Infrastructure
from infrastructure_manager import InfrastructureManager


class EntityRelationshipTypeManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_entity_relationship_type_association_type
        return super(EntityRelationshipTypeManager, self).filter_by_authority(
            authority, association_type)
    
    def get_query_set (self):
        return super(EntityRelationshipTypeManager, self).get_query_set().filter(
            types=self.eats_topic_map.entity_relationship_type_type)


class EntityRelationshipType (Topic, Infrastructure):

    objects = EntityRelationshipTypeManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'

    def get_admin_name (self):
        forward = self.get_names(self.eats_topic_map.relationship_name_type)[0]
        reverse = self.get_names(
            self.eats_topic_map.reverse_relationship_name_type)[0]
        return u'%s / %s' % (forward, reverse)
