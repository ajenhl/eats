from StringIO import StringIO

from lxml import etree

from django.test import TestCase

from eats.lib.eatsml_exporter import EATSMLExporter
from eats.tests.base_test_case import BaseTestCase


class EATSMLExportTestCase (TestCase, BaseTestCase):

    def setUp (self):
        super(EATSMLExportTestCase, self).setUp()
        self.tm = self.create_topic_map()
        self.exporter = EATSMLExporter()
        self.parser = etree.XMLParser(remove_blank_text=True)
    
    def test_export_entity_existence (self):
        authority = self.create_authority('Test')
        entity = self.tm.create_entity(authority)
        export = self.exporter.export_entities([entity])
        actual = StringIO()
        export.write_c14n(actual)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d"><name>Test</name></authority>
  </authorities>
  <entities>
    <entity xml:id="entity-%(entity)d">
      <existences>
        <existence authority="authority-%(authority)d"/>
      </existences>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id()}
        root = etree.XML(expected_xml, self.parser)
        expected = StringIO()
        root.getroottree().write_c14n(expected)
        self.assertEqual(actual.getvalue(), expected.getvalue())
