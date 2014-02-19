from django.conf import settings
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from eats.models import EATSTopicMap


class AdministrationPanelTestCase (WebTest):

    def test_create_topic_map (self):
        url = reverse('create-topic-map')
        # A GET request ought to redirect to the administration panel
        # without consequence.
        response = self.app.get(url)
        redirect_url = reverse('administration-panel')
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
