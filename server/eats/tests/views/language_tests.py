from django.core.urlresolvers import reverse

from eats.models import Language
from eats.tests.views.view_test_case import ViewTestCase


class LanguageViewsTestCase (ViewTestCase):

    def test_language_list (self):
        url = reverse('language-list')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], Language._meta)
        self.assertEqual(len(response.context['topics']), 0)
        language = self.create_language('English', 'en')
        response = self.client.get(url)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(language in response.context['topics'])

    def test_language_add_get (self):
        url = reverse('language-add')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], Language._meta)
        
    def test_language_add_post_redirects (self):
        self.assertEqual(Language.objects.count(), 0)
        url = reverse('language-add')
        post_data = {'name': 'English', 'code': 'en', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('language-list'))
        self.assertEqual(Language.objects.count(), 1)
        post_data = {'name': 'French', 'code': 'fr',
                     '_addanother': 'Save and add another'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, url)
        self.assertEqual(Language.objects.count(), 2)
        post_data = {'name': 'German', 'code': 'de',
                     '_continue': 'Save and continue editing'}
        response = self.client.post(url, post_data, follow=True)
        language = Language.objects.get_by_admin_name('German')
        redirect_url = reverse('language-change',
                               kwargs={'topic_id': language.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(Language.objects.count(), 3)

    def test_language_add_post_content (self):
        url = reverse('language-add')
        post_data = {'name': 'English', 'code': 'en', '_save': 'Save'}
        self.client.post(url, post_data, follow=True)
        language = Language.objects.get_by_admin_name('English')
        self.assertEqual(language.get_code(), 'en')

    def test_language_add_illegal_post (self):
        self.assertEqual(Language.objects.count(), 0)
        url = reverse('language-add')
        # Missing language code.
        post_data = {'name': 'English', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Language.objects.count(), 0)
        # Duplicate language name.
        language = self.create_language('English', 'en')
        self.assertEqual(Language.objects.count(), 1)
        post_data = {'name': 'English', 'code': 'fr', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Language.objects.count(), 1)
        self.assertTrue(language in Language.objects.all())
        self.assertEqual(language.get_code(), 'en')
        # Duplicate language code.
        post_data = {'name': 'French', 'code': 'en', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Language.objects.count(), 1)
        self.assertTrue(language in Language.objects.all())
        self.assertEqual(language.get_admin_name(), 'English')
        
    def test_language_change_illegal_get (self):
        url = reverse('language-change', kwargs={'topic_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_language_change_get (self):
        language = self.create_language('English', 'en')
        url = reverse('language-change', kwargs={
                'topic_id': language.get_id()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, language)

    def test_language_change_post (self):
        self.assertEqual(Language.objects.count(), 0)
        language = self.create_language('English', 'en')
        url = reverse('language-change', kwargs={
                'topic_id': language.get_id()})
        self.assertEqual(language.get_admin_name(), 'English')
        self.assertEqual(language.get_code(), 'en')
        post_data = {'name': 'French', 'code': 'fr', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('language-list'))
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(language.get_admin_name(), 'French')
        self.assertEqual(language.get_code(), 'fr')
