from tmapi.models import Association

from property_assertion import PropertyAssertion


class ExistencePropertyAssertion (Association, PropertyAssertion):

    class Meta:
        proxy = True
        app_label = 'eats'

    def set_players (self, entity):
        """Sets the entity involved in this property assertion.

        :param entity: the entity
        :type entity: `Entity`

        """
        if hasattr(self, '_entity'):
            raise Exception(
                'set_players may be called only once for a property assertion')
        self.create_role(self.eats_topic_map.property_role_type,
                         self.eats_topic_map.existence)
        self.create_role(self.eats_topic_map.entity_role_type, entity)
        self._entity = entity

    def update (self, authority):
        """Updates this property assertion.

        :param authority: authority making the assertion
        :type authority: `Topic`

        """
        super(ExistencePropertyAssertion, self).update(authority)
