from django.core.urlresolvers import reverse

from eats.models import EntityRelationshipType
from eats.tests.views.view_test_case import ViewTestCase


class EntityRelationshipTypeViewsTestCase (ViewTestCase):

    def test_entity_type_list (self):
        url = reverse('entityrelationshiptype-list')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], EntityRelationshipType._meta)
        self.assertEqual(len(response.context['topics']), 0)
        er_type = self.create_entity_relationship_type('Forward', 'Reverse')
        response = self.client.get(url)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(er_type in response.context['topics'])

    def test_entity_relationship_type_add_get (self):
        url = reverse('entityrelationshiptype-add')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], EntityRelationshipType._meta)
        
    def test_entity_relationship_type_add_post_redirects (self):
        self.assertEqual(EntityRelationshipType.objects.count(), 0)
        url = reverse('entityrelationshiptype-add')
        post_data = {'name': 'Forward', 'reverse_name': 'Reverse',
                     '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('entityrelationshiptype-list'))
        self.assertEqual(EntityRelationshipType.objects.count(), 1)
        post_data = {'name': 'Forward2', 'reverse_name': 'Reverse2',
                     '_addanother': 'Save and add another'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, url)
        self.assertEqual(EntityRelationshipType.objects.count(), 2)
        post_data = {'name': 'Forward3', 'reverse_name': 'Reverse3',
                     '_continue': 'Save and continue editing'}
        response = self.client.post(url, post_data, follow=True)
        er_type = EntityRelationshipType.objects.get_by_admin_name(
            'Forward3', 'Reverse3')
        redirect_url = reverse('entityrelationshiptype-change',
                               kwargs={'topic_id': er_type.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(EntityRelationshipType.objects.count(), 3)

    def test_entity_relationship_type_add_illegal_post (self):
        self.assertEqual(EntityRelationshipType.objects.count(), 0)
        url = reverse('entityrelationshiptype-add')
        # Missing entity_relationship_type name.
        post_data = {'name': '', 'reverse_name': '', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntityRelationshipType.objects.count(), 0)
        # Missing entity_relationship_type reverse name.
        post_data = {'name': 'Forward', 'reverse_name': '', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntityRelationshipType.objects.count(), 0)
        # Duplicate entity_relationship_type name and reverse name.
        er_type = self.create_entity_relationship_type('Forward', 'Reverse')
        self.assertEqual(EntityRelationshipType.objects.count(), 1)
        post_data = {'name': 'Forward', 'reverse_name': 'Reverse',
                     '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntityRelationshipType.objects.count(), 1)
        self.assertTrue(er_type in EntityRelationshipType.objects.all())
        
    def test_entity_relationship_type_change_illegal_get (self):
        url = reverse('entityrelationshiptype-change', kwargs={'topic_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_entity_relationship_type_change_get (self):
        er_type = self.create_entity_relationship_type('Forward', 'Reverse')
        url = reverse('entityrelationshiptype-change', kwargs={
                'topic_id': er_type.get_id()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, er_type)

    def test_entity_relationship_type_change_post (self):
        self.assertEqual(EntityRelationshipType.objects.count(), 0)
        er_type = self.create_entity_relationship_type('Forward', 'Reverse')
        url = reverse('entityrelationshiptype-change', kwargs={
                'topic_id': er_type.get_id()})
        self.assertEqual(er_type.get_admin_name(), 'Forward / Reverse')
        post_data = {'name': 'Forward2', 'reverse_name': 'Reverse2',
                     '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('entityrelationshiptype-list'))
        self.assertEqual(EntityRelationshipType.objects.count(), 1)
        self.assertEqual(er_type.get_admin_name(), 'Forward2 / Reverse2')

