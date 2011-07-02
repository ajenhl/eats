from django.core.urlresolvers import reverse

from eats.tests.base_test_case import BaseTestCase


class DateChangeViewTestCase (BaseTestCase):

    def setUp (self):
        super(DateChangeViewTestCase, self).setUp()
        self.date_period = self.create_date_period('lifespan')
    
    def test_non_matching_date_change (self):
        """Tests that the entity, assertion, and date match when
        editing a date."""
        # Test with none of entity, assertion and date existing.
        url_args = {'entity_id': 0, 'assertion_id': 0, 'date_id': 0}
        response = self.client.get(reverse('date-change', kwargs=url_args))
        self.assertEqual(
            response.status_code, 404,
            'Expected a 404 HTTP response code for a non-existent entity')
        # Test with only the entity existing.
        entity = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity.get_id()
        response = self.client.get(reverse('date-change', kwargs=url_args))
        self.assertEqual(
            response.status_code, 404,
            'Expected a 404 HTTP response code for a non-existent assertion')
        # Test with only the entity and assertion existing.
        assertion = entity.get_existences()[0]
        url_args['assertion_id'] = assertion.get_id()
        response = self.client.get(reverse('date-change', kwargs=url_args))
        self.assertEqual(
            response.status_code, 404,
            'Expected a 404 HTTP response code for a non-existent date')
        # Test that the assertion must be associated with the entity.
        date = assertion.create_date({'date_period': self.date_period})
        url_args['date_id'] = date.get_id()
        entity2 = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity2.get_id()
        response = self.client.get(reverse('date-change', kwargs=url_args))
        self.assertEqual(response.status_code, 404,
                         'Expected a 404 HTTP response code for an assertion for a different entity')
        # Test that the date must be associated with the assertion.
        assertion2 = entity2.get_existences()[0]
        url_args['assertion_id'] = assertion2.get_id()
        response = self.client.get(reverse('date-change', kwargs=url_args))
        self.assertEqual(response.status_code, 404,
                         'Expected a 404 HTTP response code for a date for a different assertion')
