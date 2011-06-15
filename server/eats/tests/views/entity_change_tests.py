# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from eats.tests.base_test_case import BaseTestCase


class EntityChangeViewTestCase (BaseTestCase):

    def test_non_existent_entity (self):
        # Use the authority topic as an example of a non-existent
        # entity. Immediately after setUp it will not be marked as an
        # entity.
        response = self.client.get(reverse(
                'entity-change', kwargs={'entity_id': self.authority.get_id()}))
        self.assertEqual(
            response.status_code, 404,
            'Expected a 404 HTTP response code for a non-existent entity')
    
    def test_empty_entity (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        response = self.client.get(reverse(
                'entity-change', kwargs={'entity_id': entity.get_id()}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/entity_change.html')
        # A newly created entity will have one existence property
        # assertion, and no other property assertions.
        existence_formset = response.context['existence_formset']
        self.assertEqual(existence_formset.initial_form_count(), 1,
                         'Expected one pre-filled existence form')
        existence_data = existence_formset.initial_forms[0].initial
        self.assertEqual(existence_data['assertion'], existence.get_id())
        self.assertEqual(existence_data['authority'],
                         entity.get_authority(existence).get_id())
        for formset in ('entity_type_formset', 'entity_relationship_formset',
                        'name_formset', 'note_formset'):
            self.assertEqual(response.context[formset].initial_form_count(), 0,
                             'Expected no %ss' % formset)

    def test_post_existences (self):
        # QAZ: Need to sort out whether existences are special in
        # terms of being required in order to make other property
        # assertions under an authority.
        pass
            
    def test_post_entity_types (self):
        entity = self.tm.create_entity(self.authority)
        authority_id = self.authority.get_id()
        existence = entity.get_existences()[0]
        entity_type = self.create_entity_type('Person')
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        response = self.client.post(url, {
                'existences-TOTAL_FORMS': 2, 'existences-INITIAL_FORMS': 1,
                'existences-0-assertion': existence.get_id(),
                'existences-0-authority': authority_id,
                'entity_types-TOTAL_FORMS': 1, 'entity_types-INITIAL_FORMS': 0,
                'entity_types-0-authority': authority_id,
                'entity_types-0-entity_type': entity_type.get_id(),
                'names-TOTAL_FORMS': 1, 'names-INITIAL_FORMS': 0,
                'entity_relationships-TOTAL_FORMS': 1,
                'entity_relationships-INITIAL_FORMS': 0,
                'notes-TOTAL_FORMS': 1, 'notes-INITIAL_FORMS': 0,
                '_save': 'Save'}, follow=True)
        self.assertRedirects(response, url)
        entity_type_formset = response.context['entity_type_formset']
        self.assertEqual(entity_type_formset.initial_form_count(), 1,
                         'Expected one pre-filled entity type form')
        entity_type_assertion = entity.get_entity_types()[0]
        entity_type_data = entity_type_formset.initial_forms[0].initial
        self.assertEqual(entity_type_data['assertion'],
                         entity_type_assertion.get_id())
        self.assertEqual(entity_type_data['authority'],
                         entity.get_authority(entity_type_assertion).get_id())
        self.assertEqual(entity_type_data['entity_type'], entity_type.get_id())
        # Test adding another entity type and deleting the existing one.
        entity_type2 = self.create_entity_type('Place')
        response = self.client.post(url, {
                'existences-TOTAL_FORMS': 2, 'existences-INITIAL_FORMS': 1,
                'existences-0-assertion': existence.get_id(),
                'existences-0-authority': authority_id,
                'entity_types-TOTAL_FORMS': 2, 'entity_types-INITIAL_FORMS': 1,
                'entity_types-0-DELETE': 'on',
                'entity_types-0-assertion': entity_type_assertion.get_id(),
                'entity_types-0-authority': authority_id,
                'entity_types-0-entity_type': entity_type.get_id(),
                'entity_types-1-authority': authority_id,
                'entity_types-1-entity_type': entity_type2.get_id(),
                'names-TOTAL_FORMS': 1, 'names-INITIAL_FORMS': 0,
                'entity_relationships-TOTAL_FORMS': 1,
                'entity_relationships-INITIAL_FORMS': 0,
                'notes-TOTAL_FORMS': 1, 'notes-INITIAL_FORMS': 0,
                '_save': 'Save'}, follow=True)
        self.assertRedirects(response, url)
        entity_type_formset = response.context['entity_type_formset']
        self.assertEqual(entity_type_formset.initial_form_count(), 1,
                         'Expected one pre-filled entity type form')
        entity_type_assertion = entity.get_entity_types()[0]
        entity_type_data = entity_type_formset.initial_forms[0].initial
        self.assertEqual(entity_type_data['assertion'],
                         entity_type_assertion.get_id())
        self.assertEqual(entity_type_data['authority'],
                         entity.get_authority(entity_type_assertion).get_id())
        self.assertEqual(entity_type_data['entity_type'], entity_type2.get_id())

    def test_post_names (self):
        entity = self.tm.create_entity(self.authority)
        authority_id = self.authority.get_id()
        existence = entity.get_existences()[0]
        name_type = self.create_name_type('regular')
        language = self.create_language('English', 'en')
        script = self.create_script('Latin', 'Latn')
        url = reverse('entity-change', kwargs={'entity_id': entity.get_id()})
        response = self.client.post(url, {
                'existences-TOTAL_FORMS': 2, 'existences-INITIAL_FORMS': 1,
                'existences-0-assertion': existence.get_id(),
                'existences-0-authority': authority_id,
                'entity_types-TOTAL_FORMS': 1, 'entity_types-INITIAL_FORMS': 0,
                'names-TOTAL_FORMS': 1, 'names-INITIAL_FORMS': 0,
                'names-0-authority': authority_id,
                'names-0-name_type': name_type.get_id(),
                'names-0-language': language.get_id(),
                'names-0-script': script.get_id(),
                'names-0-display_form': 'Carl Philipp Emanuel Bach',
                'entity_relationships-TOTAL_FORMS': 1,
                'entity_relationships-INITIAL_FORMS': 0,
                'notes-TOTAL_FORMS': 1, 'notes-INITIAL_FORMS': 0,
                '_save': 'Save'}, follow=True)
        self.assertRedirects(response, url)
        name_formset = response.context['name_formset']
        self.assertEqual(name_formset.initial_form_count(), 1,
                         'Expected one pre-filled name form')
        name_assertion = entity.get_eats_names()[0]
        name_data = name_formset.initial_forms[0].initial
        self.assertEqual(name_data['assertion'], name_assertion.get_id())
        self.assertEqual(name_data['authority'], entity.get_authority(
                name_assertion).get_id())
        self.assertEqual(name_data['name_type'], name_type.get_id())
        self.assertEqual(name_data['language'], language.get_id())
        self.assertEqual(name_data['script'], script.get_id())
        name = entity.get_entity_name(name_assertion)
        self.assertEqual(name_data['display_form'], name.name_value)
        name_type2 = self.create_name_type('irregular')
        language2 = self.create_language('Sanskrit', 'sa')
        script2 = self.create_script('Devanagari', 'Deva')
        response = self.client.post(url, {
                'existences-TOTAL_FORMS': 2, 'existences-INITIAL_FORMS': 1,
                'existences-0-assertion': existence.get_id(),
                'existences-0-authority': authority_id,
                'entity_types-TOTAL_FORMS': 1, 'entity_types-INITIAL_FORMS': 0,
                'names-TOTAL_FORMS': 2, 'names-INITIAL_FORMS': 1,
                'names-0-DELETE': 'on', 'names-0-authority': authority_id,
                'names-0-assertion': name_assertion.get_id(),
                'names-0-name_type': name_type.get_id(),
                'names-0-language': language.get_id(),
                'names-0-script': script.get_id(),
                'names-0-display_form': 'Carl Philipp Emanuel Bach',
                'names-1-authority': authority_id,
                'names-1-name_type': name_type2.get_id(),
                'names-1-language': language2.get_id(),
                'names-1-script': script2.get_id(),
                'names-1-display_form': u'पद्म',
                'entity_relationships-TOTAL_FORMS': 1,
                'entity_relationships-INITIAL_FORMS': 0,
                'notes-TOTAL_FORMS': 1, 'notes-INITIAL_FORMS': 0,
                '_save': 'Save'}, follow=True)
        self.assertRedirects(response, url)
        name_formset = response.context['name_formset']
        self.assertEqual(name_formset.initial_form_count(), 1,
                         'Expected one pre-filled name form')
        name_assertion = entity.get_eats_names()[0]
        name_data = name_formset.initial_forms[0].initial
        self.assertEqual(name_data['assertion'], name_assertion.get_id())
        self.assertEqual(name_data['authority'], entity.get_authority(
                name_assertion).get_id())
        self.assertEqual(name_data['name_type'], name_type2.get_id())
        self.assertEqual(name_data['language'], language2.get_id())
        self.assertEqual(name_data['script'], script2.get_id())
        name = entity.get_entity_name(name_assertion)
        self.assertEqual(name_data['display_form'], name.name_value)
