from django.core.urlresolvers import reverse

from eats.models import EntityType
from eats.tests.views.view_test_case import ViewTestCase


class EntityTypeViewsTestCase (ViewTestCase):

    def test_entity_type_list (self):
        url = reverse('entitytype-list')
        response = self.app.get(url)
        self.assertEqual(response.context['opts'], EntityType._meta)
        self.assertEqual(len(response.context['topics']), 0)
        entity_type = self.create_entity_type('person')
        response = self.app.get(url)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(entity_type in response.context['topics'])

    def test_entity_type_add_get (self):
        url = reverse('entitytype-add')
        response = self.app.get(url)
        self.assertEqual(response.context['opts'], EntityType._meta)
        
    def test_entity_type_add_post_redirects (self):
        self.assertEqual(EntityType.objects.count(), 0)
        url = reverse('entitytype-add')
        form = self.app.get(url).forms['infrastructure-add-form']
        form['name'] = 'person'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('entitytype-list'))
        self.assertEqual(EntityType.objects.count(), 1)
        form['name'] = 'place'
        response = form.submit('_addanother')
        self.assertRedirects(response, url)
        self.assertEqual(EntityType.objects.count(), 2)
        form['name'] = 'organisation'
        response = form.submit('_continue')
        entity_type = EntityType.objects.get_by_admin_name('organisation')
        redirect_url = reverse('entitytype-change',
                               kwargs={'topic_id': entity_type.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(EntityType.objects.count(), 3)

    def test_entity_type_add_illegal_post (self):
        self.assertEqual(EntityType.objects.count(), 0)
        url = reverse('entitytype-add')
        form = self.app.get(url).forms['infrastructure-add-form']
        # Missing entity_type name.
        form['name'] = ''
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntityType.objects.count(), 0)
        # Duplicate entity_type name.
        entity_type = self.create_entity_type('person')
        self.assertEqual(EntityType.objects.count(), 1)
        form['name'] = 'person'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntityType.objects.count(), 1)
        self.assertTrue(entity_type in EntityType.objects.all())
        
    def test_entity_type_change_illegal_get (self):
        url = reverse('entitytype-change', kwargs={'topic_id': 0})
        self.app.get(url, status=404)

    def test_entity_type_change_get (self):
        entity_type = self.create_entity_type('exact')
        url = reverse('entitytype-change', kwargs={
                'topic_id': entity_type.get_id()})
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, entity_type)

    def test_entity_type_change_post (self):
        self.assertEqual(EntityType.objects.count(), 0)
        entity_type = self.create_entity_type('person')
        self.assertEqual(entity_type.get_admin_name(), 'person')
        url = reverse('entitytype-change', kwargs={
                'topic_id': entity_type.get_id()})
        form = self.app.get(url).forms['infrastructure-change-form']
        form['name'] = 'place'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('entitytype-list'))
        self.assertEqual(EntityType.objects.count(), 1)
        self.assertEqual(entity_type.get_admin_name(), 'place')

