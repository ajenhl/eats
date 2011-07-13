from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from eats.models import EATSTopicMap


class AdministrationPanelTestCase (TestCase):

    def test_create_topic_map (self):
        url = reverse('create-topic-map')
        # A GET request ought to redirect to the administration panel
        # without consequence.
        response = self.client.get(url, follow=True)
        redirect_url = reverse('administration-panel')
        self.assertRedirects(response, redirect_url)
        self.assertRaises(EATSTopicMap.DoesNotExist, EATSTopicMap.objects.get,
                          iri=settings.EATS_TOPIC_MAP)
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, redirect_url + '?tm_create=created')
        self.assertTrue(EATSTopicMap.objects.get(iri=settings.EATS_TOPIC_MAP))
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, redirect_url + '?tm_create=exists')
        self.assertTrue(EATSTopicMap.objects.get(iri=settings.EATS_TOPIC_MAP))
