# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import Entity
from eats.tests.views.view_test_case import ViewTestCase


class EntityMergeViewTestCase (ViewTestCase):

    def setUp (self):
        super(EntityMergeViewTestCase, self).setUp()
        self.authority_id = self.authority.get_id()
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.editor.set_current_authority(self.authority)

    def test_authentication (self):
        entity = self.tm.create_entity(self.authority)
        url = reverse('entity-merge', kwargs={'entity_id': entity.get_id()})
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

    def test_non_existent_entity (self):
        url = reverse('entity-merge', kwargs={'entity_id': 0})
        self.app.get(url, status=404, user='user')

    def test_missing_merge_entity (self):
        entity = self.tm.create_entity(self.authority)
        url = reverse('entity-merge', kwargs={'entity_id': entity.get_id()})
        response = self.app.get(url, user='user')
        form = response.forms['entity-merge-form']
        form['merge_entity_1'] = None
        response = form.submit()
        # No redirect, due to invalid form.
        self.assertEqual(response.status_code, 200)

    def test_unauthorised (self):
        authority2 = self.create_authority('new authority')
        entity_type1 = self.create_entity_type('Person')
        entity_type2 = self.create_entity_type('Being')
        self.authority.set_entity_types([entity_type1, entity_type2])
        authority2.set_entity_types([entity_type1])
        entity1 = self.tm.create_entity(self.authority)
        entity1_type1 = entity1.create_entity_type_property_assertion(
            self.authority, entity_type1)
        entity2 = self.tm.create_entity(self.authority)
        entity2_type1 = entity2.create_entity_type_property_assertion(
            self.authority, entity_type2)
        entity2_type2 = entity2.create_entity_type_property_assertion(
            authority2, entity_type1)
        self.assertEqual(Entity.objects.count(), 2)
        url = reverse('entity-merge', kwargs={'entity_id': entity1.get_id()})
        response = self.app.get(url, user='user')
        form = response.forms['entity-merge-form']
        form['merge_entity_1'] = entity2.get_id()
        response = form.submit()
        # No redirect, due to the merge entity having property
        # assertions that the user is not an editor for.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Entity.objects.count(), 2)
        self.assertEqual(set(entity1.get_entity_types()), set([entity1_type1]))
        self.assertEqual(set(entity2.get_entity_types()),
                         set([entity2_type1, entity2_type2]))

    def test_successful_merge (self):
        entity_type1 = self.create_entity_type('Person')
        entity_type2 = self.create_entity_type('Being')
        self.authority.set_entity_types([entity_type1, entity_type2])
        entity1 = self.tm.create_entity(self.authority)
        type1 = entity1.create_entity_type_property_assertion(self.authority,
                                                              entity_type1)
        entity2 = self.tm.create_entity(self.authority)
        type2 = entity2.create_entity_type_property_assertion(self.authority,
                                                              entity_type2)
        type3 = entity2.create_entity_type_property_assertion(self.authority,
                                                              entity_type1)
        self.assertEqual(Entity.objects.count(), 2)
        url = reverse('entity-merge', kwargs={'entity_id': entity1.get_id()})
        response = self.app.get(url, user='user')
        form = response.forms['entity-merge-form']
        form['merge_entity_1'] = entity2.get_id()
        response = form.submit().follow()
        self.assertEqual(response.request.path_qs,
                         reverse('entity-change',
                                 kwargs={'entity_id': entity1.get_id()}))
        self.assertEqual(Entity.objects.count(), 1)
        self.assertEqual(set(entity1.get_entity_types()),
                         set([type1, type2]))

    def test_merge_redirect (self):
        # A merged entity should have URLs based on its identifier
        # redirect to the appropriate page for the entity it was
        # merged into.
        entity1 = self.tm.create_entity(self.authority)
        entity2 = self.tm.create_entity(self.authority)
        views =  ('entity-view', 'entity-eatsml-view', 'entity-change',
                  'entity-delete', 'entity-merge')
        for view in views:
            url = reverse(view, kwargs={'entity_id': entity2.get_id()})
            response = self.app.get(url, user='user')
            self.assertEqual(response.status_code, 200,
                             'Got an incorrect response for the "%s" view'
                             % view)
        entity1.merge_in(entity2)
        for view in views:
            url = reverse(view, kwargs={'entity_id': entity2.get_id()})
            response = self.app.get(url, user='user')
            self.assertEqual(response.status_code, 301)
            redirect_url = reverse(view, kwargs={'entity_id': entity1.get_id()})
            self.assertRedirects(response, redirect_url, status_code=301,
                                 msg_prefix='With the "%s" view'
                                 % view)
