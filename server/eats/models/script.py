from tmapi.models import Topic

from .infrastructure import Infrastructure
from .infrastructure_manager import InfrastructureManager


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

    def get_queryset (self):
        return super(ScriptManager, self).get_queryset().filter(
            types=self.eats_topic_map.script_type)


class Script (Topic, Infrastructure):

    objects = ScriptManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    def get_code (self):
        name = self.get_names(self.eats_topic_map.script_code_type)[0]
        return name.get_value()

    @property
    def separator (self):
        """Returns the this script's separator, to be used between name parts.

        :rtype: `str`

        """
        separator = ''
        separator_occurrences = self.get_occurrences(
            self.eats_topic_map.script_separator_type)
        if len(separator_occurrences) == 0:
            self.separator = separator
        else:
            separator = separator_occurrences[0].get_value()
        return separator

    @separator.setter
    def separator (self, separator):
        """Sets this script's separator, to be used between name parts.

        :param separator: separator
        :type separator: `str`

        """
        occurrence_type = self.eats_topic_map.script_separator_type
        try:
            separator_occurrence = self.get_occurrences(
                occurrence_type)[0]
            separator_occurrence.set_value(separator)
        except IndexError:
            self.create_occurrence(occurrence_type, separator)

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
