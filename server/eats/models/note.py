from tmapi.models import Occurrence

from .base_manager import BaseManager


class NoteManager (BaseManager):

    pass


class Note (Occurrence):

    objects = NoteManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from .eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map

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
        """Updates this note.

        :param note: note text
        :type note: `str`
        :param is_internal: if the note is internal
        :type is_internal: `bool`

        """
        if self.get_value() != note:
            self.set_value(note)
        self.is_internal = is_internal
