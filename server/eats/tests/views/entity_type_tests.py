from django.core.urlresolvers import reverse

from eats.models import EntityType
from eats.tests.views.view_test_case import ViewTestCase


class EntityTypeViewsTestCase (ViewTestCase):

    def test_entity_type_list (self):
        url = reverse('entitytype-list')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], EntityType._meta)
        self.assertEqual(len(response.context['topics']), 0)
        entity_type = self.create_entity_type('person')
        response = self.client.get(url)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(entity_type in response.context['topics'])

    def test_entity_type_add_get (self):
        url = reverse('entitytype-add')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], EntityType._meta)
        
    def test_entity_type_add_post_redirects (self):
        self.assertEqual(EntityType.objects.count(), 0)
        url = reverse('entitytype-add')
        post_data = {'name': 'person', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('entitytype-list'))
        self.assertEqual(EntityType.objects.count(), 1)
        post_data = {'name': 'place', '_addanother': 'Save and add another'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, url)
        self.assertEqual(EntityType.objects.count(), 2)
        post_data = {'name': 'organisation',
                     '_continue': 'Save and continue editing'}
        response = self.client.post(url, post_data, follow=True)
        entity_type = EntityType.objects.get_by_admin_name('organisation')
        redirect_url = reverse('entitytype-change',
                               kwargs={'topic_id': entity_type.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(EntityType.objects.count(), 3)

    def test_entity_type_add_illegal_post (self):
        self.assertEqual(EntityType.objects.count(), 0)
        url = reverse('entitytype-add')
        # Missing entity_type name.
        post_data = {'name': '', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntityType.objects.count(), 0)
        # Duplicate entity_type name.
        entity_type = self.create_entity_type('person')
        self.assertEqual(EntityType.objects.count(), 1)
        post_data = {'name': 'person', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntityType.objects.count(), 1)
        self.assertTrue(entity_type in EntityType.objects.all())
        
    def test_entity_type_change_illegal_get (self):
        url = reverse('entitytype-change', kwargs={'topic_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_entity_type_change_get (self):
        entity_type = self.create_entity_type('exact')
        url = reverse('entitytype-change', kwargs={
                'topic_id': entity_type.get_id()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, entity_type)

    def test_entity_type_change_post (self):
        self.assertEqual(EntityType.objects.count(), 0)
        entity_type = self.create_entity_type('person')
        url = reverse('entitytype-change', kwargs={
                'topic_id': entity_type.get_id()})
        self.assertEqual(entity_type.get_admin_name(), 'person')
        post_data = {'name': 'place', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('entitytype-list'))
        self.assertEqual(EntityType.objects.count(), 1)
        self.assertEqual(entity_type.get_admin_name(), 'place')

