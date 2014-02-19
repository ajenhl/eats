from django.conf import settings
from django.core.urlresolvers import reverse

from eats.tests.views.view_test_case import ViewTestCase


class DateAddViewTestCase (ViewTestCase):

    def setUp (self):
        super(DateAddViewTestCase, self).setUp()
        self.authority_id = self.authority.get_id()
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.editor.set_current_authority(self.authority)

    def test_authentication (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        url = reverse('date-add', kwargs={'entity_id': entity.get_id(),
                                          'assertion_id': existence.get_id()})
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
        response = self.app.get(url, status=404, user='user2')

    def test_non_matching_date_add (self):
        """Tests that the entity and assertion match when adding a
        date."""
        url_args = {'entity_id': 0, 'assertion_id': 0}
        # Test with non-existent entity and assertion.
        self.app.get(reverse('date-add', kwargs=url_args), status=404,
                     user='user')
        # Test with non-existent assertion.
        entity = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity.get_id()
        self.app.get(reverse('date-add', kwargs=url_args), status=404,
                     user='user')
        # Test with the assertion not belonging to the entity.
        entity2 = self.tm.create_entity(self.authority)
        assertion = entity2.get_existences()[0]
        url_args['assertion_id'] = assertion.get_id()
        self.app.get(reverse('date-add', kwargs=url_args), status=404,
                     user='user')

    def test_get_request (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        url = reverse('date-add', kwargs={'entity_id': entity.get_id(),
                                          'assertion_id': existence.get_id()})
        response = self.app.get(url, user='user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/date_add.html')

    def test_valid_post_request_continue (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        self.assertEqual(len(existence.get_dates()), 0)
        url = reverse('date-add', kwargs={'entity_id': entity.get_id(),
                                          'assertion_id': existence.get_id()})
        date_period = self.create_date_period('lifespan')
        calendar = self.create_calendar('Gregorian')
        date_type = self.create_date_type('exact')
        self.authority.set_date_periods([date_period])
        self.authority.set_calendars([calendar])
        self.authority.set_date_types([date_type])
        form = self.app.get(url, user='user').forms['date-add-form']
        form['date_period'] = date_period.get_id()
        form['point_calendar'] = calendar.get_id()
        form['point_certainty'] = 'on'
        form['point_type'] = date_type.get_id()
        form['point'] = '9 February 2011'
        form['point_normalised'] = '2011-02-09'
        response = form.submit('_continue')
        self.assertEqual(len(existence.get_dates()), 1)
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

    def test_valid_post_request_save (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        self.assertEqual(len(existence.get_dates()), 0)
        url = reverse('date-add', kwargs={'entity_id': entity.get_id(),
                                          'assertion_id': existence.get_id()})
        date_period = self.create_date_period('lifespan')
        calendar = self.create_calendar('Gregorian')
        date_type = self.create_date_type('exact')
        self.authority.set_date_periods([date_period])
        self.authority.set_calendars([calendar])
        self.authority.set_date_types([date_type])
        form = self.app.get(url, user='user').forms['date-add-form']
        form['date_period'] = date_period.get_id()
        form['point_calendar'] = calendar.get_id()
        form['point_certainty'] = 'on'
        form['point_type'] = date_type.get_id()
        form['point'] = '9 February 2011'
        form['point_normalised'] = '2011-02-09'
        response = form.submit('_save')
        self.assertEqual(len(existence.get_dates()), 1)
        date = existence.get_dates()[0]
        self.assertEqual(date.period, date_period)
        self.assertEqual(date.point.calendar, calendar)
        self.assertEqual(date.point.certainty, self.tm.date_full_certainty)
        self.assertEqual(date.point.date_type, date_type)
        self.assertEqual(date.point.get_value(), '9 February 2011')
        self.assertEqual(date.point.get_normalised_value(), '2011-02-09')
        redirect_url = reverse('entity-change',
                               kwargs={'entity_id': entity.get_id()})
        self.assertRedirects(response, redirect_url)

    def test_invalid_post_request (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        self.assertEqual(len(existence.get_dates()), 0)
        url = reverse('date-add', kwargs={'entity_id': entity.get_id(),
                                          'assertion_id': existence.get_id()})
        date_period = self.create_date_period('lifespan')
        calendar = self.create_calendar('Gregorian')
        self.authority.set_date_periods([date_period])
        self.authority.set_calendars([calendar])
        # Omitting the point date type should make the form submission
        # invalid.
        form = self.app.get(url, user='user').forms['date-add-form']
        form['date_period'] = date_period.get_id()
        form['point_calendar'] = calendar.get_id()
        form['point_certainty'] = 'on'
        form['point'] = '9 February 2011'
        form['point_normalised'] = '2011-02-09'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(existence.get_dates()), 0)
