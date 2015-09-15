from tmapi.models import Occurrence

from .base_manager import BaseManager
from .property_assertion import PropertyAssertion


class NotePropertyAssertionManager (BaseManager):

    def filter_by_entity (self, entity):
        return self.filter(topic=entity)

    def get_queryset (self):
        assertion_type = self.eats_topic_map.note_assertion_type
        qs = super(NotePropertyAssertionManager, self).get_queryset()
        return qs.filter(type=assertion_type)


class NotePropertyAssertion (Occurrence, PropertyAssertion):

    objects = NotePropertyAssertionManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    def entity (self):
        """Returns the entity making this property assertion.

        :rtype: `Entity`

        """
        if not hasattr(self, '_entity'):
            from .entity import Entity
            self._entity = self.get_parent(proxy=Entity)
        return self._entity

    @property
    def note (self):
        """Returns the textual content of the asserted note.

        :rtype: `str`

        """
        return self.get_value()

    def update (self, note):
        """Updates this property assertion.

        :param note: note text
        :type note: `str`

        """
        if self.get_value() != note:
            self.set_value(note)
