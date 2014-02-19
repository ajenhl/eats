from django.core.urlresolvers import reverse

from eats.constants import UNNAMED_ENTITY_NAME
from eats.tests.views.view_test_case import ViewTestCase


class EntityDisplayViewTestCase (ViewTestCase):

    def setUp (self):
        super(EntityDisplayViewTestCase, self).setUp()
        self.entity = self.tm.create_entity(self.authority)
        self.url = reverse('entity-view',
                           kwargs={'entity_id': self.entity.get_id()})

    def test_no_entity_name (self):
        response = self.app.get(self.url)
        self.assertContains(response, UNNAMED_ENTITY_NAME, count=2)

    def test_no_related_entity_name (self):
        entity_relationship_type = self.create_entity_relationship_type(
            'is parent of', 'is child of')
        self.authority.set_entity_relationship_types([entity_relationship_type])
        entity2 = self.tm.create_entity(self.authority)
        self.entity.create_entity_relationship_property_assertion(
            self.authority, entity_relationship_type, self.entity, entity2,
            self.tm.property_assertion_full_certainty)
        response = self.app.get(self.url)
        # Both the entity being display and the related entity have no
        # name.
        self.assertContains(response, UNNAMED_ENTITY_NAME, count=3)

    def test_entity_relationship (self):
        entity_relationship_type = self.create_entity_relationship_type(
            'is parent of', 'is child of')
        self.authority.set_entity_relationship_types([entity_relationship_type])
        entity2 = self.tm.create_entity(self.authority)
        assertion = self.entity.create_entity_relationship_property_assertion(
            self.authority, entity_relationship_type, self.entity, entity2,
            self.tm.property_assertion_no_certainty)
        response = self.app.get(self.url)
        self.assertTrue(assertion in response.context['relationship_pas'])
        self.assertContains(response, 'is parent of', count=1)
        self.assertContains(response, '(uncertain)', count=1)
