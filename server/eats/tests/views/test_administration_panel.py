from django.conf import settings
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from eats.models import EATSTopicMap
from eats.tests.base_test_case import BaseTestCase


class AdministrationPanelTestCase (WebTest, BaseTestCase):

    def setUp (self):
        super().setUp()
        # Create staff member.
        user = self.create_django_user('staff', 'staff@example.org', 'password')
        user.is_staff = True
        user.is_active = True
        user.save()
        # Create normal user.
        user = self.create_django_user('user', 'user@example.org', 'password')
        # Create normal EATS user.
        eats_user = self.create_django_user('eats_user', 'eats@example.org',
                                            'password')
        self.create_user(eats_user)

    def test_authentication (self):
        url = reverse('eats-create-topic-map')
        login_url = settings.LOGIN_URL + '?next=' + url
        response = self.app.get(url)
        self.assertRedirects(response, login_url)
        response = self.app.get(url, user='user')
        self.assertRedirects(response, login_url)
        response = self.app.get(url, user='eats_user')
        self.assertRedirects(response, login_url)

    def test_create_topic_map (self):
        url = reverse('eats-create-topic-map')
        # A GET request ought to redirect to the administration panel
        # without consequence.
        response = self.app.get(url, user='staff')
        redirect_url = reverse('eats-administration-panel')
        self.assertRedirects(response, redirect_url)
        self.assertRaises(EATSTopicMap.DoesNotExist, EATSTopicMap.objects.get,
                          iri=settings.EATS_TOPIC_MAP)
        form = self.app.get(redirect_url).forms['create-topic-map-form']
        response = form.submit()
        self.assertRedirects(response, redirect_url + '?tm_create=created')
        self.assertTrue(EATSTopicMap.objects.get(iri=settings.EATS_TOPIC_MAP))
        response = form.submit()
        self.assertRedirects(response, redirect_url + '?tm_create=exists')
        self.assertTrue(EATSTopicMap.objects.get(iri=settings.EATS_TOPIC_MAP))
