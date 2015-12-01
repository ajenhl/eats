from eats.tests.models.model_test_case import ModelTestCase


class NoteTestCase (ModelTestCase):

    def setUp (self):
        super(NoteTestCase, self).setUp()
        self.entity = self.tm.create_entity(self.authority)

    def test_create_note_property_assertion (self):
        self.assertEqual(0, self.entity.get_notes_all().count())
        assertion = self.entity.create_note_property_assertion(
            self.authority, 'Test', True)
        self.assertEqual(1, self.entity.get_notes_all().count())
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(assertion.note, 'Test')
        self.assertEqual(assertion.is_internal, True)
        fetched_assertion = self.entity.get_notes_all()[0]
        self.assertEqual(assertion, fetched_assertion)

    def test_delete_note_property_assertion (self):
        self.assertEqual(0, self.entity.get_notes_all().count())
        assertion1 = self.entity.create_note_property_assertion(
            self.authority, 'Test')
        self.assertEqual(1, self.entity.get_notes_all().count())
        assertion2 = self.entity.create_note_property_assertion(
            self.authority, 'Test 2')
        self.assertEqual(2, self.entity.get_notes_all().count())
        assertion2.remove()
        self.assertEqual(1, self.entity.get_notes_all().count())
        assertion1.remove()
        self.assertEqual(0, self.entity.get_notes_all().count())

    def test_update_note_property_assertion (self):
        assertion = self.entity.create_note_property_assertion(
            self.authority, 'Test', True)
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(assertion.note, 'Test')
        self.assertEqual(assertion.is_internal, True)
        assertion.update('Test2', False)
        self.assertEqual(assertion.note, 'Test2')
        self.assertEqual(assertion.is_internal, False)
