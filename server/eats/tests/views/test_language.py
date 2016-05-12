from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import Language
from .admin_view_test_case import AdminViewTestCase


class LanguageViewsTestCase (AdminViewTestCase):

    def test_authentication (self):
        language = self.create_language('English', 'en')
        url_data = [
            ('eats-language-list', {}),
            ('eats-language-add', {}),
            ('eats-language-change', {'topic_id': language.get_id()})]
        for url_name, kwargs in url_data:
            url = reverse(url_name, kwargs=kwargs)
            login_url = settings.LOGIN_URL + '?next=' + url
            response = self.app.get(url)
            self.assertRedirects(response, login_url,
                                 msg_prefix='Anonymous user to {}'.format(
                                     url_name))
        for url_name, kwargs in url_data:
            response = self.app.get(url, user='user')
            self.assertRedirects(response, login_url,
                                 msg_prefix='User to {}'.format(url_name))
        for url_name, kwargs in url_data:
            response = self.app.get(url, user='eats_user')
            self.assertRedirects(response, login_url,
                                 msg_prefix='EATS user to {}'.format(url_name))
            response = self.app.get(url, user='staff')
            self.assertEqual(response.status_code, 200)

    def test_language_list (self):
        url = reverse('eats-language-list')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], Language._meta)
        self.assertEqual(len(response.context['topics']), 0)
        language = self.create_language('English', 'en')
        response = self.app.get(url, user='staff')
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(language in response.context['topics'])

    def test_language_add_get (self):
        url = reverse('eats-language-add')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], Language._meta)

    def test_language_add_post_redirects (self):
        self.assertEqual(Language.objects.count(), 0)
        url = reverse('eats-language-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'English'
        form['code'] = 'en'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-language-list'))
        self.assertEqual(Language.objects.count(), 1)
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'French'
        form['code'] = 'fr'
        response = form.submit('_addanother')
        self.assertRedirects(response, url)
        self.assertEqual(Language.objects.count(), 2)
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'German'
        form['code'] = 'de'
        response = form.submit('_continue')
        language = Language.objects.get_by_admin_name('German')
        redirect_url = reverse('eats-language-change',
                               kwargs={'topic_id': language.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(Language.objects.count(), 3)

    def test_language_add_post_content (self):
        self.assertEqual(Language.objects.count(), 0)
        url = reverse('eats-language-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'English'
        form['code'] = 'en'
        form.submit('_save')
        language = Language.objects.all()[0]
        self.assertEqual(language.get_admin_name(), 'English')
        self.assertEqual(language.get_code(), 'en')

    def test_language_add_illegal_post (self):
        self.assertEqual(Language.objects.count(), 0)
        url = reverse('eats-language-add')
        # Missing language code.
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'English'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Language.objects.count(), 0)
        # Duplicate language name.
        language = self.create_language('English', 'en')
        self.assertEqual(Language.objects.count(), 1)
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'English'
        form['code'] = 'fr'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Language.objects.count(), 1)
        self.assertTrue(language in Language.objects.all())
        self.assertEqual(language.get_code(), 'en')
        # Duplicate language code.
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'French'
        form['code'] = 'en'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Language.objects.count(), 1)
        self.assertTrue(language in Language.objects.all())
        self.assertEqual(language.get_admin_name(), 'English')
        # Duplicate name part types.
        name_part_type = self.create_name_part_type('given')
        form = self.app.get(url).forms['infrastructure-add-form']
        form['name'] = 'Hindi'
        form['code'] = 'hi'
        form['name_part_type-0'] = name_part_type.get_id()
        form['name_part_type-1'] = name_part_type.get_id()
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Language.objects.count(), 1)
        self.assertTrue(language in Language.objects.all())

    def test_language_change_illegal_get (self):
        url = reverse('eats-language-change', kwargs={'topic_id': 0})
        self.app.get(url, status=404, user='staff')

    def test_language_change_get (self):
        language = self.create_language('English', 'en')
        url = reverse('eats-language-change', kwargs={'topic_id':
                                                      language.get_id()})
        response = self.app.get(url, user='staff')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, language)

    def test_language_change_post (self):
        self.assertEqual(Language.objects.count(), 0)
        language = self.create_language('English', 'en')
        url = reverse('eats-language-change', kwargs={'topic_id':
                                                      language.get_id()})
        self.assertEqual(language.get_admin_name(), 'English')
        self.assertEqual(language.get_code(), 'en')
        form = self.app.get(url, user='staff').forms[
            'infrastructure-change-form']
        form['name'] = 'French'
        form['code'] = 'fr'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-language-list'))
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(language.get_admin_name(), 'French')
        self.assertEqual(language.get_code(), 'fr')
