from tmapi.models import Topic

from .infrastructure import Infrastructure
from .infrastructure_manager import InfrastructureManager


class NamePartTypeManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_name_part_type_association_type
        return super(NamePartTypeManager, self).filter_by_authority(
            authority, association_type)

    def get_queryset (self):
        return super(NamePartTypeManager, self).get_queryset().filter(
            types=self.eats_topic_map.name_part_type_type)


class NamePartType (Topic, Infrastructure):

    objects = NamePartTypeManager()

    class Meta:
        proxy = True
        app_label = 'eats'
