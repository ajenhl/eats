from tmapi.exceptions import TopicInUseException
from eats.models import Script
from eats.tests.models.model_test_case import ModelTestCase


class ScriptTestCase (ModelTestCase):

    def test_script_admin_name (self):
        script = self.create_script('Latin', 'Latn', ' ')
        self.assertEqual(script.get_admin_name(), 'Latin')
        script.set_admin_name('Arabic')
        self.assertEqual(script.get_admin_name(), 'Arabic')
        script2 = self.create_script('Gujarati', 'Gujr', ' ')
        self.assertRaises(Exception, script2.set_admin_name, 'Arabic')
    
    def test_script_code (self):
        script = self.create_script('Latin', 'Latn', ' ')
        self.assertEqual(script.get_code(), 'Latn')
        script.set_code('Arab')
        self.assertEqual(script.get_code(), 'Arab')
        script2 = self.create_script('Gujarati', 'Gujr', ' ')
        self.assertRaises(Exception, script2.set_code, 'Arab')

    def test_script_delete (self):
        self.assertEqual(Script.objects.count(), 0)
        authority = self.create_authority('test')
        script = self.create_script('Latin', 'Latn', ' ')
        self.assertEqual(Script.objects.count(), 1)
        authority.set_scripts([script])
        self.assertRaises(TopicInUseException, script.remove)
        self.assertEqual(Script.objects.count(), 1)
        authority.set_scripts([])
        script.remove()
        self.assertEqual(Script.objects.count(), 0)

    def test_script_separator (self):
        script = self.create_script('Latin', 'Latn', '')
        self.assertEqual(script.separator, '')
        script.separator = ' '
        self.assertEqual(script.separator, ' ')
