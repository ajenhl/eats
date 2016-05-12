from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import NameType
from .admin_view_test_case import AdminViewTestCase


class NameTypeViewsTestCase (AdminViewTestCase):

    def test_authentication (self):
        name_type = self.create_name_type('exact')
        url_data = [
            ('eats-nametype-list', {}),
            ('eats-nametype-add', {}),
            ('eats-nametype-change', {'topic_id': name_type.get_id()})]
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

    def test_name_type_list (self):
        url = reverse('eats-nametype-list')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], NameType._meta)
        self.assertEqual(len(response.context['topics']), 0)
        name_type = self.create_name_type('birth')
        response = self.app.get(url, user='staff')
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(name_type in response.context['topics'])

    def test_name_type_add_get (self):
        url = reverse('eats-nametype-add')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], NameType._meta)

    def test_name_type_add_post_redirects (self):
        self.assertEqual(NameType.objects.count(), 0)
        url = reverse('eats-nametype-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'birth'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-nametype-list'))
        self.assertEqual(NameType.objects.count(), 1)
        form['name'] = 'pseudonym'
        response = form.submit('_addanother')
        self.assertRedirects(response, url)
        self.assertEqual(NameType.objects.count(), 2)
        form['name'] = 'soubriquet'
        response = form.submit('_continue')
        name_type = NameType.objects.get_by_admin_name('soubriquet')
        redirect_url = reverse('eats-nametype-change',
                               kwargs={'topic_id': name_type.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(NameType.objects.count(), 3)

    def test_name_type_add_illegal_post (self):
        self.assertEqual(NameType.objects.count(), 0)
        url = reverse('eats-nametype-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        # Missing name_type name.
        form['name'] = ''
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NameType.objects.count(), 0)
        # Duplicate name_type name.
        name_type = self.create_name_type('birth')
        self.assertEqual(NameType.objects.count(), 1)
        form['name'] = 'birth'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NameType.objects.count(), 1)
        self.assertTrue(name_type in NameType.objects.all())

    def test_name_type_change_illegal_get (self):
        url = reverse('eats-nametype-change', kwargs={'topic_id': 0})
        self.app.get(url, status=404, user='staff')

    def test_name_type_change_get (self):
        name_type = self.create_name_type('exact')
        url = reverse('eats-nametype-change', kwargs={
                'topic_id': name_type.get_id()})
        response = self.app.get(url, user='staff')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, name_type)

    def test_name_type_change_post (self):
        self.assertEqual(NameType.objects.count(), 0)
        name_type = self.create_name_type('birth')
        url = reverse('eats-nametype-change', kwargs={
                'topic_id': name_type.get_id()})
        self.assertEqual(name_type.get_admin_name(), 'birth')
        form = self.app.get(url, user='staff').forms[
            'infrastructure-change-form']
        form['name'] = 'pseudonym'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-nametype-list'))
        self.assertEqual(NameType.objects.count(), 1)
        self.assertEqual(name_type.get_admin_name(), 'pseudonym')
