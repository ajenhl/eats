from tmapi.models import Topic

from .infrastructure import Infrastructure
from .infrastructure_manager import InfrastructureManager


class EntityRelationshipTypeManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_entity_relationship_type_association_type
        return super(EntityRelationshipTypeManager, self).filter_by_authority(
            authority, association_type)

    def get_by_admin_name (self, name, reverse_name):
        for ert in self.all():
            existing_name = ert.get_admin_forward_name()
            existing_reverse_name = ert.get_admin_reverse_name()
            if name == existing_name and reverse_name == existing_reverse_name:
                return ert
        else:
            raise self.model.DoesNotExist

    def get_queryset (self):
        return super(EntityRelationshipTypeManager, self).get_queryset().filter(
            types=self.eats_topic_map.entity_relationship_type_type)


class EntityRelationshipType (Topic, Infrastructure):

    objects = EntityRelationshipTypeManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    def get_admin_forward_name (self):
        name = self.get_names(self.eats_topic_map.relationship_name_type)[0]
        return name.get_value()

    def get_admin_name (self):
        forward = self.get_names(self.eats_topic_map.relationship_name_type)[0]
        reverse = self.get_names(
            self.eats_topic_map.reverse_relationship_name_type)[0]
        return '%s / %s' % (forward.get_value(), reverse.get_value())

    def get_admin_reverse_name (self):
        name = self.get_names(
            self.eats_topic_map.reverse_relationship_name_type)[0]
        return name.get_value()

    def set_admin_name (self, name, reverse_name):
        if name == self.get_admin_forward_name() and \
                reverse_name == self.get_admin_reverse_name():
            return
        try:
            EntityRelationshipType.objects.get_by_admin_name(name, reverse_name)
            # QAZ: Raise a specific exception with error message.
            raise Exception
        except self.DoesNotExist:
            pass
        self.get_names(self.eats_topic_map.relationship_name_type)[0].set_value(name)
        self.get_names(self.eats_topic_map.reverse_relationship_name_type)[0].set_value(reverse_name)
