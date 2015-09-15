# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse

from eats.constants import FORWARD_RELATIONSHIP_MARKER, \
    REVERSE_RELATIONSHIP_MARKER
from eats.models import Name, NamePart
from eats.tests.views.view_test_case import ViewTestCase


class EntityChangeViewTestCase (ViewTestCase):

    def setUp (self):
        super(EntityChangeViewTestCase, self).setUp()
        self.authority_id = self.authority.get_id()
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.editor.set_current_authority(self.authority)

    def test_authentication (self):
        entity = self.tm.create_entity(self.authority)
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
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
        url = reverse('entity-change', kwargs={'entity_id': 0})
        self.app.get(url, status=404, user='user')

    def test_empty_entity (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        response = self.app.get(url, user='user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/entity_change.html')
        # A newly created entity will have one existence property
        # assertion, and no other property assertions.
        formset = response.context['existence_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled existence form')
        existence_data = formset.initial_forms[0].initial
        self.assertEqual(existence_data['assertion'], existence.get_id())
        self.assertEqual(existence_data['authority'], self.authority_id)
        self.assertEqual(existence_data['authority'],
                         existence.authority.get_id())
        for formset in ('entity_type_formset', 'entity_relationship_formset',
                        'name_formset', 'note_formset'):
            self.assertEqual(response.context[formset].initial_form_count(), 0,
                             'Expected no %ss' % formset)

    def test_post_redirect_add (self):
        entity = self.tm.create_entity(self.authority)
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        form = self.app.get(url, user='user').forms['entity-change-form']
        response = form.submit('_save_add').follow()
        add_url = reverse('entity-add')
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         add_url)

    def test_post_entity_relationships (self):
        entity = self.tm.create_entity(self.authority)
        entity2 = self.tm.create_entity(self.authority)
        rel_type = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        self.authority.set_entity_relationship_types([rel_type])
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['entity_relationships-0-relationship_type'] = \
            str(rel_type.get_id()) + FORWARD_RELATIONSHIP_MARKER
        form['entity_relationships-0-related_entity_1'] = entity2.get_id()
        form['entity_relationships-0-certainty'] = True
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['entity_relationship_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled entity relationship form')
        assertion = entity.get_entity_relationships()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['relationship_type'],
                         str(rel_type.get_id()) + FORWARD_RELATIONSHIP_MARKER)
        self.assertEqual(form_data['relationship_type'],
                         str(assertion.entity_relationship_type.get_id())
                         + FORWARD_RELATIONSHIP_MARKER)
        self.assertEqual(form_data['related_entity'], entity2.get_id())
        self.assertEqual(form_data['related_entity'],
                         assertion.range_entity.get_id())
        self.assertEqual(form_data['certainty'], True)
        self.assertEqual(assertion.certainty,
                         self.tm.property_assertion_full_certainty)
        # Test adding another entity relationship and deleting the
        # existing one.
        rel_type2 = self.create_entity_relationship_type(
            'is born in', 'is birth place of')
        self.authority.set_entity_relationship_types([rel_type, rel_type2])
        entity3 = self.tm.create_entity(self.authority)
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['entity_relationships-0-DELETE'] = 'on'
        form['entity_relationships-1-relationship_type'] = \
            str(rel_type2.get_id()) + REVERSE_RELATIONSHIP_MARKER
        form['entity_relationships-1-related_entity_1'] = entity3.get_id()
        form['entity_relationships-1-certainty'] = False
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['entity_relationship_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled entity relationship form')
        assertion = entity.get_entity_relationships()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['relationship_type'],
                         str(rel_type2.get_id()) + REVERSE_RELATIONSHIP_MARKER)
        self.assertEqual(form_data['relationship_type'],
                         str(assertion.entity_relationship_type.get_id())
                         + REVERSE_RELATIONSHIP_MARKER)
        self.assertEqual(form_data['related_entity'], entity3.get_id())
        self.assertEqual(form_data['related_entity'],
                         assertion.domain_entity.get_id())
        self.assertEqual(form_data['certainty'], False)
        self.assertEqual(assertion.certainty,
                         self.tm.property_assertion_no_certainty)
        # Test updating an existing entity relationship.
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['entity_relationships-0-relationship_type'] = \
            str(rel_type.get_id()) + FORWARD_RELATIONSHIP_MARKER
        form['entity_relationships-0-related_entity_1'] = entity2.get_id()
        form['entity_relationships-0-certainty'] = True
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['entity_relationship_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled entity relationship form')
        assertion = entity.get_entity_relationships()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['relationship_type'],
                         str(rel_type.get_id()) + FORWARD_RELATIONSHIP_MARKER)
        self.assertEqual(form_data['relationship_type'],
                         str(assertion.entity_relationship_type.get_id())
                         + FORWARD_RELATIONSHIP_MARKER)
        self.assertEqual(form_data['related_entity'], entity2.get_id())
        self.assertEqual(form_data['related_entity'],
                         assertion.range_entity.get_id())
        self.assertEqual(form_data['certainty'], True)
        self.assertEqual(assertion.certainty,
                         self.tm.property_assertion_full_certainty)

    def test_post_entity_types (self):
        entity = self.tm.create_entity(self.authority)
        entity_type = self.create_entity_type('Person')
        self.authority.set_entity_types([entity_type])
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['entity_types-0-entity_type'] = entity_type.get_id()
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['entity_type_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled entity type form')
        assertion = entity.get_entity_types()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['entity_type'], entity_type.get_id())
        self.assertEqual(form_data['entity_type'],
                         assertion.entity_type.get_id())
        # Test adding another entity type and deleting the existing one.
        entity_type2 = self.create_entity_type('Place')
        self.authority.set_entity_types([entity_type, entity_type2])
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['entity_types-0-DELETE'] = 'on'
        form['entity_types-1-entity_type'] = entity_type2.get_id()
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['entity_type_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled entity type form')
        assertion = entity.get_entity_types()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['entity_type'], entity_type2.get_id())
        self.assertEqual(form_data['entity_type'],
                         assertion.entity_type.get_id())
        # Test updating an existing entity type.
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['entity_types-0-entity_type'] = entity_type.get_id()
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['entity_type_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled entity type form')
        assertion = entity.get_entity_types()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['entity_type'], entity_type.get_id())
        self.assertEqual(form_data['entity_type'],
                         assertion.entity_type.get_id())

    def test_post_existences (self):
        entity = self.tm.create_entity(self.authority)
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        form = self.app.get(url, user='user').forms['entity-change-form']
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)

    def test_post_names (self):
        entity = self.tm.create_entity(self.authority)
        name_type = self.create_name_type('regular')
        language = self.create_language('English', 'en')
        script = self.create_script('Latin', 'Latn', ' ')
        self.authority.set_name_types([name_type])
        self.authority.set_languages([language])
        self.authority.set_scripts([script])
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['names-0-name_type'] = name_type.get_id()
        form['names-0-language'] = language.get_id()
        form['names-0-script'] = script.get_id()
        form['names-0-display_form'] = 'Carl Philipp Emanuel Bach'
        form['names-0-is_preferred'] = True
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['name_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled name form')
        assertion = entity.get_eats_names()[0]
        name = assertion.name
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['name_type'], name_type.get_id())
        self.assertEqual(form_data['name_type'], name.name_type.get_id())
        self.assertEqual(form_data['language'], language.get_id())
        self.assertEqual(form_data['language'], name.language.get_id())
        self.assertEqual(form_data['script'], script.get_id())
        self.assertEqual(form_data['script'], name.script.get_id())
        self.assertEqual(form_data['display_form'], 'Carl Philipp Emanuel Bach')
        self.assertEqual(form_data['display_form'], name.display_form)
        self.assertEqual(form_data['is_preferred'], assertion.is_preferred)
        # Test adding another name and deleting the existing one.
        name_type2 = self.create_name_type('irregular')
        language2 = self.create_language('Sanskrit', 'sa')
        script2 = self.create_script('Devanagari', 'Deva', ' ')
        self.authority.set_name_types([name_type, name_type2])
        self.authority.set_languages([language, language2])
        self.authority.set_scripts([script, script2])
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['names-0-DELETE'] = 'on'
        form['names-1-name_type'] = name_type2.get_id()
        form['names-1-language'] = language2.get_id()
        form['names-1-script'] = script2.get_id()
        form['names-1-display_form'] = 'पद्म'
        form['names-1-is_preferred'] = False
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['name_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled name form')
        assertion = entity.get_eats_names()[0]
        name = assertion.name
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['name_type'], name_type2.get_id())
        self.assertEqual(form_data['name_type'], name.name_type.get_id())
        self.assertEqual(form_data['language'], language2.get_id())
        self.assertEqual(form_data['language'], name.language.get_id())
        self.assertEqual(form_data['script'], script2.get_id())
        self.assertEqual(form_data['script'], name.script.get_id())
        self.assertEqual(form_data['display_form'], 'पद्म')
        self.assertEqual(form_data['display_form'], name.display_form)
        self.assertEqual(form_data['is_preferred'], assertion.is_preferred)
        # Test updating an existing name.
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['names-0-name_type'] = name_type.get_id()
        form['names-0-language'] = language.get_id()
        form['names-0-script'] = script.get_id()
        form['names-0-display_form'] = 'Isaac Fuller'
        form['names-0-is_preferred'] = True
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['name_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled name form')
        assertion = entity.get_eats_names()[0]
        name = assertion.name
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['name_type'], name_type.get_id())
        self.assertEqual(form_data['name_type'], name.name_type.get_id())
        self.assertEqual(form_data['language'], language.get_id())
        self.assertEqual(form_data['language'], name.language.get_id())
        self.assertEqual(form_data['script'], script.get_id())
        self.assertEqual(form_data['script'], name.script.get_id())
        self.assertEqual(form_data['display_form'], 'Isaac Fuller')
        self.assertEqual(form_data['display_form'], name.display_form)
        self.assertEqual(form_data['is_preferred'], assertion.is_preferred)

    def test_post_name_parts (self):
        entity = self.tm.create_entity(self.authority)
        name_type = self.create_name_type('regular')
        language = self.create_language('English', 'en')
        script = self.create_script('Latin', 'Latn', ' ')
        name_part_type = self.create_name_part_type('given')
        self.authority.set_name_types([name_type])
        self.authority.set_languages([language])
        self.authority.set_scripts([script])
        self.authority.set_name_part_types([name_part_type])
        self.assertEqual(Name.objects.count(), 0)
        self.assertEqual(NamePart.objects.count(), 0)
        # Not specifying a name part type should cause the creation of
        # both the name and name part to fail.
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['names-0-name_type'] = name_type.get_id()
        form['names-0-language'] = language.get_id()
        form['names-0-script'] = script.get_id()
        form['names-0-name_parts-0-name_part_display_form-0'] = 'Carl'
        form.submit('_save')
        self.assertEqual(Name.objects.count(), 0)
        self.assertEqual(NamePart.objects.count(), 0)
        form['names-0-name_parts-0-name_part_type'] = name_part_type.get_id()
        form.submit('_save')
        self.assertEqual(Name.objects.count(), 1)
        self.assertEqual(NamePart.objects.count(), 1)

    def test_post_notes (self):
        entity = self.tm.create_entity(self.authority)
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['notes-0-note'] = 'Test'
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['note_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled note form')
        self.assertEqual(entity.get_notes().count(), 1)
        assertion = entity.get_notes()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(assertion.authority.get_id(), self.authority_id)
        self.assertEqual(form_data['note'], assertion.note)
        self.assertEqual(form_data['note'], 'Test')
        # Test adding another note and deleting the existing one.
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['notes-0-DELETE'] = 'on'
        form['notes-1-note'] = 'Test 2'
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['note_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled note form')
        self.assertEqual(entity.get_notes().count(), 1)
        assertion = entity.get_notes()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['note'], assertion.note)
        self.assertEqual(form_data['note'], 'Test 2')
        # Test updating an existing note.
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['notes-0-note'] = 'Test'
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['note_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled note form')
        self.assertEqual(entity.get_notes().count(), 1)
        assertion = entity.get_notes()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['note'], assertion.note)
        self.assertEqual(form_data['note'], 'Test')

    def test_post_subject_identifiers (self):
        entity = self.tm.create_entity(self.authority)
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['subject_identifiers-1-subject_identifier'] = \
            'http://www.example.org/test'
        response = form.submit('_save', user='user').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['subject_identifier_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled subject identifier form')
        self.assertEqual(entity.get_subject_identifiers().count(), 1)
        assertion = entity.get_eats_subject_identifiers()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(assertion.authority.get_id(), self.authority_id)
        self.assertEqual(form_data['subject_identifier'],
                         assertion.subject_identifier)
        self.assertEqual(form_data['subject_identifier'],
                         'http://www.example.org/test')
        # Test adding another subject_identifier and deleting the
        # existing one.
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['subject_identifiers-0-DELETE'] = 'on'
        form['subject_identifiers-1-subject_identifier'] = \
            'http://www.example.org/test2'
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['subject_identifier_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled subject_identifier form')
        self.assertEqual(entity.get_eats_subject_identifiers().count(), 1)
        assertion = entity.get_eats_subject_identifiers()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['subject_identifier'],
                         assertion.subject_identifier)
        self.assertEqual(form_data['subject_identifier'],
                         'http://www.example.org/test2')
        # Test updating an existing subject_identifier.
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['subject_identifiers-0-subject_identifier'] = \
            'http://www.example.org/test3'
        response = form.submit('_save').follow()
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         url)
        formset = response.context['subject_identifier_formset']
        self.assertEqual(formset.initial_form_count(), 1,
                         'Expected one pre-filled subject_identifier form')
        self.assertEqual(entity.get_eats_subject_identifiers().count(), 1)
        assertion = entity.get_eats_subject_identifiers()[0]
        form_data = formset.initial_forms[0].initial
        self.assertEqual(form_data['assertion'], assertion.get_id())
        self.assertEqual(self.authority_id, assertion.authority.get_id())
        self.assertEqual(form_data['subject_identifier'],
                         assertion.subject_identifier)
        self.assertEqual(form_data['subject_identifier'],
                         'http://www.example.org/test3')

    def test_post_subject_identifiers_illegal (self):
        entity1 = self.tm.create_entity(self.authority)
        self.assertEqual(entity1.get_eats_subject_identifiers().count(), 0)
        url = reverse('entity-change', kwargs={'entity_id': entity1.get_id()})
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['subject_identifiers-0-subject_identifier'] = \
            'http://www.example.org/test'
        form['subject_identifiers-1-subject_identifier'] = \
            'http://www.example.org/test'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(entity1.get_eats_subject_identifiers().count(), 0)
        entity2 = self.tm.create_entity(self.authority)
        entity2.create_subject_identifier_property_assertion(
            self.authority, 'http://www.example.org/test')
        form = self.app.get(url, user='user').forms['entity-change-form']
        form['subject_identifiers-0-subject_identifier'] = \
            'http://www.example.org/test'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(entity1.get_eats_subject_identifiers().count(), 0)
