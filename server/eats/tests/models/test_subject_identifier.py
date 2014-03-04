from eats.tests.models.model_test_case import ModelTestCase


class SubjectIdentifierTestCase (ModelTestCase):

    def setUp (self):
        super(SubjectIdentifierTestCase, self).setUp()
        self.entity = self.tm.create_entity(self.authority)

    def test_create_subject_identifier_property_assertion (self):
        self.assertEqual(0, self.entity.get_eats_subject_identifiers().count())
        assertion = self.entity.create_subject_identifier_property_assertion(
            self.authority, 'http://www.example.org/test')
        self.assertEqual(1, self.entity.get_eats_subject_identifiers().count())
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(assertion.subject_identifier,
                         'http://www.example.org/test')
        fetched_assertion = self.entity.get_eats_subject_identifiers()[0]
        self.assertEqual(assertion, fetched_assertion)

    def test_delete_subject_identifier_property_assertion (self):
        self.assertEqual(0, self.entity.get_eats_subject_identifiers().count())
        assertion1 = self.entity.create_subject_identifier_property_assertion(
            self.authority, 'http://www.example.org/test')
        self.assertEqual(1, self.entity.get_eats_subject_identifiers().count())
        assertion2 = self.entity.create_subject_identifier_property_assertion(
            self.authority, 'http://www.example.org/test2')
        self.assertEqual(2, self.entity.get_eats_subject_identifiers().count())
        assertion2.remove()
        self.assertEqual(1, self.entity.get_eats_subject_identifiers().count())
        assertion1.remove()
        self.assertEqual(0, self.entity.get_eats_subject_identifiers().count())

    def test_update_subject_identifier_property_assertion (self):
        assertion = self.entity.create_subject_identifier_property_assertion(
            self.authority, 'http://www.example.org/test')
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(assertion.subject_identifier,
                         'http://www.example.org/test')
        assertion.update('http://www.example.org/test2')
        self.assertEqual(assertion.subject_identifier,
                         'http://www.example.org/test2')

    def test_get_duplicate_subject_identifiers (self):
        subject_identifier = 'http://www.example.org/test'
        duplicates = self.entity.get_duplicate_subject_identifiers(
            subject_identifier)
        self.assertEqual(duplicates.count(), 0)
        self.entity.create_subject_identifier_property_assertion(
            self.authority, subject_identifier)
        self.assertEqual(duplicates.count(), 0)
        entity2 = self.tm.create_entity(self.authority)
        entity3 = self.tm.create_entity(self.authority)
        authority2 = self.create_authority('Test 2')
        entity2.create_subject_identifier_property_assertion(
            self.authority, subject_identifier)
        entity3.create_subject_identifier_property_assertion(
            authority2, subject_identifier)
        duplicates = self.entity.get_duplicate_subject_identifiers(
            subject_identifier)
        self.assertEqual(duplicates.count(), 2)
        self.assertTrue(entity2 in duplicates)
        self.assertTrue(entity3 in duplicates)
        duplicates = self.entity.get_duplicate_subject_identifiers(
            subject_identifier, self.authority)
        self.assertEqual(duplicates.count(), 1)
        self.assertTrue(entity2 in duplicates)
