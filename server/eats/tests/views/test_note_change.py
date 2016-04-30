from django.conf import settings
from django.core.urlresolvers import reverse

from eats.tests.views.view_test_case import ViewTestCase


class NoteChangeViewTestCase (ViewTestCase):

    def setUp (self):
        super().setUp()
        self.date_period = self.create_date_period('lifespan')
        self.authority.set_date_periods([self.date_period])
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.editor.set_current_authority(self.authority)

    def test_authentication_assertion (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        note = existence.create_note('Test', False)
        url_args = {'entity_id': entity.get_id(), 'note_id': note.get_id(),
                    'assertion_id': existence.get_id()}
        url = reverse('eats-pa-note-change', kwargs=url_args)
        self._authenticate_request(url)

    def test_authentication_date (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date = existence.create_date({'date_period': self.date_period})
        note = date.create_note('Test', False)
        url_args = {'entity_id': entity.get_id(), 'date_id': date.get_id(),
                    'assertion_id': existence.get_id(),
                    'note_id': note.get_id()}
        url = reverse('eats-date-note-change', kwargs=url_args)
        self._authenticate_request(url)

    def _authenticate_request (self, url):
        login_url = settings.LOGIN_URL + '?next=' + url
        response = self.app.get(url)
        self.assertRedirects(response, login_url)
        user = self.create_django_user('user2', 'user2@example.org', 'password')
        response = self.app.get(url, user='user2')
        self.assertRedirects(response, login_url)
        eats_user = self.create_user(user)
        response = self.app.get(url, user='user2')
        self.assertRedirects(response, login_url)
        authority = self.create_authority('Test2')
        eats_user.editable_authorities = [self.authority, authority]
        eats_user.set_current_authority(authority)
        self.app.get(url, status=404, user='user2')

    def test_non_matching_pa_note_change (self):
        """Tests that the entity, assertion and note match when editing an
        assertion's note."""
        # Test with none of entity, assertion, and note existing.
        url_args = {'entity_id': 0, 'assertion_id': 0, 'note_id': 0}
        self.app.get(reverse('eats-pa-note-change', kwargs=url_args),
                     status=404, user='user')
        # Test with only the entity existing.
        entity = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity.get_id()
        self.app.get(reverse('eats-pa-note-change', kwargs=url_args),
                     status=404, user='user')
        # Test with only the entity and assertion existing.
        assertion = entity.get_existences()[0]
        url_args['assertion_id'] = assertion.get_id()
        self.app.get(reverse('eats-pa-note-change', kwargs=url_args),
                     status=404, user='user')
        # Test that the assertion must be associated with the entity.
        note = assertion.create_note('Test', True)
        url_args['note_id'] = note.get_id()
        entity2 = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity2.get_id()
        self.app.get(reverse('eats-pa-note-change', kwargs=url_args),
                     status=404, user='user')
        # Test that the note must be associated with the assertion.
        url_args['entity_id'] = entity.get_id()
        note2 = entity2.get_existences()[0].create_note('Test', True)
        url_args['note_id'] = note2.get_id()
        self.app.get(reverse('eats-pa-note-change', kwargs=url_args),
                     status=404, user='user')

    def test_non_matching_date_note_change (self):
        """Tests that the entity, assertion, date and note match when
        editing a date's note."""
        # Test with none of entity, assertion, date and note existing.
        url_args = {'entity_id': 0, 'assertion_id': 0, 'date_id': 0,
                    'note_id': 0}
        self.app.get(reverse('eats-date-note-change', kwargs=url_args),
                     status=404, user='user')
        # Test with only the entity existing.
        entity = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity.get_id()
        self.app.get(reverse('eats-date-note-change', kwargs=url_args),
                     status=404, user='user')
        # Test with only the entity and assertion existing.
        assertion = entity.get_existences()[0]
        url_args['assertion_id'] = assertion.get_id()
        self.app.get(reverse('eats-date-note-change', kwargs=url_args),
                     status=404, user='user')
        # Test that the assertion must be associated with the entity.
        date = assertion.create_date({'date_period': self.date_period})
        url_args['date_id'] = date.get_id()
        entity2 = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity2.get_id()
        self.app.get(reverse('eats-date-note-change', kwargs=url_args),
                     status=404, user='user')
        # Test that the date must be associated with the assertion.
        assertion2 = entity2.get_existences()[0]
        url_args['assertion_id'] = assertion2.get_id()
        self.app.get(reverse('eats-date-note-change', kwargs=url_args),
                     status=404, user='user')
        # Test that the note must be associated with the date.
        date2 = assertion.create_date({'date_period': self.date_period})
        note = date2.create_note('Test', True)
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': assertion.get_id(),
                    'date_id': date.get_id(),
                    'note_id': note.get_id()}
        self.app.get(reverse('eats-date-note-change', kwargs=url_args),
                     status=404, user='user')

    def test_get_request_pa (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        note = existence.create_note('Test', True)
        url = reverse('eats-pa-note-change', kwargs={
            'entity_id': entity.get_id(), 'assertion_id': existence.get_id(),
            'note_id': note.get_id()})
        response = self.app.get(url, user='user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/note_change.html')

    def test_get_request_date (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date = existence.create_date({'date_period': self.date_period})
        note = date.create_note('Test', True)
        url = reverse('eats-date-note-change', kwargs={
            'entity_id': entity.get_id(), 'assertion_id': existence.get_id(),
            'date_id': date.get_id(), 'note_id': note.get_id()})
        response = self.app.get(url, user='user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/note_change.html')

    def test_valid_post_request_pa (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        note = existence.create_note('Test', True)
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': existence.get_id(),
                    'note_id': note.get_id()}
        url = reverse('eats-pa-note-change', kwargs=url_args)
        form = self.app.get(url, user='user').forms['note-change-form']
        form['note'] = 'Altered'
        form['is_internal'] = False
        response = form.submit('_continue')
        self.assertRedirects(response, url)
        note = existence.get_notes(self.editor)[0]
        self.assertEqual(note.note, 'Altered')
        self.assertEqual(note.is_internal, False)
        form['note'] = 'Altered again'
        form['is_internal'] = True
        response = form.submit('_save')
        url2 = reverse('eats-entity-change',
                       kwargs={'entity_id': entity.get_id()})
        self.assertRedirects(response, url2)
        note = existence.get_notes(self.editor)[0]
        self.assertEqual(note.note, 'Altered again')
        self.assertEqual(note.is_internal, True)

    def test_valid_post_request_date (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date_data = {'date_period': self.date_period}
        date = existence.create_date(date_data)
        note = date.create_note('Test', True)
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': existence.get_id(),
                    'date_id': date.get_id(), 'note_id': note.get_id()}
        url = reverse('eats-date-note-change', kwargs=url_args)
        form = self.app.get(url, user='user').forms['note-change-form']
        form['note'] = 'Altered'
        form['is_internal'] = False
        response = form.submit('_continue')
        self.assertRedirects(response, url)
        note = date.get_notes(self.editor)[0]
        self.assertEqual(note.note, 'Altered')
        self.assertEqual(note.is_internal, False)
        form['note'] = 'Altered again'
        form['is_internal'] = True
        response = form.submit('_save')
        del url_args['note_id']
        url2 = reverse('eats-date-change', kwargs=url_args)
        self.assertRedirects(response, url2)
        note = date.get_notes(self.editor)[0]
        self.assertEqual(note.note, 'Altered again')
        self.assertEqual(note.is_internal, True)

    def test_delete_pa (self):
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(1, len(entity.get_existences()))
        existence = entity.get_existences()[0]
        self.assertEqual(0, len(existence.get_notes(self.editor)))
        note = existence.create_note('Test', True)
        self.assertEqual(1, len(existence.get_notes(self.editor)))
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': existence.get_id(),
                    'note_id': note.get_id()}
        url = reverse('eats-pa-note-change', kwargs=url_args)
        form = self.app.get(url, user='user').forms['note-change-form']
        response = form.submit('_delete')
        url2 = reverse('eats-entity-change',
                       kwargs={'entity_id': entity.get_id()})
        self.assertRedirects(response, url2)
        self.assertEqual(0, len(existence.get_notes(self.editor)))
        self.assertEqual(1, len(entity.get_existences()))
        self.app.get(url, status=404, user='user')

    def test_delete_date (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date_data = {'date_period': self.date_period}
        date = existence.create_date(date_data)
        self.assertEqual(1, len(existence.get_dates()))
        note = date.create_note('Test', True)
        self.assertEqual(1, len(date.get_notes(self.editor)))
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': existence.get_id(),
                    'date_id': date.get_id(), 'note_id': note.get_id()}
        url = reverse('eats-date-note-change', kwargs=url_args)
        form = self.app.get(url, user='user').forms['note-change-form']
        response = form.submit('_delete')
        del url_args['note_id']
        url2 = reverse('eats-date-change', kwargs=url_args)
        self.assertRedirects(response, url2)
        self.assertEqual(0, len(date.get_notes(self.editor)))
        self.assertEqual(1, len(existence.get_dates()))
        self.app.get(url, status=404, user='user')
