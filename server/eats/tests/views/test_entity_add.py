from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import EATSUser, Entity
from eats.tests.views.view_test_case import ViewTestCase


class EntityAddViewTestCase (ViewTestCase):

    def setUp (self):
        super(EntityAddViewTestCase, self).setUp()
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.editor.set_current_authority(self.authority)

    def test_authentication (self):
        url = reverse('entity-add')
        login_url = settings.LOGIN_URL + '?next=' + url
        response = self.app.get(url)
        self.assertRedirects(response, login_url)
        user = self.create_django_user('user2', 'user2@example.org', 'password')
        response = self.app.get(url, user='user2')
        self.assertRedirects(response, login_url)
        self.create_user(user)
        response = self.app.get(url, user='user2')
        self.assertRedirects(response, login_url)
        response = self.app.get(url, user='user')
        self.assertEqual(response.status_code, 200)

    def test_add_entity (self):
        self.assertEqual(Entity.objects.count(), 0)
        url = reverse('entity-add')
        form = self.app.get(url, user='user').forms['entity-add-form']
        form['authority'] = self.authority.get_id()
        response = form.submit('_save')
        self.assertEqual(Entity.objects.count(), 1)
        entity_id = Entity.objects.all()[0].get_id()
        redirect_url = reverse('entity-change', kwargs={'entity_id': entity_id})
        self.assertRedirects(response, redirect_url)

    def test_change_current_authority (self):
        authority = self.create_authority('Test2')
        self.editor.editable_authorities = [self.authority, authority]
        self.assertEqual(self.editor.get_current_authority(), self.authority)
        self.assertEqual(Entity.objects.count(), 0)
        url = reverse('entity-add')
        form = self.app.get(url, user='user').forms['entity-add-form']
        form['authority'] = authority.get_id()
        response = form.submit('_save')
        self.assertEqual(Entity.objects.count(), 1)
        entity_id = Entity.objects.all()[0].get_id()
        # self.editor is out-of-date, since the view has changed the
        # database in the meantime. Therefore instantiate a new model
        # object.
        editor = EATSUser.objects.get(pk=self.editor.pk)
        self.assertEqual(editor.get_current_authority(), authority)
        redirect_url = reverse('entity-change', kwargs={'entity_id': entity_id})
        self.assertRedirects(response, redirect_url)
