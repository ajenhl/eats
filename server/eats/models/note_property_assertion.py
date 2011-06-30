from tmapi.models import Occurrence

from base_manager import BaseManager
from property_assertion import PropertyAssertion
import logging
logger = logging.getLogger(__name__)

class NotePropertyAssertionManager (BaseManager):

    def get_by_identifier (self, identifier):
        return self.get(identifier__pk=identifier)
    
    def get_query_set (self):
        logger.debug('get_query_set')
        assertion_type = self.eats_topic_map.note_assertion_type
        qs = super(NotePropertyAssertionManager, self).get_query_set()
        return qs.filter(type=assertion_type)


class NotePropertyAssertion (Occurrence, PropertyAssertion):

    objects = NotePropertyAssertionManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def entity (self):
        """Returns the entity making this property assertion.

        :rtype: `Entity`

        """
        if not hasattr(self, '_entity'):
            from entity import Entity
            self._entity = self.get_parent(proxy=Entity)
        return self._entity
        
    @property
    def note (self):
        """Returns the textual content of the asserted note.

        :rtype: unicode string

        """
        return self.get_value()
        
    def update (self, authority, note):
        """Updates this property assertion.

        :param authority: authority making the assertion
        :type authority: `Topic`
        :param note: note text
        :type note: unicode string

        """
        super(NotePropertyAssertion, self).update(authority)
        if self.get_value() != note:
            self.set_value(note)
