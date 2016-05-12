from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import Calendar
from .admin_view_test_case import AdminViewTestCase


class CalendarViewsTestCase (AdminViewTestCase):

    def test_authentication (self):
        calendar = self.create_calendar('Julian')
        url_data = [
            ('eats-calendar-list', {}),
            ('eats-calendar-add', {}),
            ('eats-calendar-change', {'topic_id': calendar.get_id()})]
        for url_name, kwargs in url_data:
            url = reverse(url_name, kwargs=kwargs)
            login_url = settings.LOGIN_URL + '?next=' + url
            response = self.app.get(url)
            self.assertRedirects(response, login_url,
                                 msg_prefix='Anonymous user to {}'.format(
                                     url_name))
        for url_name, kwargs in url_data:
            response = self.app.get(url, user='user')
            self.assertRedirects(response, login_url,
                                 msg_prefix='User to {}'.format(url_name))
        for url_name, kwargs in url_data:
            response = self.app.get(url, user='eats_user')
            self.assertRedirects(response, login_url,
                                 msg_prefix='EATS user to {}'.format(url_name))
            response = self.app.get(url, user='staff')
            self.assertEqual(response.status_code, 200)

    def test_calendar_list (self):
        url = reverse('eats-calendar-list')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], Calendar._meta)
        self.assertEqual(len(response.context['topics']), 0)
        calendar = self.create_calendar('Gregorian')
        response = self.app.get(url, user='staff')
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(calendar in response.context['topics'])

    def test_calendar_add_get (self):
        url = reverse('eats-calendar-add')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], Calendar._meta)

    def test_calendar_add_post_redirects (self):
        self.assertEqual(Calendar.objects.count(), 0)
        url = reverse('eats-calendar-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'Gregorian'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-calendar-list'))
        self.assertEqual(Calendar.objects.count(), 1)
        form = self.app.get(url).forms['infrastructure-add-form']
        form['name'] = 'Julian'
        response = form.submit('_addanother')
        self.assertRedirects(response, url)
        self.assertEqual(Calendar.objects.count(), 2)
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'Lunar'
        response = form.submit('_continue')
        calendar = Calendar.objects.get_by_admin_name('Lunar')
        redirect_url = reverse('eats-calendar-change',
                               kwargs={'topic_id': calendar.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(Calendar.objects.count(), 3)

    def test_calendar_add_illegal_post (self):
        self.assertEqual(Calendar.objects.count(), 0)
        url = reverse('eats-calendar-add')
        # Missing calendar name.
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Calendar.objects.count(), 0)
        # Duplicate calendar name.
        calendar = self.create_calendar('Gregorian')
        self.assertEqual(Calendar.objects.count(), 1)
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'Gregorian'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Calendar.objects.count(), 1)
        self.assertTrue(calendar in Calendar.objects.all())

    def test_calendar_change_illegal_get (self):
        url = reverse('eats-calendar-change', kwargs={'topic_id': 0})
        self.app.get(url, status=404, user='staff')

    def test_calendar_change_get (self):
        calendar = self.create_calendar('Gregorian')
        url = reverse('eats-calendar-change', kwargs={
                'topic_id': calendar.get_id()})
        response = self.app.get(url, user='staff')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, calendar)

    def test_calendar_change_post (self):
        self.assertEqual(Calendar.objects.count(), 0)
        calendar = self.create_calendar('Gregorian')
        url = reverse('eats-calendar-change', kwargs={
                'topic_id': calendar.get_id()})
        self.assertEqual(calendar.get_admin_name(), 'Gregorian')
        form = self.app.get(url, user='staff').forms[
            'infrastructure-change-form']
        form['name'] = 'Julian'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-calendar-list'))
        self.assertEqual(Calendar.objects.count(), 1)
        self.assertEqual(calendar.get_admin_name(), 'Julian')
