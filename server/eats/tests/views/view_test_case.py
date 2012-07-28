from django_webtest import WebTest

from eats.tests.base_test_case import BaseTestCase


class ViewTestCase (WebTest, BaseTestCase):

    def setUp (self):
        super(ViewTestCase, self).setUp()
        self.reset_managers()
        self.tm = self.create_topic_map()
        self.authority = self.create_authority('Test')
