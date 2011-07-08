from base_manager import BaseManager


class InfrastructureManager (BaseManager):

    def filter_by_authority (self, authority, association_type):
        infrastructure_role_type = self.eats_topic_map.infrastructure_role_type
        authority_role_type = self.eats_topic_map.authority_role_type
        return self.filter(
            role_players__type=infrastructure_role_type,
            role_players__association__type=association_type,
            role_players__association__roles__type=authority_role_type,
            role_players__association__roles__player=authority)
