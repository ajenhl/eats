from django.conf import settings
from django.core.urlresolvers import reverse

from eats.tests.views.view_test_case import ViewTestCase


class DateChangeViewTestCase (ViewTestCase):

    def setUp (self):
        super(DateChangeViewTestCase, self).setUp()
        self.date_period = self.create_date_period('lifespan')
        self.calendar = self.create_calendar('Gregorian')
        self.date_type = self.create_date_type('exact')
        self.authority.set_date_periods([self.date_period])
        self.authority.set_calendars([self.calendar])
        self.authority.set_date_types([self.date_type])
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.editor.set_current_authority(self.authority)
    
    def test_authentication (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date_data = {'date_period': self.date_period, 'point': '1 January 1900',
                     'point_normalised': '1900-01-01',
                     'point_calendar': self.calendar,
                     'point_type': self.date_type,
                     'point_certainty': self.tm.date_full_certainty}
        date = existence.create_date(date_data)
        url_args = {'entity_id': entity.get_id(), 'date_id': date.get_id(),
                    'assertion_id': existence.get_id()}
        url = reverse('date-change', kwargs=url_args)
        login_url = settings.LOGIN_URL + '?next=' + url
        response = self.app.get(url)
        self.assertRedirects(response, login_url)
        user = self.create_django_user('user2', 'user2@example.org', 'password')
        response = self.app.get(url, user='user2')
        self.assertRedirects(response, login_url)
        eats_user = self.create_user(user)
        response = self.app.get(url, user='user2')
        self.assertRedirects(response, login_url)        
        authority = self.create_authority('Test2')
        eats_user.editable_authorities = [self.authority, authority]
        eats_user.set_current_authority(authority)
        self.app.get(url, status=404, user='user2')

    def test_non_matching_date_change (self):
        """Tests that the entity, assertion, and date match when
        editing a date."""
        # Test with none of entity, assertion and date existing.
        url_args = {'entity_id': 0, 'assertion_id': 0, 'date_id': 0}
        self.app.get(reverse('date-change', kwargs=url_args), status=404,
                     user='user')
        # Test with only the entity existing.
        entity = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity.get_id()
        self.app.get(reverse('date-change', kwargs=url_args), status=404,
                     user='user')
        # Test with only the entity and assertion existing.
        assertion = entity.get_existences()[0]
        url_args['assertion_id'] = assertion.get_id()
        self.app.get(reverse('date-change', kwargs=url_args), status=404,
                     user='user')
        # Test that the assertion must be associated with the entity.
        date = assertion.create_date({'date_period': self.date_period})
        url_args['date_id'] = date.get_id()
        entity2 = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity2.get_id()
        self.app.get(reverse('date-change', kwargs=url_args), status=404,
                     user='user')
        # Test that the date must be associated with the assertion.
        assertion2 = entity2.get_existences()[0]
        url_args['assertion_id'] = assertion2.get_id()
        self.app.get(reverse('date-change', kwargs=url_args), status=404,
                     user='user')

    def test_get_request (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date = existence.create_date({'date_period': self.date_period})
        url = reverse('date-change', kwargs={'entity_id': entity.get_id(),
                                             'assertion_id': existence.get_id(),
                                             'date_id': date.get_id()})
        response = self.app.get(url, user='user')
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
        self.authority.set_date_periods([self.date_period, date_period2])
        form = self.app.get(url, user='user').forms['date-change-form']
        form['date_period'] = date_period2.get_id()
        form['point_taq_calendar'] = self.calendar.get_id()
        form['point_taq_certainty'] = 'on'
        form['point_taq_type'] = self.date_type.get_id()
        form['point_taq'] = '9 February 2011'
        form['point_taq_normalised'] = '2011-02-09'
        form['point'] = ''
        form['point_normalised'] = ''
        form['point_calendar'] = ''
        form['point_type'] = ''
        form['point_certainty'] = None
        response = form.submit('_continue')
        self.assertRedirects(response, url)
        date = existence.get_dates()[0]
        self.assertEqual(date.period, date_period2)
        self.assertEqual(date.point_taq.calendar, self.calendar)
        self.assertEqual(date.point_taq.certainty, self.tm.date_full_certainty)
        self.assertEqual(date.point_taq.date_type, self.date_type)
        self.assertEqual(date.point_taq.get_value(), '9 February 2011')
        self.assertEqual(date.point_taq.get_normalised_value(), '2011-02-09')
        self.assertEqual(date.point.get_value(), '')
        form['date_period'] = self.date_period.get_id()
        form['start'] = '6 June 1812'
        form['start_normalised'] = '1812-06-06'
        form['start_calendar'] = self.calendar.get_id()
        form['start_type'] = self.date_type.get_id()
        form['point_taq_calendar'] = ''
        form['point_taq_certainty'] = None
        form['point_taq_type'] = ''
        form['point_taq'] = ''
        form['point_taq_normalised'] = ''
        response = form.submit('_save')
        url2 = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        self.assertRedirects(response, url2)
        date = existence.get_dates()[0]
        self.assertEqual(date.period, self.date_period)
        self.assertEqual(date.start.calendar, self.calendar)
        self.assertEqual(date.start.certainty, self.tm.date_no_certainty)
        self.assertEqual(date.start.date_type, self.date_type)
        self.assertEqual(date.start.get_value(), '6 June 1812')
        self.assertEqual(date.start.get_normalised_value(), '1812-06-06')
        self.assertEqual(date.point.get_value(), '')
        self.assertEqual(date.point_taq.get_value(), '')

    def test_delete (self):
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(1, len(entity.get_existences()))
        existence = entity.get_existences()[0]
        self.assertEqual(0, len(existence.get_dates()))
        date_data = {'date_period': self.date_period, 'point': '1 January 1900',
                     'point_normalised': '1900-01-01',
                     'point_calendar': self.calendar,
                     'point_type': self.date_type,
                     'point_certainty': self.tm.date_full_certainty}
        date = existence.create_date(date_data)
        self.assertEqual(1, len(existence.get_dates()))
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': existence.get_id(),
                    'date_id': date.get_id()}
        url = reverse('date-change', kwargs=url_args)
        form = self.app.get(url, user='user').forms['date-change-form']
        response = form.submit('_delete')
        url2 = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        self.assertRedirects(response, url2)
        self.assertEqual(0, len(existence.get_dates()))
        self.assertEqual(1, len(entity.get_existences()))
        self.app.get(url, status=404, user='user')
