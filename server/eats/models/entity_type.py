from tmapi.models import Topic

from .infrastructure import Infrastructure
from .infrastructure_manager import InfrastructureManager


class EntityTypeManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_entity_type_association_type
        return super(EntityTypeManager, self).filter_by_authority(
            authority, association_type)

    def filter_by_used_by_authority (self):
        association_type = self.eats_topic_map.authority_has_entity_type_association_type
        return super(EntityTypeManager, self).filter_by_used_by_authority(
            association_type)

    def get_queryset (self):
        return super(EntityTypeManager, self).get_queryset().filter(
            types=self.eats_topic_map.entity_type_type)


class EntityType (Infrastructure, Topic):

    objects = EntityTypeManager()

    class Meta:
        proxy = True
        app_label = 'eats'
