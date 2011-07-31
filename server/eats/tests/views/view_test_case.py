from django_webtest import WebTest

from eats.tests.base_test_case import BaseTestCase


class ViewTestCase (WebTest, BaseTestCase):

    def setUp (self):
        # Create a topic map.
        self.tm = self.create_topic_map()
        # Create an authority.
        self.authority = self.create_authority('Test')
