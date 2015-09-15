from .base_manager import BaseManager


class InfrastructureManager (BaseManager):

    def filter_by_authority (self, authority, association_type):
        infrastructure_role_type = self.eats_topic_map.infrastructure_role_type
        authority_role_type = self.eats_topic_map.authority_role_type
        return self.filter(
            roles__type=infrastructure_role_type,
            roles__association__type=association_type,
            roles__association__roles__type=authority_role_type,
            roles__association__roles__player=authority)

    def get_by_admin_name (self, name):
        for model_object in self.all():
            if name == model_object.get_admin_name():
                return model_object
        else:
            raise self.model.DoesNotExist
