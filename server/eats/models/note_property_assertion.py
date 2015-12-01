from django.db.models import Q

from tmapi.models import Occurrence

from .base_manager import BaseManager
from .property_assertion import PropertyAssertion


class NotePropertyAssertionManager (BaseManager):

    def filter_by_entity (self, entity, user=None):
        qs = self.filter_by_entity_all(entity)
        internal_q = Q(scope=self.eats_topic_map.is_note_internal)
        if user is not None:
            authority_q = Q(scope__in=user.editable_authorities.all())
            qs = qs.exclude(internal_q & ~authority_q)
        else:
            qs = qs.exclude(internal_q)
        return qs

    def filter_by_entity_all (self, entity):
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
    def is_internal (self):
        """Returns True if this note is internal."""
        return self.eats_topic_map.is_note_internal in self.get_scope()

    @is_internal.setter
    def is_internal (self, is_internal):
        """Sets whether this note is internal."""
        if is_internal:
            self.add_theme(self.eats_topic_map.is_note_internal)
        else:
            self.remove_theme(self.eats_topic_map.is_note_internal)

    @property
    def note (self):
        """Returns the textual content of the asserted note.

        :rtype: `str`

        """
        return self.get_value()

    def update (self, note, is_internal):
        """Updates this property assertion.

        :param note: note text
        :type note: `str`
        :param is_internal: if the note is internal
        :type is_internal: `bool`

        """
        if self.get_value() != note:
            self.set_value(note)
        self.is_internal = is_internal
