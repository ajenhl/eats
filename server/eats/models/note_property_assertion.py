from tmapi.models import Occurrence

from property_assertion import PropertyAssertion


class NotePropertyAssertion (Occurrence, PropertyAssertion):

    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def note (self):
        """Returns the textual content of the asserted note."""
        return self.get_value()
        
    def update (self, authority, note):
        """Update this property assertion.

        :param authority: authority making the assertion
        :type authority: `Topic`
        :param note: note text
        :type note: unicode string

        """
        super(NotePropertyAssertion, self).update(authority)
        if self.get_value() != note:
            self.set_value(note)
