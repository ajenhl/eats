from eats.models import Authority
from eats.tests.base_test_case import BaseTestCase


class EATSTopicMapTestCase (BaseTestCase):

    def test_create_authority (self):
        self.assertEqual(Authority.objects.count(), 1)
        authority1 = self.tm.create_authority('Test1')
        self.assertEqual(Authority.objects.count(), 2)
        self.assertTrue(authority1 in Authority.objects.all())
        self.assertRaises(Exception, self.tm.create_authority, 'Test1')
        
