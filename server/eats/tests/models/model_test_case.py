from django.test import TransactionTestCase

from eats.tests.base_test_case import BaseTestCase


class ModelTestCase (TransactionTestCase, BaseTestCase):

    def setUp (self):
        # Create a topic map.
        self.tm = self.create_topic_map()
        # Create an authority.
        self.authority = self.create_authority('Test')

