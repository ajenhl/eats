from .view_test_case import ViewTestCase


class AdminViewTestCase (ViewTestCase):

    def setUp (self):
        super().setUp()
        self.authority_id = self.authority.get_id()
        # Create staff member.
        user = self.create_django_user('staff', 'staff@example.org', 'password')
        user.is_staff = True
        user.is_active = True
        user.save()
        # Create normal user.
        user = self.create_django_user('user', 'user@example.org', 'password')
        # Create normal EATS user.
        eats_user = self.create_django_user('eats_user', 'eats@example.org',
                                            'password')
        self.create_user(eats_user)
