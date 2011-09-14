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
        authority = self.create_authority('Test')
        entity = self.tm.create_entity(authority)
        entity.get_existences()[0].remove()
        relationship_type = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        authority.set_entity_relationship_types([relationship_type])
        other = self.tm.create_entity(authority)
        other.get_existences()[0].remove()
        relationship = entity.create_entity_relationship_property_assertion(
            authority, relationship_type, entity, other)
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d">
      <name>Test</name>
      <entity_relationship_types>
        <entity_relationship_type ref="entity_relationship_type-%(relationship_type)d"/>
      </entity_relationship_types>
    </authority>
  </authorities>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-%(relationship_type)d">
      <name>is child of</name>
      <reverse_name>is parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
  <entities>
    <entity xml:id="entity-%(entity)d">
      <entity_relationships>
        <entity_relationship authority="authority-%(authority)d" entity_relationship_type="entity_relationship_type-%(relationship_type)d" domain_entity="entity-%(entity)d" range_entity="entity-%(other)d"/>
      </entity_relationships>
    </entity>
    <entity xml:id="entity-%(other)d" related_entity="true"></entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'other': other.get_id(), 'relationship_type': relationship_type.get_id()}
        self._compare_XML(export, expected_xml)

    def test_export_entity_note (self):
        authority = self.create_authority('Test')
        entity = self.tm.create_entity(authority)
        entity.get_existences()[0].remove()
        entity.create_note_property_assertion(authority, 'A note.')
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-%(entity)d">
      <notes>
        <note authority="authority-%(authority)d">A note.</note>
      </notes>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id()}
        self._compare_XML(export, expected_xml)

    def test_export_entity_subject_identifier (self):
        authority = self.create_authority('Test')
        entity = self.tm.create_entity(authority)
        entity.get_existences()[0].remove()
        entity.create_subject_identifier_property_assertion(
            authority, 'http://www.example.org/test/')
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-%(entity)d">
      <subject_identifiers>
        <subject_identifier authority="authority-%(authority)d">http://www.example.org/test/</subject_identifier>
      </subject_identifiers>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id()}
        self._compare_XML(export, expected_xml)

    def test_export_infrastructure_full (self):
        authority1 = self.create_authority('Test1')
        authority2 = self.create_authority('Test2')
        person = self.create_entity_type('person')
        place = self.create_entity_type('place')
        authority1.set_entity_types([person, place])
        authority2.set_entity_types([place])
        regular = self.create_name_type('regular')
        authority1.set_name_types([regular])
        title = self.create_name_part_type('title')
        given = self.create_name_part_type('given')
        family = self.create_name_part_type('family')
        authority1.set_name_part_types([given, family])
        authority2.set_name_part_types([family])
        english = self.create_language('English', 'en')
        english.name_part_types = [title, given, family]
        french = self.create_language('French', 'fr')
        authority1.set_languages([english])
        authority2.set_languages([french])
        child = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        latin = self.create_script('Latin', 'Latn', ' ')
        arabic = self.create_script('Arabic', 'Arab', '')
        authority1.set_scripts([latin])
        authority2.set_scripts([arabic])
        export = self.exporter.export_infrastructure()
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority1)d">
      <name>Test1</name>
      <entity_types>
        <entity_type ref="entity_type-%(person)d"/>
        <entity_type ref="entity_type-%(place)d"/>
      </entity_types>
      <languages>
        <language ref="language-%(english)d"/>
      </languages>
      <name_types>
        <name_type ref="name_type-%(regular)d"/>
      </name_types>
      <name_part_types>
        <name_part_type ref="name_part_type-%(given)d"/>
        <name_part_type ref="name_part_type-%(family)d"/>
      </name_part_types>
      <scripts>
        <script ref="script-%(latin)d"/>
      </scripts>
    </authority>
    <authority xml:id="authority-%(authority2)d">
      <name>Test2</name>
      <entity_types>
        <entity_type ref="entity_type-%(place)d"/>
      </entity_types>
      <languages>
        <language ref="language-%(french)d"/>
      </languages>
      <name_part_types>
        <name_part_type ref="name_part_type-%(family)d"/>
      </name_part_types>
      <scripts>
        <script ref="script-%(arabic)d"/>
      </scripts>
    </authority>
  </authorities>
  <entity_types>
    <entity_type xml:id="entity_type-%(person)d">
      <name>person</name>
    </entity_type>
    <entity_type xml:id="entity_type-%(place)d">
      <name>place</name>
    </entity_type>
  </entity_types>
  <languages>
    <language xml:id="language-%(english)d">
      <name>English</name>
      <code>en</code>
      <name_part_types>
        <name_part_type ref="name_part_type-%(title)d"/>
        <name_part_type ref="name_part_type-%(given)d"/>
        <name_part_type ref="name_part_type-%(family)d"/>
      </name_part_types>
    </language>
    <language xml:id="language-%(french)d">
      <name>French</name>
      <code>fr</code>
    </language>
  </languages>
  <scripts>
    <script xml:id="script-%(arabic)d">
      <name>Arabic</name>
      <code>Arab</code>
      <separator></separator>
    </script>
    <script xml:id="script-%(latin)d">
      <name>Latin</name>
      <code>Latn</code>
      <separator> </separator>
    </script>
  </scripts>
  <name_types>
    <name_type xml:id="name_type-%(regular)d">
      <name>regular</name>
    </name_type>
  </name_types>
  <name_part_types>
    <name_part_type xml:id="name_part_type-%(given)d">
      <name>given</name>
    </name_part_type>
    <name_part_type xml:id="name_part_type-%(family)d">
      <name>family</name>
    </name_part_type>
    <name_part_type xml:id="name_part_type-%(title)d">
      <name>title</name>
    </name_part_type>
  </name_part_types>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-%(child)d">
      <name>is child of</name>
      <reverse_name>is parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
</collection>
''' % {'authority1': authority1.get_id(), 'authority2': authority2.get_id(),
       'english': english.get_id(), 'french': french.get_id(),
       'latin': latin.get_id(), 'arabic': arabic.get_id(),
       'given': given.get_id(), 'family': family.get_id(),
       'person': person.get_id(), 'place': place.get_id(),
       'regular': regular.get_id(), 'title': title.get_id(),
       'child': child.get_id()}
        self._compare_XML(export, expected_xml)
