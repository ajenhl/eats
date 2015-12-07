from eats.tests.models.model_test_case import ModelTestCase


class NoteBearingTestCase (ModelTestCase):

    def setUp (self):
        super(NoteBearingTestCase, self).setUp()
        self.entity = self.tm.create_entity(self.authority)
        django_user = self.create_django_user('test', 'test@example.org',
                                              'password')
        self.user = self.create_user(django_user)
        self.user.editable_authorities.add(self.authority)

    def test_assertion_note_editor (self):
        existence = self.entity.create_existence_property_assertion(
            self.authority)
        self.assertEqual(len(existence.get_notes(self.user)), 0)
        note = existence.create_note('Test', True)
        notes = existence.get_notes(self.user)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], note)
        self.assertEqual(notes[0].note, 'Test')
        self.assertEqual(notes[0].is_internal, True)
        got_note = existence.get_note(self.user, note.get_id())
        self.assertEqual(got_note, note)

    def test_assertion_note_non_editor (self):
        existence = self.entity.create_existence_property_assertion(
            self.authority)
        self.assertEqual(len(existence.get_notes(None)), 0)
        note = existence.create_note('Test', True)
        self.assertEqual(len(existence.get_notes(None)), 0)
        note2 = existence.create_note('Test2', False)
        notes = existence.get_notes(None)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].note, 'Test2')
        self.assertEqual(notes[0].is_internal, False)
        got_note = existence.get_note(None, note.get_id())
        self.assertIsNone(got_note)
        got_note2 = existence.get_note(None, note2.get_id())
        self.assertEqual(got_note2, note2)

    def test_date_note_editor (self):
        existence = self.entity.create_existence_property_assertion(
            self.authority)
        date_period = self.create_date_period('lifespan')
        self.authority.set_date_periods([date_period])
        date = existence.create_date({'date_period': date_period})
        self.assertEqual(len(date.get_notes(self.user)), 0)
        note = date.create_note('Test', True)
        notes = date.get_notes(self.user)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0], note)
        self.assertEqual(notes[0].note, 'Test')
        self.assertEqual(notes[0].is_internal, True)
        got_note = date.get_note(self.user, note.get_id())
        self.assertEqual(got_note, note)

    def test_date_note_non_editor (self):
        existence = self.entity.create_existence_property_assertion(
            self.authority)
        date_period = self.create_date_period('lifespan')
        self.authority.set_date_periods([date_period])
        date = existence.create_date({'date_period': date_period})
        self.assertEqual(len(date.get_notes(None)), 0)
        note = date.create_note('Test', True)
        self.assertEqual(len(date.get_notes(None)), 0)
        note2 = date.create_note('Test2', False)
        notes = date.get_notes(None)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].note, 'Test2')
        self.assertEqual(notes[0].is_internal, False)
        got_note = date.get_note(None, note.get_id())
        self.assertIsNone(got_note)
        got_note2 = date.get_note(None, note2.get_id())
        self.assertEqual(got_note2, note2)
