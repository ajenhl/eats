from django.conf import settings
from django.core.urlresolvers import reverse

from eats.models import EATSMLImport
from eats.tests.views.view_test_case import ViewTestCase


class EATSMLImportViewTestCase (ViewTestCase):

    def setUp (self):
        super(EATSMLImportViewTestCase, self).setUp()
        user = self.create_django_user('user', 'user@example.org', 'password')
        self.editor = self.create_user(user)
        self.editor.editable_authorities = [self.authority]
        self.url = reverse('import-eatsml')

    def test_authentication (self):
        """Tests that only an editor can see the import page."""
        login_url = settings.LOGIN_URL + '?next=' + self.url
        # Anonymous request.
        response = self.app.get(self.url)
        self.assertRedirects(response, login_url)
        non_editor = self.create_django_user('user2', 'user2@example.org',
                                             'password')
        # Non-EATS user request.
        response = self.app.get(self.url, user='user2')
        self.assertRedirects(response, login_url)
        # EATS non-editor request.
        self.create_user(non_editor)
        response = self.app.get(self.url, user='user2')
        self.assertRedirects(response, login_url)
        # EATS editor request.
        response = self.app.get(self.url, user='user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'eats/edit/eatsml_import.html')

    def test_post_valid (self):
        self.assertEqual(EATSMLImport.objects.count(), 0)
        description = 'New import'
        import_xml = b'''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1">
      <name>New authority</name>
    </authority>
  </authorities>
</collection>'''
        form = self.app.get(self.url, user='user').forms['eatsml-import-form']
        upload_file = ('import_file', 'eatsml.xml', import_xml)
        csrf_token = form['csrfmiddlewaretoken'].value
        data = {'csrfmiddlewaretoken': csrf_token, 'description': description}
        response = self.app.post(self.url, data, upload_files=[upload_file],
                                 user='user').follow()
        self.assertEqual(EATSMLImport.objects.count(), 1)
        eatsml_import = EATSMLImport.objects.all()[0]
        self.assertEqual(eatsml_import.description, description)
        view_url = reverse('display-eatsml-import',
                           kwargs={'import_id': eatsml_import.id})
        self.assertEqual(response.request.url[len(response.request.host_url):],
                         view_url)

    def test_post_invalid (self):
        self.assertEqual(EATSMLImport.objects.count(), 0)
        description = 'New import'
        import_xml = b'''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <!-- Missing @xml:id -->
    <authority>
      <name>Test</name>
    </authority>
  </authorities>
</collection>'''
        form = self.app.get(self.url, user='user').forms['eatsml-import-form']
        upload_file = ('import_file', 'eatsml.xml', import_xml)
        csrf_token = form['csrfmiddlewaretoken'].value
        data = {'csrfmiddlewaretoken': csrf_token, 'description': description}
        self.app.post(self.url, data, status=500,
                      upload_files=[upload_file], user='user')
        self.assertEqual(EATSMLImport.objects.count(), 0)
