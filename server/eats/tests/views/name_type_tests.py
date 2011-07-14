from django.core.urlresolvers import reverse

from eats.models import NameType
from eats.tests.base_test_case import BaseTestCase


class NameTypeViewsTestCase (BaseTestCase):

    def test_name_type_list (self):
        url = reverse('nametype-list')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], NameType._meta)
        self.assertEqual(len(response.context['topics']), 0)
        name_type = self.create_name_type('birth')
        response = self.client.get(url)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(name_type in response.context['topics'])

    def test_name_type_add_get (self):
        url = reverse('nametype-add')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], NameType._meta)
        
    def test_name_type_add_post_redirects (self):
        self.assertEqual(NameType.objects.count(), 0)
        url = reverse('nametype-add')
        post_data = {'name': 'birth', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('nametype-list'))
        self.assertEqual(NameType.objects.count(), 1)
        post_data = {'name': 'pseudonym', '_addanother': 'Save and add another'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, url)
        self.assertEqual(NameType.objects.count(), 2)
        post_data = {'name': 'soubriquet',
                     '_continue': 'Save and continue editing'}
        response = self.client.post(url, post_data, follow=True)
        name_type = NameType.objects.get_by_admin_name('soubriquet')
        redirect_url = reverse('nametype-change',
                               kwargs={'topic_id': name_type.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(NameType.objects.count(), 3)

    def test_name_type_add_illegal_post (self):
        self.assertEqual(NameType.objects.count(), 0)
        url = reverse('nametype-add')
        # Missing name_type name.
        post_data = {'name': '', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NameType.objects.count(), 0)
        # Duplicate name_type name.
        name_type = self.create_name_type('birth')
        self.assertEqual(NameType.objects.count(), 1)
        post_data = {'name': 'birth', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NameType.objects.count(), 1)
        self.assertTrue(name_type in NameType.objects.all())
        
    def test_name_type_change_illegal_get (self):
        url = reverse('nametype-change', kwargs={'topic_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_name_type_change_get (self):
        name_type = self.create_name_type('exact')
        url = reverse('nametype-change', kwargs={
                'topic_id': name_type.get_id()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, name_type)

    def test_name_type_change_post (self):
        self.assertEqual(NameType.objects.count(), 0)
        name_type = self.create_name_type('birth')
        url = reverse('nametype-change', kwargs={
                'topic_id': name_type.get_id()})
        self.assertEqual(name_type.get_admin_name(), 'birth')
        post_data = {'name': 'pseudonym', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('nametype-list'))
        self.assertEqual(NameType.objects.count(), 1)
        self.assertEqual(name_type.get_admin_name(), 'pseudonym')

