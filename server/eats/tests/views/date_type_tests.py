from django.core.urlresolvers import reverse

from eats.models import DateType
from eats.tests.views.view_test_case import ViewTestCase


class DateTypeViewsTestCase (ViewTestCase):

    def test_date_type_list (self):
        url = reverse('datetype-list')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], DateType._meta)
        self.assertEqual(len(response.context['topics']), 0)
        date_type = self.create_date_type('exact')
        response = self.client.get(url)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(date_type in response.context['topics'])

    def test_date_type_add_get (self):
        url = reverse('datetype-add')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], DateType._meta)
        
    def test_date_type_add_post_redirects (self):
        self.assertEqual(DateType.objects.count(), 0)
        url = reverse('datetype-add')
        post_data = {'name': 'exact', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('datetype-list'))
        self.assertEqual(DateType.objects.count(), 1)
        post_data = {'name': 'circa', '_addanother': 'Save and add another'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, url)
        self.assertEqual(DateType.objects.count(), 2)
        post_data = {'name': 'roughly',
                     '_continue': 'Save and continue editing'}
        response = self.client.post(url, post_data, follow=True)
        date_type = DateType.objects.get_by_admin_name('roughly')
        redirect_url = reverse('datetype-change',
                               kwargs={'topic_id': date_type.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(DateType.objects.count(), 3)

    def test_date_type_add_illegal_post (self):
        self.assertEqual(DateType.objects.count(), 0)
        url = reverse('datetype-add')
        # Missing date_type name.
        post_data = {'name': '', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DateType.objects.count(), 0)
        # Duplicate date_type name.
        date_type = self.create_date_type('exact')
        self.assertEqual(DateType.objects.count(), 1)
        post_data = {'name': 'exact', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DateType.objects.count(), 1)
        self.assertTrue(date_type in DateType.objects.all())
        
    def test_date_type_change_illegal_get (self):
        url = reverse('datetype-change', kwargs={'topic_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_date_type_change_get (self):
        date_type = self.create_date_type('exact')
        url = reverse('datetype-change', kwargs={
                'topic_id': date_type.get_id()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, date_type)

    def test_date_type_change_post (self):
        self.assertEqual(DateType.objects.count(), 0)
        date_type = self.create_date_type('exact')
        url = reverse('datetype-change', kwargs={
                'topic_id': date_type.get_id()})
        self.assertEqual(date_type.get_admin_name(), 'exact')
        post_data = {'name': 'circa', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('datetype-list'))
        self.assertEqual(DateType.objects.count(), 1)
        self.assertEqual(date_type.get_admin_name(), 'circa')

