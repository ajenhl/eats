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

    def _compare_XML (self, export, expected_xml):
        parser = etree.XMLParser(remove_blank_text=True)
        actual = StringIO()
        export.write_c14n(actual)
        expected = StringIO()
        root = etree.XML(expected_xml, parser)
        root.getroottree().write_c14n(expected)
        self.assertEqual(actual.getvalue(), expected.getvalue())
    
    def test_export_entity_existence (self):
        authority = self.create_authority('Test')
        entity = self.tm.create_entity(authority)
        export = self.exporter.export_entities([entity])
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
        self._compare_XML(export, expected_xml)

    def test_export_entity_entity_type (self):
        authority = self.create_authority('Test')
        entity_type = self.create_entity_type('person')
        authority.set_entity_types([entity_type])
        entity = self.tm.create_entity(authority)
        entity.get_existences()[0].remove()
        entity.create_entity_type_property_assertion(authority, entity_type)
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d">
      <name>Test</name>
      <entity_types>
        <entity_type ref="entity_type-%(entity_type)d"/>
      </entity_types>
    </authority>
  </authorities>
  <entity_types>
    <entity_type xml:id="entity_type-%(entity_type)d">
      <name>person</name>
    </entity_type>
  </entity_types>
  <entities>
    <entity xml:id="entity-%(entity)d">
      <entity_types>
        <entity_type authority="authority-%(authority)d" entity_type="entity_type-%(entity_type)d"/>
      </entity_types>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'entity_type': entity_type.get_id()}
        self._compare_XML(export, expected_xml)

    def test_export_entity_name (self):
        authority = self.create_authority('Test')
        name_type = self.create_name_type('regular')
        given_name_part_type = self.create_name_part_type('given')
        family_name_part_type = self.create_name_part_type('family')
        language = self.create_language('English', 'en')
        language.name_part_types = [given_name_part_type,
                                    family_name_part_type]
        script = self.create_script('Latin', 'Latn', ' ')
        authority.set_name_types([name_type])
        authority.set_languages([language])
        authority.set_scripts([script])
        authority.set_name_part_types([given_name_part_type,
                                       family_name_part_type])
        entity = self.tm.create_entity(authority)
        entity.get_existences()[0].remove()
        assertion = entity.create_name_property_assertion(
            authority, name_type, language, script, '')
        name = assertion.name
        name.create_name_part(given_name_part_type, language, script,
                              'Miriam', 1)
        name.create_name_part(given_name_part_type, language, script,
                              'Clare', 2)
        name.create_name_part(family_name_part_type, language, script,
                              'Frost', 1)
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d">
      <name>Test</name>
      <languages>
        <language ref="language-%(language)d"/>
      </languages>
      <name_types>
        <name_type ref="name_type-%(name_type)d"/>
      </name_types>
      <name_part_types>
        <name_part_type ref="name_part_type-%(family_name_part_type)d"/>
        <name_part_type ref="name_part_type-%(given_name_part_type)d"/>
      </name_part_types>
      <scripts>
        <script ref="script-%(script)d"/>
      </scripts>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-%(language)d">
      <name>English</name>
      <code>en</code>
      <name_part_types>
        <name_part_type ref="name_part_type-%(given_name_part_type)d"/>
        <name_part_type ref="name_part_type-%(family_name_part_type)d"/>
      </name_part_types>
    </language>
  </languages>
  <scripts>
    <script xml:id="script-%(script)d">
      <name>Latin</name>
      <code>Latn</code>
      <separator> </separator>
    </script>
  </scripts>
  <name_types>
    <name_type xml:id="name_type-%(name_type)d">
      <name>regular</name>
    </name_type>
  </name_types>
  <name_part_types>
    <name_part_type xml:id="name_part_type-%(family_name_part_type)d">
      <name>family</name>
    </name_part_type>
    <name_part_type xml:id="name_part_type-%(given_name_part_type)d">
      <name>given</name>
    </name_part_type>
  </name_part_types>
  <entities>
    <entity xml:id="entity-%(entity)d">
      <names>
        <name authority="authority-%(authority)d" language="language-%(language)d" name_type="name_type-%(name_type)d" script="script-%(script)d">
          <display_form></display_form>
          <name_parts>
            <name_part name_part_type="name_part_type-%(family_name_part_type)d" language="language-%(language)d" script="script-%(script)d">Frost</name_part>
            <name_part name_part_type="name_part_type-%(given_name_part_type)d" language="language-%(language)d" script="script-%(script)d">Miriam</name_part>
            <name_part name_part_type="name_part_type-%(given_name_part_type)d" language="language-%(language)d" script="script-%(script)d">Clare</name_part>
          </name_parts>
          <assembled_form>Miriam Clare Frost</assembled_form>
        </name>
      </names>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'language': language.get_id(), 'script': script.get_id(),
       'given_name_part_type': given_name_part_type.get_id(),
       'family_name_part_type': family_name_part_type.get_id(),
       'name_type': name_type.get_id()}
        self._compare_XML(export, expected_xml)
        
    def test_export_entity_entity_relationship (self):
        pass

    def test_export_infrastructure (self):
        pass
