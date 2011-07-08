from tmapi.models import Topic

from infrastructure_manager import InfrastructureManager


class EntityRelationshipTypeManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_entity_relationship_type_association_type
        return super(EntityRelationshipTypeManager, self).filter_by_authority(
            authority, association_type)
    
    def get_query_set (self):
        return super(EntityRelationshipTypeManager, self).get_query_set().filter(
            types=self.eats_topic_map.entity_relationship_type_type)


class EntityRelationshipType (Topic):

    objects = EntityRelationshipTypeManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'
