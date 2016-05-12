from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import NamePartType
from .admin_view_test_case import AdminViewTestCase


class NamePartTypeViewsTestCase (AdminViewTestCase):

    def test_authentication (self):
        nameparttype = self.create_name_part_type('given')
        url_data = [
            ('eats-nameparttype-list', {}),
            ('eats-nameparttype-add', {}),
            ('eats-nameparttype-change', {'topic_id': nameparttype.get_id()})]
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

    def test_name_part_type_list (self):
        url = reverse('eats-nameparttype-list')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], NamePartType._meta)
        self.assertEqual(len(response.context['topics']), 0)
        name_part_type = self.create_name_part_type('given')
        response = self.app.get(url, user='staff')
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(name_part_type in response.context['topics'])

    def test_name_part_type_add_get (self):
        url = reverse('eats-nameparttype-add')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], NamePartType._meta)

    def test_name_part_type_add_post_redirects (self):
        self.assertEqual(NamePartType.objects.count(), 0)
        url = reverse('eats-nameparttype-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'given'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-nameparttype-list'))
        self.assertEqual(NamePartType.objects.count(), 1)
        form['name'] = 'family'
        response = form.submit('_addanother')
        self.assertRedirects(response, url)
        self.assertEqual(NamePartType.objects.count(), 2)
        form['name'] = 'patronymic'
        response = form.submit('_continue')
        name_part_type = NamePartType.objects.get_by_admin_name('patronymic')
        redirect_url = reverse('eats-nameparttype-change',
                               kwargs={'topic_id': name_part_type.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(NamePartType.objects.count(), 3)

    def test_name_part_type_add_illegal_post (self):
        self.assertEqual(NamePartType.objects.count(), 0)
        url = reverse('eats-nameparttype-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        # Missing name_part_type name.
        form['name'] = ''
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NamePartType.objects.count(), 0)
        # Duplicate name_part_type name.
        name_part_type = self.create_name_part_type('given')
        self.assertEqual(NamePartType.objects.count(), 1)
        form['name'] = 'given'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(NamePartType.objects.count(), 1)
        self.assertTrue(name_part_type in NamePartType.objects.all())

    def test_name_part_type_change_illegal_get (self):
        url = reverse('eats-nameparttype-change', kwargs={'topic_id': 0})
        self.app.get(url, status=404, user='staff')

    def test_name_part_type_change_get (self):
        name_part_type = self.create_name_part_type('exact')
        url = reverse('eats-nameparttype-change', kwargs={
                'topic_id': name_part_type.get_id()})
        response = self.app.get(url, user='staff')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, name_part_type)

    def test_name_part_type_change_post (self):
        self.assertEqual(NamePartType.objects.count(), 0)
        name_part_type = self.create_name_part_type('given')
        self.assertEqual(name_part_type.get_admin_name(), 'given')
        url = reverse('eats-nameparttype-change', kwargs={
                'topic_id': name_part_type.get_id()})
        form = self.app.get(url, user='staff').forms[
            'infrastructure-change-form']
        form['name'] = 'family'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-nameparttype-list'))
        self.assertEqual(NamePartType.objects.count(), 1)
        self.assertEqual(name_part_type.get_admin_name(), 'family')
