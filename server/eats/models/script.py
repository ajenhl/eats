from tmapi.models import Topic

from infrastructure import Infrastructure
from infrastructure_manager import InfrastructureManager


class ScriptManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_script_association_type
        return super(ScriptManager, self).filter_by_authority(
            authority, association_type)

    def get_by_code (self, code):
        for script in self.all():
            if code == script.get_code():
                return script
        else:
            raise self.model.DoesNotExist
    
    def get_query_set (self):
        return super(ScriptManager, self).get_query_set().filter(
            types=self.eats_topic_map.script_type)


class Script (Topic, Infrastructure):

    objects = ScriptManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'

    def get_code (self):
        name = self.get_names(self.eats_topic_map.script_code_type)[0]
        return name.get_value()

    def set_code (self, code):
        if code == self.get_code():
            return
        try:
            self._default_manager.get_by_code(code)
            # QAZ: Raise a specific exception with error message.
            raise Exception
        except self.DoesNotExist:
            pass
        name = self.get_names(self.eats_topic_map.script_code_type)[0]
        name.set_value(code)
