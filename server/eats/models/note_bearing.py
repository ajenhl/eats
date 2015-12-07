from django.db.models import Q

from .note import Note


class NoteBearing:

    """Class representing those objects that can have notes associated
    with them.

    This does not include `NotePropertyAssertion`s.

    """

    def create_note (self, note, is_internal, reifier=None):
        """Creates and returns a new note associated with this object.

        :param note: text of note
        :type note: `str`
        :param is_internal: if the note is for internal use only
        :type is_internal: `bool`
        :param reifier: reifier of object bearing notes
        :type reifier: `Topic`
        :rtype: `Note`

        """
        if reifier is None:
            reifier = self
        scope = []
        if is_internal:
            scope.append(self.eats_topic_map.is_note_internal)
        note = reifier.create_occurrence(self.eats_topic_map.note_type,
                                         note, scope=scope, proxy=Note)
        return note

    def get_note (self, user, note_id, authority=None, reifier=None):
        """Returns the note specified by `note_id`, filtered by the permission
        of `user` (to exclude internal notes). If there is no such
        note, or the note is not associated with this note bearing
        object, returns None.

        :param user: user requesting the notes
        :type user: `EATSUser`
        :param note_id: id of the requested note
        :type note_id: `int`
        :param authority: authority associated with this object
        :type authority: `Authority`
        :param reifier: reifier of object bearing notes
        :type reifier: `Topic`
        :rtype: `Note` or None

        """
        try:
            note = Note.objects.get_by_identifier(note_id)
        except Note.DoesNotExist:
            return None
        if reifier is None:
            reifier = self
        if note.get_parent() != reifier:
            return None
        if authority is None:
            authority = self.property_assertion.authority
        if note.is_internal and (user is None or authority not in
                                 user.editable_authorities.all()):
            return None
        return note

    def get_notes (self, user, authority=None, reifier=None):

        """Returns the `Note`s associated with this object, filtered by the
        permission of `user` (to exclude internal notes).

        :param user: user requesting the notes
        :type user: `EATSUser`
        :param authority: authority associated with this object
        :type authority: `Authority`
        :param reifier: reifier of object bearing notes
        :type reifier: `Topic`
        :rtype: `QuerySet` of `Note`s

        """
        if reifier is None:
            reifier = self
        if authority is None:
            authority = self.property_assertion.authority
        include_internal = False
        if user is not None and authority in user.editable_authorities.all():
            include_internal = True
        note_type = self.eats_topic_map.note_type
        notes = reifier.get_occurrences(occurrence_type=note_type, proxy=Note)
        internal_q = Q(scope=self.eats_topic_map.is_note_internal)
        if not include_internal:
            notes = notes.exclude(internal_q)
        return notes
