from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import DateType
from .admin_view_test_case import AdminViewTestCase


class DateTypeViewsTestCase (AdminViewTestCase):

    def test_authentication (self):
        date_type = self.create_date_type('exact')
        url_data = [
            ('eats-datetype-list', {}),
            ('eats-datetype-add', {}),
            ('eats-datetype-change', {'topic_id': date_type.get_id()})]
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

    def test_date_type_list (self):
        url = reverse('eats-datetype-list')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], DateType._meta)
        self.assertEqual(len(response.context['topics']), 0)
        date_type = self.create_date_type('exact')
        response = self.app.get(url, user='staff')
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(date_type in response.context['topics'])

    def test_date_type_add_get (self):
        url = reverse('eats-datetype-add')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], DateType._meta)

    def test_date_type_add_post_redirects (self):
        self.assertEqual(DateType.objects.count(), 0)
        url = reverse('eats-datetype-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'exact'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-datetype-list'))
        self.assertEqual(DateType.objects.count(), 1)
        form['name'] = 'circa'
        response = form.submit('_addanother')
        self.assertRedirects(response, url)
        self.assertEqual(DateType.objects.count(), 2)
        form['name'] = 'roughly'
        response = form.submit('_continue')
        date_type = DateType.objects.get_by_admin_name('roughly')
        redirect_url = reverse('eats-datetype-change',
                               kwargs={'topic_id': date_type.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(DateType.objects.count(), 3)

    def test_date_type_add_illegal_post (self):
        self.assertEqual(DateType.objects.count(), 0)
        url = reverse('eats-datetype-add')
        # Missing date_type name.
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = ''
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DateType.objects.count(), 0)
        # Duplicate date_type name.
        date_type = self.create_date_type('exact')
        self.assertEqual(DateType.objects.count(), 1)
        form['name'] = 'exact'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DateType.objects.count(), 1)
        self.assertTrue(date_type in DateType.objects.all())

    def test_date_type_change_illegal_get (self):
        url = reverse('eats-datetype-change', kwargs={'topic_id': 0})
        self.app.get(url, status=404, user='staff')

    def test_date_type_change_get (self):
        date_type = self.create_date_type('exact')
        url = reverse('eats-datetype-change', kwargs={
                'topic_id': date_type.get_id()})
        response = self.app.get(url, user='staff')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, date_type)

    def test_date_type_change_post (self):
        self.assertEqual(DateType.objects.count(), 0)
        date_type = self.create_date_type('exact')
        url = reverse('eats-datetype-change', kwargs={
                'topic_id': date_type.get_id()})
        self.assertEqual(date_type.get_admin_name(), 'exact')
        form = self.app.get(url, user='staff').forms[
            'infrastructure-change-form']
        form['name'] = 'circa'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-datetype-list'))
        self.assertEqual(DateType.objects.count(), 1)
        self.assertEqual(date_type.get_admin_name(), 'circa')
