from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import DatePeriod
from .admin_view_test_case import AdminViewTestCase


class DatePeriodViewsTestCase (AdminViewTestCase):

    def test_authentication (self):
        date_period = self.create_date_period('lifespan')
        url_data = [
            ('eats-dateperiod-list', {}),
            ('eats-dateperiod-add', {}),
            ('eats-dateperiod-change', {'topic_id': date_period.get_id()})]
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

    def test_date_period_list (self):
        url = reverse('eats-dateperiod-list')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], DatePeriod._meta)
        self.assertEqual(len(response.context['topics']), 0)
        date_period = self.create_date_period('Gregorian')
        response = self.app.get(url, user='staff')
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(date_period in response.context['topics'])

    def test_date_period_add_get (self):
        url = reverse('eats-dateperiod-add')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], DatePeriod._meta)

    def test_date_period_add_post_redirects (self):
        self.assertEqual(DatePeriod.objects.count(), 0)
        url = reverse('eats-dateperiod-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'lifespan'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-dateperiod-list'))
        self.assertEqual(DatePeriod.objects.count(), 1)
        form['name'] = 'floruit'
        response = form.submit('_addanother')
        self.assertRedirects(response, url)
        self.assertEqual(DatePeriod.objects.count(), 2)
        form['name'] = 'germination'
        response = form.submit('_continue')
        date_period = DatePeriod.objects.get_by_admin_name('germination')
        redirect_url = reverse('eats-dateperiod-change',
                               kwargs={'topic_id': date_period.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(DatePeriod.objects.count(), 3)

    def test_date_period_add_illegal_post (self):
        self.assertEqual(DatePeriod.objects.count(), 0)
        url = reverse('eats-dateperiod-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        # Missing date_period name.
        form['name'] = ''
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DatePeriod.objects.count(), 0)
        # Duplicate date_period name.
        date_period = self.create_date_period('lifespan')
        self.assertEqual(DatePeriod.objects.count(), 1)
        form['name'] = 'lifespan'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DatePeriod.objects.count(), 1)
        self.assertTrue(date_period in DatePeriod.objects.all())

    def test_date_period_change_illegal_get (self):
        url = reverse('eats-dateperiod-change', kwargs={'topic_id': 0})
        self.app.get(url, status=404, user='staff')

    def test_date_period_change_get (self):
        date_period = self.create_date_period('lifespan')
        url = reverse('eats-dateperiod-change', kwargs={
                'topic_id': date_period.get_id()})
        response = self.app.get(url, user='staff')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, date_period)

    def test_date_period_change_post (self):
        self.assertEqual(DatePeriod.objects.count(), 0)
        date_period = self.create_date_period('lifespan')
        self.assertEqual(date_period.get_admin_name(), 'lifespan')
        url = reverse('eats-dateperiod-change', kwargs={
                'topic_id': date_period.get_id()})
        form = self.app.get(url, user='staff').forms[
            'infrastructure-change-form']
        form['name'] = 'floruit'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-dateperiod-list'))
        self.assertEqual(DatePeriod.objects.count(), 1)
        self.assertEqual(date_period.get_admin_name(), 'floruit')
