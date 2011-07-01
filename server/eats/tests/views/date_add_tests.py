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
        
    def test_valid_post_request (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        url = reverse('date-add', kwargs={'entity_id': entity.get_id(),
                                          'assertion_id': existence.get_id()})
        date_period = self.create_date_period('lifespan')
        calendar = self.create_calendar('Gregorian')
        date_type = self.create_date_type('exact')
        post_data = {'date_period': date_period.get_id(),
                     'point_calendar': calendar.get_id(),
                     'point_certainty': 'on',
                     'point_type': date_type.get_id(),
                     'point': '9 February 2011',
                     'point_normalised': '2011-02-09'}
        response = self.client.post(url, post_data)
        date = existence.get_dates()[0]
        self.assertEqual(date.period, date_period)
        self.assertEqual(date.point.calendar, calendar)
        self.assertEqual(date.point.certainty, self.tm.date_full_certainty)
        self.assertEqual(date.point.date_type, date_type)
        self.assertEqual(date.point.get_value(), '9 February 2011')
        self.assertEqual(date.point.get_normalised_value(), '2011-02-09')
        redirect_url = reverse('date-change',
                               kwargs={'entity_id': entity.get_id(),
                                       'assertion_id': existence.get_id(),
                                       'date_id': date.get_id()})
        self.assertRedirects(response, redirect_url)

    def test_invalid_post_request (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        url = reverse('date-add', kwargs={'entity_id': entity.get_id(),
                                          'assertion_id': existence.get_id()})
        date_period = self.create_date_period('lifespan')
        calendar = self.create_calendar('Gregorian')
        # Omitting 
        post_data = {'date_period': date_period.get_id(),
                     'point_calendar': calendar.get_id(),
                     'point_certainty': 'on',
                     'point': '9 February 2011',
                     'point_normalised': '2011-02-09'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
