from django.core.urlresolvers import reverse

from eats.models import NamePartType
from eats.tests.base_test_case import BaseTestCase


class NamePartTypeViewsTestCase (BaseTestCase):

    def test_name_part_type_list (self):
        url = reverse('nameparttype-list')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], NamePartType._meta)
        self.assertEqual(len(response.context['topics']), 0)
        name_part_type = self.create_name_part_type('given')
        response = self.client.get(url)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(name_part_type in response.context['topics'])

    def test_name_part_type_add_get (self):
        url = reverse('nameparttype-add')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], NamePartType._meta)
        
    def test_name_part_type_add_post_redirects (self):
        self.assertEqual(NamePartType.objects.count(), 0)
        url = reverse('nameparttype-add')
        post_data = {'name': 'given', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('nameparttype-list'))
        self.assertEqual(NamePartType.objects.count(), 1)
        post_data = {'name': 'family', '_addanother': 'Save and add another'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, url)
        self.assertEqual(NamePartType.objects.count(), 2)
        post_data = {'name': 'patronymic',
                     '_continue': 'Save and continue editing'}
        response = self.client.post(url, post_data, follow=True)
        name_part_type = NamePartType.objects.get_by_admin_name('patronymic')
        redirect_url = reverse('nameparttype-change',
                               kwargs={'topic_id': name_part_type.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(NamePartType.objects.count(), 3)

    def test_name_part_type_add_illegal_post (self):
        self.assertEqual(NamePartType.objects.count(), 0)
        url = reverse('nameparttype-add')
        # Missing name_part_type name.
        post_data = {'name': '', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NamePartType.objects.count(), 0)
        # Duplicate name_part_type name.
        name_part_type = self.create_name_part_type('given')
        self.assertEqual(NamePartType.objects.count(), 1)
        post_data = {'name': 'given', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NamePartType.objects.count(), 1)
        self.assertTrue(name_part_type in NamePartType.objects.all())
        
    def test_name_part_type_change_illegal_get (self):
        url = reverse('nameparttype-change', kwargs={'topic_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_name_part_type_change_get (self):
        name_part_type = self.create_name_part_type('exact')
        url = reverse('nameparttype-change', kwargs={
                'topic_id': name_part_type.get_id()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, name_part_type)

    def test_name_part_type_change_post (self):
        self.assertEqual(NamePartType.objects.count(), 0)
        name_part_type = self.create_name_part_type('given')
        url = reverse('nameparttype-change', kwargs={
                'topic_id': name_part_type.get_id()})
        self.assertEqual(name_part_type.get_admin_name(), 'given')
        post_data = {'name': 'family', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('nameparttype-list'))
        self.assertEqual(NamePartType.objects.count(), 1)
        self.assertEqual(name_part_type.get_admin_name(), 'family')

