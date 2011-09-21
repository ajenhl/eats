from StringIO import StringIO

from lxml import etree

from django.test import TestCase

from eats.lib.eatsml_importer import EATSMLImporter
from eats.models import Authority
from eats.tests.base_test_case import BaseTestCase


class EATSMLImportTestCase (TestCase, BaseTestCase):

    def setUp (self):
        super(EATSMLImportTestCase, self).setUp()
        self.tm = self.create_topic_map()
        self.importer = EATSMLImporter(self.tm)
        admin_user = self.create_django_user('admin', 'admin@example.org',
                                             'password')
        self.admin = self.create_user(admin_user)

    def _compare_XML (self, export, expected_xml):
        parser = etree.XMLParser(remove_blank_text=True)
        actual = StringIO()
        export.write_c14n(actual)
        expected = StringIO()
        root = etree.XML(expected_xml, parser)
        root.getroottree().write_c14n(expected)
        self.assertEqual(actual.getvalue(), expected.getvalue())

    def test_import_authority (self):
        self.assertEqual(Authority.objects.all().count(), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1">
      <name>Test</name>
    </authority>
  </authorities>
</collection>
'''
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(Authority.objects.all().count(), 1)
        authority = Authority.objects.all()[0]
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%s">
      <name>Test</name>
    </authority>
  </authorities>
</collection>
''' % authority.get_id()
        self._compare_XML(annotated_import, expected_xml)
        
    def test_import_entity (self):
        pass
