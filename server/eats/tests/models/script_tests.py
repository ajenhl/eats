from eats.tests.base_test_case import BaseTestCase


class ScriptTestCase (BaseTestCase):

    def test_script_admin_name (self):
        script = self.create_script('Latin', 'Latn')
        self.assertEqual(script.get_admin_name(), 'Latin')
        script.set_admin_name('Arabic')
        self.assertEqual(script.get_admin_name(), 'Arabic')
        script2 = self.create_script('Gujarati', 'Gujr')
        self.assertRaises(Exception, script2.set_admin_name, 'Arabic')
    
    def test_script_code (self):
        script = self.create_script('Latin', 'Latn')
        self.assertEqual(script.get_code(), 'Latn')
        script.set_code('Arab')
        self.assertEqual(script.get_code(), 'Arab')
        script2 = self.create_script('Gujarati', 'Gujr')
        self.assertRaises(Exception, script2.set_code, 'Arab')
