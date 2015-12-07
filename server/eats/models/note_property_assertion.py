from django.db.models import Q

from .base_manager import BaseManager
from .note import Note
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


class NotePropertyAssertion (Note, PropertyAssertion):

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
