from django.core.urlresolvers import reverse

from eats.models import Entity
from eats.tests.views.view_test_case import ViewTestCase


class EntityDeleteViewTestCase (ViewTestCase):

    def setUp (self):
        super(EntityDeleteViewTestCase, self).setUp()
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.editor.set_current_authority(self.authority)
        
    def test_non_existent_entity (self):
        url = reverse('entity-delete', kwargs={'entity_id': 0})
        self.app.get(url, status=404, user='user')

    def test_delete (self):
        # Test for successful deletion of an entity associated with a
        # single authority that the user is an editor for.
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(Entity.objects.count(), 1)
        url = reverse('entity-delete', kwargs={'entity_id': entity.get_id()})
        form = self.app.get(url, user='user').forms['entity-delete-form']
        response = form.submit('_delete')
        self.assertRedirects(response, reverse('search'))
        self.assertEqual(Entity.objects.count(), 0)
        # Test for unsuccessful deletion of an entity associated with
        # two authorities, one of which the user is not an editor for.
        authority2 = self.tm.create_authority('Test2')
        entity2 = self.tm.create_entity(self.authority)
        entity2.create_note_property_assertion(authority2, 'Test note')
        self.assertEqual(Entity.objects.count(), 1)
        url = reverse('entity-delete', kwargs={'entity_id': entity2.get_id()})
        response = self.app.get(url, user='user')
        # There should be no delete form.
        self.assertTrue('entity-delete-form' not in response.forms)
        # A submission even without the form should fail.
        self.csrf_checks = False
        self._patch_settings()
        self.renew_app()
        response = self.app.post(url, {'_delete': 'Delete'}, user='user')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Entity.objects.count(), 1)
        self.csrf_checks = True
        self._patch_settings()
        self.renew_app()
        # Test that the delete succeeds when the user is made an
        # editor for the second authority too.
        self.editor.editable_authorities = [self.authority, authority2]
        form = self.app.get(url, user='user').forms['entity-delete-form']
        response = form.submit('_delete')
        self.assertRedirects(response, reverse('search'))
        self.assertEqual(Entity.objects.count(), 0)
