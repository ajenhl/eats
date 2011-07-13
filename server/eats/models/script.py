from tmapi.models import Topic

from infrastructure import Infrastructure
from infrastructure_manager import InfrastructureManager


class ScriptManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_script_association_type
        return super(ScriptManager, self).filter_by_authority(
            authority, association_type)
    
    def get_query_set (self):
        return super(ScriptManager, self).get_query_set().filter(
            types=self.eats_topic_map.script_type)


class Script (Topic, Infrastructure):

    objects = ScriptManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'
