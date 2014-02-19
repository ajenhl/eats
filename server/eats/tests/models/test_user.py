from eats.models import EATSUser
from eats.tests.models.model_test_case import ModelTestCase


class UserTestCase (ModelTestCase):

    def setUp (self):
        super(UserTestCase, self).setUp()
        self.user = self.create_django_user('username', 'user@example.org',
                                            'password')

    def test_create_user (self):
        self.assertEqual(EATSUser.objects.count(), 0)
        self.assertEqual(EATSUser.editors.count(), 0)
        user = EATSUser(user=self.user)
        user.save()
        self.assertEqual(EATSUser.objects.count(), 1)
        self.assertEqual(EATSUser.editors.count(), 0)
        self.assertFalse(user.is_editor())
        self.assertTrue(user in EATSUser.objects.all())
        user.editable_authorities = [self.authority]
        self.assertEqual(EATSUser.objects.count(), 1)
        self.assertEqual(EATSUser.editors.count(), 1)
        self.assertTrue(user.is_editor())
        user.editable_authorities.clear()
        self.assertFalse(user.is_editor())

    def test_authority (self):
        user = self.create_user(self.user)
        self.assertEqual(user.get_authority(), None)
        user.set_authority(self.authority)
        self.assertEqual(user.get_authority(), self.authority)
        authority2 = self.create_authority('Test2')
        user.editable_authorities = [authority2]
        user.set_current_authority(authority2)
        self.assertEqual(user.get_authority(), authority2)

    def test_current_authority (self):
        user = self.create_user(self.user)
        self.assertEqual(user.get_current_authority(), None)
        authority2 = self.create_authority('Test2')
        user.editable_authorities = [self.authority, authority2]
        self.assertEqual(user.get_current_authority(),
                         user.editable_authorities.all()[0])
        user.set_current_authority(self.authority)
        self.assertEqual(user.get_current_authority(), self.authority)
        user.set_current_authority(authority2)
        self.assertEqual(user.get_current_authority(), authority2)
        user.editable_authorities = [self.authority]
        self.assertEqual(user.get_current_authority(), self.authority)
        self.assertRaises(Exception, user.set_current_authority, authority2)
        user.editable_authorities.clear()
        self.assertEqual(user.get_current_authority(), None)

    def test_language_preference (self):
        user = self.create_user(self.user)
        self.assertEqual(user.get_language(), None)
        language = self.create_language('English', 'en')
        user.set_language(language)
        self.assertEqual(user.get_language(), language)

    def test_script_preference (self):
        user = self.create_user(self.user)
        self.assertEqual(user.get_script(), None)
        script = self.create_script('Latin', 'Latn', ' ')
        user.set_script(script)
        self.assertEqual(user.get_script(), script)
