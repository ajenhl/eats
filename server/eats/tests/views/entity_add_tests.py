from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import EATSUser, Entity
from eats.tests.base_test_case import BaseTestCase


class EntityAddViewTestCase (BaseTestCase):

    def setUp (self):
        super(EntityAddViewTestCase, self).setUp()
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.editor.set_current_authority(self.authority)

    def test_authentication (self):
        url = reverse('entity-add')
        login_url = settings.LOGIN_URL + '?next=' + url
        response = self.client.get(url)
        self.assertRedirects(response, login_url)
        user = self.create_django_user('user2', 'user@example.org', 'password')
        self.client.login(username='user2', password='password')
        response = self.client.get(url)
        self.assertRedirects(response, login_url)
        self.create_user(user)
        response = self.client.get(url)
        self.assertRedirects(response, login_url)
        self.client.login(username='user', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_entity (self):
        self.client.login(username='user', password='password')
        self.assertEqual(Entity.objects.count(), 0)
        url = reverse('entity-add')
        response = self.client.post(url, {'authority': self.authority.get_id(),
                                          '_save': 'Create and edit'})
        self.assertEqual(Entity.objects.count(), 1)
        entity_id = Entity.objects.all()[0].get_id()
        redirect_url = reverse('entity-change', kwargs={'entity_id': entity_id})
        self.assertRedirects(response, redirect_url)

    def test_change_current_authority (self):
        authority = self.create_authority('Test2')
        self.editor.editable_authorities = [self.authority, authority]
        self.assertEqual(self.editor.get_current_authority(), self.authority)
        self.client.login(username='user', password='password')
        self.assertEqual(Entity.objects.count(), 0)
        url = reverse('entity-add')
        self.client.post(url, {'authority': authority.get_id(),
                               '_save': 'Create and edit'})
        self.assertEqual(Entity.objects.count(), 1)
        # self.editor is out-of-date, since the view has changed the
        # database in the meantime. Therefore instantiate a new model
        # object.
        editor = EATSUser.objects.get(pk=self.editor.pk)
        self.assertEqual(editor.get_current_authority(), authority)
