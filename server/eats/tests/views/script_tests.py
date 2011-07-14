from django.core.urlresolvers import reverse

from eats.models import Script
from eats.tests.base_test_case import BaseTestCase


class ScriptViewsTestCase (BaseTestCase):

    def test_script_list (self):
        url = reverse('script-list')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], Script._meta)
        self.assertEqual(len(response.context['topics']), 0)
        script = self.create_script('Latin', 'Latn')
        response = self.client.get(url)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(script in response.context['topics'])

    def test_script_add_get (self):
        url = reverse('script-add')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], Script._meta)
        
    def test_script_add_post_redirects (self):
        self.assertEqual(Script.objects.count(), 0)
        url = reverse('script-add')
        post_data = {'name': 'Latin', 'code': 'Latn', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('script-list'))
        self.assertEqual(Script.objects.count(), 1)
        post_data = {'name': 'Arabic', 'code': 'Arab',
                     '_addanother': 'Save and add another'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, url)
        self.assertEqual(Script.objects.count(), 2)
        post_data = {'name': 'Gujarati', 'code': 'Gujr',
                     '_continue': 'Save and continue editing'}
        response = self.client.post(url, post_data, follow=True)
        script = Script.objects.get_by_admin_name('Gujarati')
        redirect_url = reverse('script-change',
                               kwargs={'topic_id': script.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(Script.objects.count(), 3)

    def test_script_add_post_content (self):
        url = reverse('script-add')
        post_data = {'name': 'Latin', 'code': 'Latn', '_save': 'Save'}
        self.client.post(url, post_data, follow=True)
        script = Script.objects.get_by_admin_name('Latin')
        self.assertEqual(script.get_code(), 'Latn')

    def test_script_add_illegal_post (self):
        self.assertEqual(Script.objects.count(), 0)
        url = reverse('script-add')
        # Missing script code.
        post_data = {'name': 'Latin', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Script.objects.count(), 0)
        # Duplicate script name.
        script = self.create_script('Latin', 'Latn')
        self.assertEqual(Script.objects.count(), 1)
        post_data = {'name': 'Latin', 'code': 'Arab', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Script.objects.count(), 1)
        self.assertTrue(script in Script.objects.all())
        self.assertEqual(script.get_code(), 'Latn')
        # Duplicate script code.
        post_data = {'name': 'Arabic', 'code': 'Latn', '_save': 'Save'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Script.objects.count(), 1)
        self.assertTrue(script in Script.objects.all())
        self.assertEqual(script.get_admin_name(), 'Latin')
        
    def test_script_change_illegal_get (self):
        url = reverse('script-change', kwargs={'topic_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_script_change_get (self):
        script = self.create_script('Latin', 'Latn')
        url = reverse('script-change', kwargs={
                'topic_id': script.get_id()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, script)

    def test_script_change_post (self):
        self.assertEqual(Script.objects.count(), 0)
        script = self.create_script('Latin', 'Latn')
        url = reverse('script-change', kwargs={
                'topic_id': script.get_id()})
        self.assertEqual(script.get_admin_name(), 'Latin')
        self.assertEqual(script.get_code(), 'Latn')
        post_data = {'name': 'Arabic', 'code': 'Arab', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('script-list'))
        self.assertEqual(Script.objects.count(), 1)
        self.assertEqual(script.get_admin_name(), 'Arabic')
        self.assertEqual(script.get_code(), 'Arab')
