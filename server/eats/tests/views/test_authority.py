from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import Authority
from .admin_view_test_case import AdminViewTestCase


class AuthorityViewsTestCase (AdminViewTestCase):

    def test_authentication (self):
        url_data = [
            ('eats-authority-list', {}),
            ('eats-authority-add', {}),
            ('eats-authority-change', {'topic_id': self.authority.get_id()})]
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

    def test_authority_list (self):
        url = reverse('eats-authority-list')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], Authority._meta)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(self.authority in response.context['topics'])
        authority2 = self.create_authority('Test2')
        response = self.app.get(url, user='staff')
        self.assertEqual(len(response.context['topics']), 2)
        self.assertTrue(self.authority in response.context['topics'])
        self.assertTrue(authority2 in response.context['topics'])

    def test_authority_add_get (self):
        url = reverse('eats-authority-add')
        response = self.app.get(url, user='staff')
        self.assertEqual(response.context['opts'], Authority._meta)

    def test_authority_add_post_redirects (self):
        url = reverse('eats-authority-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'Test2'
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-authority-list'))
        self.assertEqual(Authority.objects.count(), 2)
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'Test3'
        response = form.submit('_addanother')
        self.assertRedirects(response, url)
        self.assertEqual(Authority.objects.count(), 3)
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'Test4'
        response = form.submit('_continue')
        authority = Authority.objects.get_by_admin_name('Test4')
        redirect_url = reverse('eats-authority-change',
                               kwargs={'topic_id': authority.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(Authority.objects.count(), 4)

    def test_authority_add_post_content (self):
        url = reverse('eats-authority-add')
        calendar1 = self.create_calendar('Test1')
        calendar2 = self.create_calendar('Test2')
        date_period = self.create_date_period('Test')
        date_type = self.create_date_type('Test')
        entity_relationship_type = self.create_entity_relationship_type(
            'Test', 'Reverse')
        entity_type = self.create_entity_type('Test')
        language = self.create_language('English', 'en')
        name_type = self.create_name_type('Test')
        script = self.create_script('Latin', 'Latn', ' ')
        user = self.create_django_user('user1', 'user1@example.org', 'password')
        editor = self.create_user(user)
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'Test1'
        form['calendars'] = [calendar1.get_id(), calendar2.get_id()]
        form['date_periods'] = [date_period.get_id()]
        form['date_types'] = [date_type.get_id()]
        form['entity_relationship_types'] = [entity_relationship_type.get_id()]
        form['entity_types'] = [entity_type.get_id()]
        form['languages'] = [language.get_id()]
        form['name_types'] = [name_type.get_id()]
        form['scripts'] = [script.get_id()]
        form['editors'] = [editor.pk]
        form.submit('_save')
        authority = Authority.objects.get_by_admin_name('Test1')
        self.assertEqual(len(authority.get_calendars()), 2)
        self.assertTrue(calendar1 in authority.get_calendars())
        self.assertTrue(calendar2 in authority.get_calendars())
        self.assertEqual(len(authority.get_date_periods()), 1)
        self.assertTrue(date_period in authority.get_date_periods())
        self.assertEqual(len(authority.get_date_types()), 1)
        self.assertTrue(date_type in authority.get_date_types())
        self.assertEqual(len(authority.get_entity_relationship_types()), 1)
        self.assertTrue(entity_relationship_type in
                        authority.get_entity_relationship_types())
        self.assertEqual(len(authority.get_entity_types()), 1)
        self.assertTrue(entity_type in authority.get_entity_types())
        self.assertEqual(len(authority.get_languages()), 1)
        self.assertTrue(language in authority.get_languages())
        self.assertEqual(len(authority.get_name_types()), 1)
        self.assertTrue(name_type in authority.get_name_types())
        self.assertEqual(len(authority.get_scripts()), 1)
        self.assertTrue(script in authority.get_scripts())
        self.assertEqual(len(authority.get_editors()), 1)
        self.assertTrue(editor in authority.get_editors())

    def test_authority_add_illegal_post (self):
        self.assertEqual(Authority.objects.count(), 1)
        url = reverse('eats-authority-add')
        form = self.app.get(url, user='staff').forms['infrastructure-add-form']
        form['name'] = 'Test'
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Authority.objects.count(), 1)

    def test_authority_change_illegal_get (self):
        url = reverse('eats-authority-change', kwargs={'topic_id': 0})
        self.app.get(url, status=404, user='staff')

    def test_authority_change_get (self):
        url = reverse('eats-authority-change', kwargs={
                'topic_id': self.authority.get_id()})
        response = self.app.get(url, user='staff')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, self.authority)

    def test_authority_change_post (self):
        self.assertEqual(Authority.objects.count(), 1)
        url = reverse('eats-authority-change', kwargs={
                'topic_id': self.authority.get_id()})
        self.assertEqual(self.authority.get_admin_name(), 'Test')
        self.assertEqual(len(self.authority.get_calendars()), 0)
        self.assertEqual(len(self.authority.get_date_periods()), 0)
        self.assertEqual(len(self.authority.get_date_types()), 0)
        self.assertEqual(len(self.authority.get_entity_relationship_types()), 0)
        self.assertEqual(len(self.authority.get_entity_types()), 0)
        self.assertEqual(len(self.authority.get_languages()), 0)
        self.assertEqual(len(self.authority.get_name_types()), 0)
        self.assertEqual(len(self.authority.get_scripts()), 0)
        self.assertEqual(len(self.authority.get_editors()), 0)
        calendar1 = self.create_calendar('Test1')
        calendar2 = self.create_calendar('Test2')
        date_period = self.create_date_period('Test')
        date_type = self.create_date_type('Test')
        entity_relationship_type = self.create_entity_relationship_type(
            'Test', 'Reverse')
        entity_type = self.create_entity_type('Test')
        language = self.create_language('English', 'en')
        name_type = self.create_name_type('Test')
        script = self.create_script('Latin', 'Latn', ' ')
        user1 = self.create_django_user('user1', 'user1@example.org',
                                        'password')
        editor1 = self.create_user(user1)
        user2 = self.create_django_user('user2', 'user2@example.org',
                                        'password')
        editor2 = self.create_user(user2)
        form = self.app.get(url, user='staff').forms[
            'infrastructure-change-form']
        form['name'] = 'Test1'
        form['calendars'] = [calendar1.get_id(), calendar2.get_id()]
        form['date_periods'] = [date_period.get_id()]
        form['date_types'] = [date_type.get_id()]
        form['entity_relationship_types'] = [entity_relationship_type.get_id()]
        form['entity_types'] = [entity_type.get_id()]
        form['languages'] = [language.get_id()]
        form['name_types'] = [name_type.get_id()]
        form['scripts'] = [script.get_id()]
        form['editors'] = [editor1.pk, editor2.pk]
        response = form.submit('_save')
        self.assertRedirects(response, reverse('eats-authority-list'))
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(self.authority.get_admin_name(), 'Test1')
        self.assertEqual(len(self.authority.get_calendars()), 2)
        self.assertTrue(calendar1 in self.authority.get_calendars())
        self.assertTrue(calendar2 in self.authority.get_calendars())
        self.assertEqual(len(self.authority.get_date_periods()), 1)
        self.assertTrue(date_period in self.authority.get_date_periods())
        self.assertEqual(len(self.authority.get_date_types()), 1)
        self.assertTrue(date_type in self.authority.get_date_types())
        self.assertEqual(len(self.authority.get_entity_relationship_types()), 1)
        self.assertTrue(entity_relationship_type in
                        self.authority.get_entity_relationship_types())
        self.assertEqual(len(self.authority.get_entity_types()), 1)
        self.assertTrue(entity_type in self.authority.get_entity_types())
        self.assertEqual(len(self.authority.get_languages()), 1)
        self.assertTrue(language in self.authority.get_languages())
        self.assertEqual(len(self.authority.get_name_types()), 1)
        self.assertTrue(name_type in self.authority.get_name_types())
        self.assertEqual(len(self.authority.get_scripts()), 1)
        self.assertTrue(script in self.authority.get_scripts())
        self.assertEqual(len(self.authority.get_editors()), 2)
        self.assertTrue(editor1 in self.authority.get_editors())
        self.assertTrue(editor2 in self.authority.get_editors())
        self.assertTrue(self.authority in editor1.editable_authorities.all())
        self.assertTrue(self.authority in editor2.editable_authorities.all())

    def test_authority_illegal_remove (self):
        """Tests that an infrastructure element in use cannot be removed."""
        calendar = self.create_calendar('Julian')
        entity_type1 = self.create_entity_type('Test1')
        entity_type2 = self.create_entity_type('Test2')
        self.authority.set_entity_types([entity_type1, entity_type2])
        self.assertEqual(len(self.authority.get_calendars()), 0)
        entity = self.tm.create_entity(self.authority)
        entity.create_entity_type_property_assertion(self.authority,
                                                     entity_type1)
        url = reverse('eats-authority-change', kwargs={
                'topic_id': self.authority.get_id()})
        form = self.app.get(url, user='staff').forms[
            'infrastructure-change-form']
        form['calendars'] = [calendar.get_id()]
        form['entity_types'] = [entity_type2.get_id()]
        response = form.submit('_save')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(self.authority.get_entity_types()),
                         set([entity_type1, entity_type2]))
        self.assertEqual(len(self.authority.get_calendars()), 0)
