from django.core.urlresolvers import reverse

from eats.models import Authority
from eats.tests.views.view_test_case import ViewTestCase


class AuthorityViewsTestCase (ViewTestCase):

    def test_authority_list (self):
        url = reverse('authority-list')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], Authority._meta)
        self.assertEqual(len(response.context['topics']), 1)
        self.assertTrue(self.authority in response.context['topics'])
        authority2 = self.create_authority('Test2')
        response = self.client.get(url)
        self.assertEqual(len(response.context['topics']), 2)
        self.assertTrue(self.authority in response.context['topics'])
        self.assertTrue(authority2 in response.context['topics'])

    def test_authority_add_get (self):
        url = reverse('authority-add')
        response = self.client.get(url)
        self.assertEqual(response.context['opts'], Authority._meta)
        
    def test_authority_add_post_redirects (self):
        url = reverse('authority-add')
        post_data = {'name': 'Test2', '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('authority-list'))
        self.assertEqual(Authority.objects.count(), 2)
        post_data = {'name': 'Test3', '_addanother': 'Save and add another'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, url)
        self.assertEqual(Authority.objects.count(), 3)
        post_data = {'name': 'Test4', '_continue': 'Save and continue editing'}
        response = self.client.post(url, post_data, follow=True)
        authority = Authority.objects.get_by_admin_name('Test4')
        redirect_url = reverse('authority-change',
                               kwargs={'topic_id': authority.get_id()})
        self.assertRedirects(response, redirect_url)
        self.assertEqual(Authority.objects.count(), 4)

    def test_authority_add_post_content (self):
        url = reverse('authority-add')
        calendar1 = self.create_calendar('Test1')
        calendar2 = self.create_calendar('Test2')
        date_period = self.create_date_period('Test')
        date_type = self.create_date_type('Test')
        entity_relationship_type = self.create_entity_relationship_type(
            'Test', 'Reverse')
        entity_type = self.create_entity_type('Test')
        language = self.create_language('English', 'en')
        name_type = self.create_name_type('Test')
        script = self.create_script('Latin', 'Latn')
        user = self.create_django_user('user1', 'user1@example.org', 'password')
        editor = self.create_user(user)
        post_data = {
            'name': 'Test1',
            'calendars': [calendar1.get_id(), calendar2.get_id()],
            'date_periods': [date_period.get_id()],
            'date_types': [date_type.get_id()],
            'entity_relationship_types': [entity_relationship_type.get_id()],
            'entity_types': [entity_type.get_id()],
            'languages': [language.get_id()],
            'name_types': [name_type.get_id()], 'scripts': [script.get_id()],
            'editors': [editor.pk], '_save': 'Save'}
        self.client.post(url, post_data, follow=True)
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
        url = reverse('authority-add')
        post_data = {'name': 'Test'}
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Authority.objects.count(), 1)
        
    def test_authority_change_illegal_get (self):
        url = reverse('authority-change', kwargs={'topic_id': 0})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_authority_change_get (self):
        url = reverse('authority-change', kwargs={
                'topic_id': self.authority.get_id()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, self.authority)

    def test_authority_change_post (self):
        self.assertEqual(Authority.objects.count(), 1)
        url = reverse('authority-change', kwargs={
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
        script = self.create_script('Latin', 'Latn')
        user1 = self.create_django_user('user1', 'user1@example.org',
                                        'password')
        editor1 = self.create_user(user1)
        user2 = self.create_django_user('user2', 'user2@example.org',
                                        'password')
        editor2 = self.create_user(user2)
        post_data = {
            'name': 'Test1',
            'calendars': [calendar1.get_id(), calendar2.get_id()],
            'date_periods': [date_period.get_id()],
            'date_types': [date_type.get_id()],
            'entity_relationship_types': [entity_relationship_type.get_id()],
            'entity_types': [entity_type.get_id()],
            'languages': [language.get_id()],
            'name_types': [name_type.get_id()], 'scripts': [script.get_id()],
            'editors': [editor1.pk, editor2.pk], '_save': 'Save'}
        response = self.client.post(url, post_data, follow=True)
        self.assertRedirects(response, reverse('authority-list'))
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
