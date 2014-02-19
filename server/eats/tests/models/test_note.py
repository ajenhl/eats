from eats.tests.models.model_test_case import ModelTestCase


class NoteTestCase (ModelTestCase):

    def setUp (self):
        super(NoteTestCase, self).setUp()
        self.entity = self.tm.create_entity(self.authority)

    def test_create_note_property_assertion (self):
        self.assertEqual(0, self.entity.get_notes().count())
        assertion = self.entity.create_note_property_assertion(
            self.authority, 'Test')
        self.assertEqual(1, self.entity.get_notes().count())
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(assertion.note, 'Test')
        fetched_assertion = self.entity.get_notes()[0]
        self.assertEqual(assertion, fetched_assertion)

    def test_delete_note_property_assertion (self):
        self.assertEqual(0, self.entity.get_notes().count())
        assertion1 = self.entity.create_note_property_assertion(
            self.authority, 'Test')
        self.assertEqual(1, self.entity.get_notes().count())
        assertion2 = self.entity.create_note_property_assertion(
            self.authority, 'Test 2')
        self.assertEqual(2, self.entity.get_notes().count())
        assertion2.remove()
        self.assertEqual(1, self.entity.get_notes().count())
        assertion1.remove()
        self.assertEqual(0, self.entity.get_notes().count())

    def test_update_note_property_assertion (self):
        assertion = self.entity.create_note_property_assertion(
            self.authority, 'Test')
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(assertion.note, 'Test')
        assertion.update('Test2')
        self.assertEqual(assertion.note, 'Test2')
