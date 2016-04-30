from django.conf import settings
from django.core.urlresolvers import reverse

from eats.tests.views.view_test_case import ViewTestCase


class NoteAddViewTestCase (ViewTestCase):

    def setUp (self):
        super().setUp()
        self.authority_id = self.authority.get_id()
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.editor.set_current_authority(self.authority)
        self.date_period = self.create_date_period('lifespan')
        self.authority.set_date_periods([self.date_period])

    def test_authentication_assertion (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        url = reverse('eats-pa-note-add', kwargs={
            'entity_id': entity.get_id(), 'assertion_id': existence.get_id()})
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
        response = self.app.get(url, status=404, user='user2')

    def test_authentication_date (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date = existence.create_date({'date_period': self.date_period})
        url = reverse('eats-date-note-add', kwargs={
            'entity_id': entity.get_id(), 'assertion_id': existence.get_id(),
            'date_id': date.get_id()})
        login_url = settings.LOGIN_URL + '?next=' + url
        response = self.app.get(url)
        self.assertRedirects(response, login_url)
        user = self.create_django_user('user2', 'user2@example.org', 'password')
        eats_user = self.create_user(user)
        response = self.app.get(url, user='user2')
        self.assertRedirects(response, login_url)
        authority = self.create_authority('Test2')
        eats_user.editable_authorities = [self.authority, authority]
        eats_user.set_current_authority(authority)
        response = self.app.get(url, status=404, user='user2')

    def test_non_matching_pa_note_add (self):
        """Tests that the entity and assertion match when adding a
        note to a property assertion."""
        url_args = {'entity_id': 0, 'assertion_id': 0}
        # Test with non-existent entity and assertion.
        self.app.get(reverse('eats-pa-note-add', kwargs=url_args), status=404,
                     user='user')
        # Test with non-existent assertion.
        entity = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity.get_id()
        self.app.get(reverse('eats-pa-note-add', kwargs=url_args), status=404,
                     user='user')
        # Test with the assertion not belonging to the entity.
        entity2 = self.tm.create_entity(self.authority)
        assertion = entity2.get_existences()[0]
        url_args['assertion_id'] = assertion.get_id()
        self.app.get(reverse('eats-pa-note-add', kwargs=url_args), status=404,
                     user='user')

    def test_non_matching_date_note_add (self):
        """Tests that the entity, assertion and date match when adding a note
        to a date."""
        url_args = {'entity_id': 0, 'assertion_id': 0, 'date_id': 0}
        # Test with non-existent entity, assertion and date.
        self.app.get(reverse('eats-date-note-add', kwargs=url_args), status=404,
                     user='user')
        # Test with non-existent assertion and date.
        entity = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity.get_id()
        self.app.get(reverse('eats-date-note-add', kwargs=url_args), status=404,
                     user='user')
        # Test with non-existent date.
        existence = entity.get_existences()[0]
        url_args['assertion_id'] = existence.get_id()
        self.app.get(reverse('eats-date-note-add', kwargs=url_args), status=404,
                     user='user')
        date = existence.create_date({'date_period': self.date_period})
        url_args['date_id'] = date.get_id()
        # Test with the assertion not belonging to the entity.
        entity2 = self.tm.create_entity(self.authority)
        url_args['entity_id'] = entity2.get_id()
        self.app.get(reverse('eats-date-note-add', kwargs=url_args), status=404,
                     user='user')
        # Test with the date not belonging to the assertion.
        existence2 = entity2.get_existences()[0]
        url_args['assertion_id'] = existence2.get_id()
        self.app.get(reverse('eats-date-note-add', kwargs=url_args), status=404,
                     user='user')

    def test_wrong_assertion_type (self):
        """Tests that the assertion is one of those types that may bear
        notes."""
        entity = self.tm.create_entity(self.authority)
        note_pa = entity.create_note_property_assertion(self.authority, 'Test',
                                                        False)
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': note_pa.get_id()}
        self.app.get(reverse('eats-pa-note-add', kwargs=url_args), status=404,
                     user='user')
        si_pa = entity.create_subject_identifier_property_assertion(
            self.authority, 'http://www.example.org/')
        url_args['assertion_id'] = si_pa.get_id()
        self.app.get(reverse('eats-pa-note-add', kwargs=url_args), status=404,
                     user='user')

    def test_get_request_assertion (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        url = reverse('eats-pa-note-add', kwargs={
            'entity_id': entity.get_id(), 'assertion_id': existence.get_id()})
        response = self.app.get(url, user='user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/note_add.html')

    def test_get_request_date (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date = existence.create_date({'date_period': self.date_period})
        url = reverse('eats-date-note-add', kwargs={
            'entity_id': entity.get_id(), 'assertion_id': existence.get_id(),
            'date_id': date.get_id()})
        response = self.app.get(url, user='user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/note_add.html')

    def test_pa_valid_post_request_continue (self):
        response, url_args = self._post_valid_pa_note('_continue')
        redirect_url = reverse('eats-pa-note-change', kwargs=url_args)
        self.assertRedirects(response, redirect_url)

    def test_pa_valid_post_request_save (self):
        response, url_args = self._post_valid_pa_note('_save')
        del url_args['note_id']
        del url_args['assertion_id']
        redirect_url = reverse('eats-entity-change', kwargs=url_args)
        self.assertRedirects(response, redirect_url)

    def _post_valid_pa_note (self, submit_name):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        self.assertEqual(len(existence.get_notes(self.editor)), 0)
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': existence.get_id()}
        url = reverse('eats-pa-note-add', kwargs=url_args)
        form = self.app.get(url, user='user').forms['note-add-form']
        form['note'] = 'Test'
        form['is_internal'] = 'on'
        response = form.submit(submit_name)
        existence = entity.get_existences()[0]
        notes = existence.get_notes(self.editor)
        self.assertEqual(len(notes), 1)
        note = notes[0]
        self.assertEqual(note.note, 'Test')
        self.assertEqual(note.is_internal, True)
        url_args['note_id'] = note.get_id()
        return response, url_args

    def test_date_valid_post_request_continue (self):
        response, url_args = self._post_valid_date_note('_continue')
        redirect_url = reverse('eats-date-note-change', kwargs=url_args)
        self.assertRedirects(response, redirect_url)

    def test_date_valid_post_request_save (self):
        response, url_args = self._post_valid_date_note('_save')
        del url_args['note_id']
        redirect_url = reverse('eats-date-change', kwargs=url_args)
        self.assertRedirects(response, redirect_url)

    def _post_valid_date_note (self, submit_name):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        date = existence.create_date({'date_period': self.date_period})
        self.assertEqual(len(date.get_notes(self.editor)), 0)
        url_args = {'entity_id': entity.get_id(),
                    'assertion_id': existence.get_id(),
                    'date_id': date.get_id()}
        url = reverse('eats-date-note-add', kwargs=url_args)
        form = self.app.get(url, user='user').forms['note-add-form']
        form['note'] = 'Test'
        form['is_internal'] = 'on'
        response = form.submit(submit_name)
        date = existence.get_dates()[0]
        notes = date.get_notes(self.editor)
        self.assertEqual(len(notes), 1)
        note = notes[0]
        self.assertEqual(note.note, 'Test')
        self.assertEqual(note.is_internal, True)
        url_args['note_id'] = note.get_id()
        return response, url_args
