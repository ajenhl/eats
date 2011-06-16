from tmapi.models import Association

from name import Name
from property_assertion import PropertyAssertion


class NamePropertyAssertion (Association, PropertyAssertion):

    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def name (self):
        """Returns the name being asserted."""
        if not hasattr(self, '_name'):
            property_role = self.get_roles(
                self.eats_topic_map.property_role_type)[0]
            self._name = property_role.get_player(proxy=Name)
        return self._name

    def remove (self):
        """Deletes this property assertion."""
        self.name.remove()
        super(NamePropertyAssertion, self).remove()
        
    def set_players (self, entity, name):
        """Sets the entity and name involved in this property assertion.

        :param entity: the entity
        :type entity: `Entity`
        :param name: the name
        :type name: `Name`

        """
        if hasattr(self, '_entity') or hasattr(self, '_name'):
            raise Exception(
                'set_players may be called only once for a property assertion')
        self.create_role(self.eats_topic_map.property_role_type, name)
        self._name = name
        self.create_role(self.eats_topic_map.entity_role_type, entity)
        self._entity = entity
        name.entity = entity
        
    def update (self, authority, name_type, language, script, display_form):
        """Update this property assertion, and its associated name.

        :param authority: authority making the assertion
        :type authority: `Topic`
        :param name_type: type of the name
        :type name_type: `Topic`
        :param language: language of the name
        :type language: `Topic`
        :param script: script of the name
        :type script: `Topic`
        :param display_form: display form of the name
        :type display_form: unicode string

        """
        super(NamePropertyAssertion, self).update(authority)
        self.name.update(name_type, language, script, display_form)
