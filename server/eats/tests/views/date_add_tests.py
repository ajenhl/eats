from django.core.urlresolvers import reverse

from eats.tests.base_test_case import BaseTestCase


class DateAddViewTestCase (BaseTestCase):

    def test_non_matching_date_add (self):
        """Tests that the entity, assertion, and assertion type all
        match when adding a date."""
        response = self.client.get(reverse(
                'date-add', kwargs={'entity_id': 0, 'assertion_id': 0}))
        self.assertEqual(
            response.status_code, 404,
            'Expected a 404 HTTP response code for a non-existent entity')
        entity = self.tm.create_entity(self.authority)
        response = self.client.get(reverse(
                'date-add', kwargs={'entity_id': entity.get_id(),
                                    'assertion_id': entity.get_id()}))
        self.assertEqual(
            response.status_code, 404,
            'Expected a 404 HTTP response code for a non-existent assertion')

    def test_get_request (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        response = self.client.get(reverse(
                'date-add', kwargs={'entity_id': entity.get_id(),
                                    'assertion_id': existence.get_id()}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/date_add.html')
        form = response.context['form']
        
