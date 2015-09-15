from tmapi.models import Topic

from .infrastructure import Infrastructure
from .infrastructure_manager import InfrastructureManager


class NameTypeManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_name_type_association_type
        return super(NameTypeManager, self).filter_by_authority(
            authority, association_type)

    def get_queryset (self):
        return super(NameTypeManager, self).get_queryset().filter(
            types=self.eats_topic_map.name_type_type)


class NameType (Topic, Infrastructure):

    objects = NameTypeManager()

    class Meta:
        proxy = True
        app_label = 'eats'
