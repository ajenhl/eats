from django.core.urlresolvers import reverse

from eats.models import DatePeriod
from eats.tests.views.view_test_case import ViewTestCase


class DatePeriodViewsTestCase (ViewTestCase):

    def test_date_period_list (self):
        url = reverse('dateperiod-list')
        response = self.app.get(url)
        self.assertEqual(response.context['opts'], DatePeriod._meta)
        self.assertEqual(len(response.context['topics']), 0)
        date_period = self.create_date_period('Gregorian')
        response = self.app.get(url)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(date_period in response.context['topics'])

    def test_date_period_add_get (self):
        url = reverse('dateperiod-add')
        response = self.app.get(url)
        self.assertEqual(response.context['opts'], DatePeriod._meta)
        
    def test_date_period_add_post_redirects (self):
        self.assertEqual(DatePeriod.objects.count(), 0)
        url = reverse('dateperiod-add')
        form = self.app.get(url).forms['infrastructure-add-form']
        form['name'] = 'lifespan'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('dateperiod-list'))
        self.assertEqual(DatePeriod.objects.count(), 1)
        form['name'] = 'floruit'
        response = form.submit('_addanother')
        self.assertRedirects(response, url)
        self.assertEqual(DatePeriod.objects.count(), 2)
        form['name'] = 'germination'
        response = form.submit('_continue')
        date_period = DatePeriod.objects.get_by_admin_name('germination')
        redirect_url = reverse('dateperiod-change',
                               kwargs={'topic_id': date_period.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(DatePeriod.objects.count(), 3)

    def test_date_period_add_illegal_post (self):
        self.assertEqual(DatePeriod.objects.count(), 0)
        url = reverse('dateperiod-add')
        form = self.app.get(url).forms['infrastructure-add-form']
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
        url = reverse('dateperiod-change', kwargs={'topic_id': 0})
        self.app.get(url, status=404)

    def test_date_period_change_get (self):
        date_period = self.create_date_period('lifespan')
        url = reverse('dateperiod-change', kwargs={
                'topic_id': date_period.get_id()})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, date_period)

    def test_date_period_change_post (self):
        self.assertEqual(DatePeriod.objects.count(), 0)
        date_period = self.create_date_period('lifespan')
        self.assertEqual(date_period.get_admin_name(), 'lifespan')
        url = reverse('dateperiod-change', kwargs={
                'topic_id': date_period.get_id()})
        form = self.app.get(url).forms['infrastructure-change-form']
        form['name'] = 'floruit'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('dateperiod-list'))
        self.assertEqual(DatePeriod.objects.count(), 1)
        self.assertEqual(date_period.get_admin_name(), 'floruit')

