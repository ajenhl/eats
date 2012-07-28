from django.test import TestCase, TransactionTestCase

from eats.tests.base_test_case import BaseTestCase


class ModelTestCase (TestCase, BaseTestCase):

    def setUp (self):
        super(ModelTestCase, self).setUp()
        self.reset_managers()
        self.tm = self.create_topic_map()
        self.authority = self.create_authority('Test')


class ModelTransactionTestCase (TransactionTestCase, BaseTestCase):

    def setUp (self):
        super(ModelTransactionTestCase, self).setUp()
        self.reset_managers()
        self.tm = self.create_topic_map()
        self.authority = self.create_authority('Test')
