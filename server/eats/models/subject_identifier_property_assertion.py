from tmapi.models import Locator, Occurrence

from .base_manager import BaseManager
from .property_assertion import PropertyAssertion


class SubjectIdentifierPropertyAssertionManager (BaseManager):

    def filter_by_entity (self, entity):
        return self.filter(topic=entity)

    def get_queryset (self):
        assertion_type = self.eats_topic_map.subject_identifier_assertion_type
        qs = super(SubjectIdentifierPropertyAssertionManager, self).get_queryset()
        return qs.filter(type=assertion_type)


class SubjectIdentifierPropertyAssertion (Occurrence, PropertyAssertion):

    objects = SubjectIdentifierPropertyAssertionManager()

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
    def subject_identifier (self):
        """Returns the textual content of the asserted subject_identifier.

        :rtype: `str`

        """
        return self.get_value()

    def update (self, subject_identifier):
        """Updates this property assertion.

        :param subject_identifier: subject_identifier URL
        :type subject_identifier: `str`

        """
        if self.get_value() != subject_identifier:
            self.set_value(subject_identifier,
                           Locator('http://www.w3.org/2001/XMLSchema#anyURI'))
