from django.core.urlresolvers import reverse

from eats.tests.base_test_case import BaseTestCase


class DateChangeViewTestCase (BaseTestCase):

    def setUp (self):
        super(DateChangeViewTestCase, self).setUp()
        self.date_period = self.create_date_period('lifespan')
        self.calendar = self.create_calendar('Gregorian')
        self.date_type = self.create_date_type('exact')
    
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

    def test_get_request (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date = existence.create_date({'date_period': self.date_period})
        response = self.client.get(reverse(
                'date-change', kwargs={'entity_id': entity.get_id(),
                                       'assertion_id': existence.get_id(),
                                       'date_id': date.get_id()}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/date_change.html')

    def test_valid_post_request (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date_data = {'date_period': self.date_period, 'point': '1 January 1900',
                     'point_normalised': '1900-01-01',
                     'point_calendar': self.calendar,
                     'point_type': self.date_type,
                     'point_certainty': self.tm.date_full_certainty}
        date = existence.create_date(date_data)
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': existence.get_id(),
                    'date_id': date.get_id()}
        url = reverse('date-change', kwargs=url_args)
        date_period2 = self.create_date_period('floruit')
        post_data = {'date_period': date_period2.get_id(),
                     'point_taq_calendar': self.calendar.get_id(),
                     'point_taq_certainty': 'on',
                     'point_taq_type': self.date_type.get_id(),
                     'point_taq': '9 February 2011',
                     'point_taq_normalised': '2011-02-09',
                     }
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, url)
        date = existence.get_dates()[0]
        self.assertEqual(date.period, date_period2)
        self.assertEqual(date.point_taq.calendar, self.calendar)
        self.assertEqual(date.point_taq.certainty, self.tm.date_full_certainty)
        self.assertEqual(date.point_taq.date_type, self.date_type)
        self.assertEqual(date.point_taq.get_value(), '9 February 2011')
        self.assertEqual(date.point_taq.get_normalised_value(), '2011-02-09')
        self.assertEqual(date.point.get_value(), '')
