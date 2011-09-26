from StringIO import StringIO

from lxml import etree

from django.test import TestCase

from eats.exceptions import EATSMLException
from eats.lib.eatsml_importer import EATSMLImporter
from eats.models import Authority, Calendar, DatePeriod, DateType, Entity, EntityRelationshipType, EntityType, Language, NamePartType, NameType, Script
from eats.tests.base_test_case import BaseTestCase


class EATSMLImportTestCase (TestCase, BaseTestCase):

    def setUp (self):
        super(EATSMLImportTestCase, self).setUp()
        self.tm = self.create_topic_map()
        self.importer = EATSMLImporter(self.tm)
        admin_user = self.create_django_user('admin', 'admin@example.org',
                                             'password')
        self.admin = self.create_user(admin_user)

    def _compare_XML (self, import_tree, expected_xml):
        parser = etree.XMLParser(remove_blank_text=True)
        actual = StringIO()
        import_tree.write_c14n(actual)
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
        authority_name = authority.get_admin_name()
        self.assertEqual(authority_name, 'Test')
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

    def test_import_calendar (self):
        authority = self.create_authority('Test')
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(Calendar.objects.all()), 0)
        self.assertEqual(len(authority.get_calendars()), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <calendars>
        <calendar ref="calendar-1"/>
      </calendars>
    </authority>
  </authorities>
  <calendars>
    <calendar xml:id="calendar-1">
      <name>lifespan</name>
    </calendar>
  </calendars>
</collection>
''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(Calendar.objects.all()), 1)
        self.assertEqual(len(authority.get_calendars()), 1)
        calendar = Calendar.objects.all()[0]
        self.assertTrue(calendar in authority.get_calendars())
        self.assertEqual(calendar.get_admin_name(), 'lifespan')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <calendars>
        <calendar ref="calendar-1"/>
      </calendars>
    </authority>
  </authorities>
  <calendars>
    <calendar xml:id="calendar-1" eats_id="%(calendar)d">
      <name>lifespan</name>
    </calendar>
  </calendars>
</collection>
''' % {'authority': authority.get_id(), 'calendar': calendar.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_date_period (self):
        authority = self.create_authority('Test')
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(DatePeriod.objects.all()), 0)
        self.assertEqual(len(authority.get_date_periods()), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <date_periods>
        <date_period ref="date_period-1"/>
      </date_periods>
    </authority>
  </authorities>
  <date_periods>
    <date_period xml:id="date_period-1">
      <name>lifespan</name>
    </date_period>
  </date_periods>
</collection>
''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(DatePeriod.objects.all()), 1)
        self.assertEqual(len(authority.get_date_periods()), 1)
        date_period = DatePeriod.objects.all()[0]
        self.assertTrue(date_period in authority.get_date_periods())
        self.assertEqual(date_period.get_admin_name(), 'lifespan')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <date_periods>
        <date_period ref="date_period-1"/>
      </date_periods>
    </authority>
  </authorities>
  <date_periods>
    <date_period xml:id="date_period-1" eats_id="%(date_period)d">
      <name>lifespan</name>
    </date_period>
  </date_periods>
</collection>
''' % {'authority': authority.get_id(), 'date_period': date_period.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_date_type (self):
        authority = self.create_authority('Test')
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(DateType.objects.all()), 0)
        self.assertEqual(len(authority.get_date_types()), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <date_types>
        <date_type ref="date_type-1"/>
      </date_types>
    </authority>
  </authorities>
  <date_types>
    <date_type xml:id="date_type-1">
      <name>exact</name>
    </date_type>
  </date_types>
</collection>
''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(DateType.objects.all()), 1)
        self.assertEqual(len(authority.get_date_types()), 1)
        date_type = DateType.objects.all()[0]
        self.assertTrue(date_type in authority.get_date_types())
        self.assertEqual(date_type.get_admin_name(), 'exact')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <date_types>
        <date_type ref="date_type-1"/>
      </date_types>
    </authority>
  </authorities>
  <date_types>
    <date_type xml:id="date_type-1" eats_id="%(date_type)d">
      <name>exact</name>
    </date_type>
  </date_types>
</collection>
''' % {'authority': authority.get_id(), 'date_type': date_type.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_entity_relationship_type (self):
        authority = self.create_authority('Test')
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(EntityRelationshipType.objects.all()), 0)
        self.assertEqual(len(authority.get_entity_relationship_types()), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <entity_relationship_types>
        <entity_relationship_type ref="entity_relationship_type-1"/>
      </entity_relationship_types>
    </authority>
  </authorities>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-1">
      <name>is child of</name>
      <reverse_name>is parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
</collection>
''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(EntityRelationshipType.objects.all()), 1)
        self.assertEqual(len(authority.get_entity_relationship_types()), 1)
        entity_relationship_type = EntityRelationshipType.objects.all()[0]
        self.assertTrue(entity_relationship_type in
                        authority.get_entity_relationship_types())
        self.assertEqual(entity_relationship_type.get_admin_forward_name(),
                         'is child of')
        self.assertEqual(entity_relationship_type.get_admin_reverse_name(),
                         'is parent of')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <entity_relationship_types>
        <entity_relationship_type ref="entity_relationship_type-1"/>
      </entity_relationship_types>
    </authority>
  </authorities>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-1" eats_id="%(entity_relationship_type)d">
      <name>is child of</name>
      <reverse_name>is parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
</collection>
''' % {'authority': authority.get_id(), 'entity_relationship_type': entity_relationship_type.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_entity_type (self):
        authority = self.create_authority('Test')
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(EntityType.objects.all()), 0)
        self.assertEqual(len(authority.get_entity_types()), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <entity_types>
        <entity_type ref="entity_type-1"/>
      </entity_types>
    </authority>
  </authorities>
  <entity_types>
    <entity_type xml:id="entity_type-1">
      <name>exact</name>
    </entity_type>
  </entity_types>
</collection>
''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(EntityType.objects.all()), 1)
        self.assertEqual(len(authority.get_entity_types()), 1)
        entity_type = EntityType.objects.all()[0]
        self.assertTrue(entity_type in authority.get_entity_types())
        self.assertEqual(entity_type.get_admin_name(), 'exact')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <entity_types>
        <entity_type ref="entity_type-1"/>
      </entity_types>
    </authority>
  </authorities>
  <entity_types>
    <entity_type xml:id="entity_type-1" eats_id="%(entity_type)d">
      <name>exact</name>
    </entity_type>
  </entity_types>
</collection>
''' % {'authority': authority.get_id(), 'entity_type': entity_type.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_language (self):
        authority = self.create_authority('Test')
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(Language.objects.all()), 0)
        self.assertEqual(len(authority.get_languages()), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <languages>
        <language ref="language-1"/>
      </languages>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-1">
      <name>English</name>
      <code>en</code>
    </language>
  </languages>
</collection>
''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(Language.objects.all()), 1)
        self.assertEqual(len(authority.get_languages()), 1)
        language = Language.objects.all()[0]
        self.assertTrue(language in authority.get_languages())
        self.assertEqual(language.get_admin_name(), 'English')
        self.assertEqual(language.get_code(), 'en')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <languages>
        <language ref="language-1"/>
      </languages>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-1" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
    </language>
  </languages>
</collection>
''' % {'authority': authority.get_id(), 'language': language.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_name_part_type (self):
        authority = self.create_authority('Test')
        language = self.create_language('English', 'en')
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(Language.objects.all()), 1)
        self.assertEqual(len(NamePartType.objects.all()), 0)
        self.assertEqual(len(authority.get_name_part_types()), 0)
        self.assertEqual(len(language.name_part_types), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
      </name_part_types>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-1" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
      </name_part_types>
    </language>
  </languages>
  <name_part_types>
    <name_part_type xml:id="name_part_type-1">
      <name>given</name>
    </name_part_type>
  </name_part_types>
</collection>
''' % {'authority': authority.get_id(), 'language': language.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(Language.objects.all()), 1)
        self.assertEqual(len(NamePartType.objects.all()), 1)
        self.assertEqual(len(authority.get_name_part_types()), 1)
        name_part_type = NamePartType.objects.all()[0]
        self.assertEqual(language.name_part_types, [name_part_type])
        self.assertTrue(name_part_type in authority.get_name_part_types())
        self.assertEqual(name_part_type.get_admin_name(), 'given')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
      </name_part_types>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-1" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
      </name_part_types>
    </language>
  </languages>
  <name_part_types>
    <name_part_type xml:id="name_part_type-1" eats_id="%(name_part_type)d">
      <name>given</name>
    </name_part_type>
  </name_part_types>
</collection>
''' % {'authority': authority.get_id(), 'language': language.get_id(),
       'name_part_type': name_part_type.get_id()}
        self._compare_XML(annotated_import, expected_xml)
        
    def test_import_name_type (self):
        authority = self.create_authority('Test')
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(NameType.objects.all()), 0)
        self.assertEqual(len(authority.get_name_types()), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <name_types>
        <name_type ref="name_type-1"/>
      </name_types>
    </authority>
  </authorities>
  <name_types>
    <name_type xml:id="name_type-1">
      <name>regular</name>
    </name_type>
  </name_types>
</collection>
''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(NameType.objects.all()), 1)
        self.assertEqual(len(authority.get_name_types()), 1)
        name_type = NameType.objects.all()[0]
        self.assertTrue(name_type in authority.get_name_types())
        self.assertEqual(name_type.get_admin_name(), 'regular')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <name_types>
        <name_type ref="name_type-1"/>
      </name_types>
    </authority>
  </authorities>
  <name_types>
    <name_type xml:id="name_type-1" eats_id="%(name_type)d">
      <name>regular</name>
    </name_type>
  </name_types>
</collection>
''' % {'authority': authority.get_id(), 'name_type': name_type.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_script (self):
        authority = self.create_authority('Test')
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(Script.objects.all()), 0)
        self.assertEqual(len(authority.get_scripts()), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <scripts>
        <script ref="script-1"/>
      </scripts>
    </authority>
  </authorities>
  <scripts>
    <script xml:id="script-1">
      <name>Latin</name>
      <code>Latn</code>
      <separator> </separator>
    </script>
  </scripts>
</collection>
''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        self.assertEqual(len(Authority.objects.all()), 1)
        self.assertEqual(len(Script.objects.all()), 1)
        self.assertEqual(len(authority.get_scripts()), 1)
        script = Script.objects.all()[0]
        self.assertTrue(script in authority.get_scripts())
        self.assertEqual(script.get_admin_name(), 'Latin')
        self.assertEqual(script.get_code(), 'Latn')
        self.assertEqual(script.separator, ' ')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <scripts>
        <script ref="script-1"/>
      </scripts>
    </authority>
  </authorities>
  <scripts>
    <script xml:id="script-1" eats_id="%(script)d">
      <name>Latin</name>
      <code>Latn</code>
      <separator> </separator>
    </script>
  </scripts>
</collection>
''' % {'authority': authority.get_id(), 'script': script.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_illformed_xml (self):
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority>
      <name>Test</name>
    </authority>
  </authorities>
<!-- Missing closing tag. -->'''
        self.assertRaises(EATSMLException, self.importer.import_xml, import_xml,
                          self.admin)

    def test_import_invalid_xml (self):
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <!-- Missing @xml:id -->
    <authority>
      <name>Test</name>
    </authority>
  </authorities>
</collection>'''
        self.assertRaises(EATSMLException, self.importer.import_xml, import_xml,
                          self.admin)

    def test_import_new_entity_entity_relationship (self):
        authority = self.create_authority('Test')
        entity_relationship_type = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        authority.set_entity_relationship_types([entity_relationship_type])
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <entity_relationship_types>
        <entity_relationship_type ref="entity_relationship_type-1"/>
      </entity_relationship_types>
    </authority>
  </authorities>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-1" eats_id="%(entity_relationship_type)d">
      <name>is child of</name>
      <reverse_name>is parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
  <entities>
    <entity xml:id="entity-1">
      <entity_relationships>
        <entity_relationship authority="authority-1" domain_entity="entity-1" entity_relationship_type="entity_relationship_type-1" range_entity="entity-2"/>
      </entity_relationships>
    </entity>
    <entity xml:id="entity-2">
      <entity_relationships>
        <entity_relationship authority="authority-1" domain_entity="entity-1" entity_relationship_type="entity_relationship_type-1" range_entity="entity-2"/>
      </entity_relationships>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(),
                    'entity_relationship_type': entity_relationship_type.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        entity1 = Entity.objects.all()[0]
        entity2 = Entity.objects.all()[1]
        assertion = entity1.get_entity_relationships()[0]
        self.assertEqual(assertion.authority, authority)
        self.assertEqual(assertion.entity_relationship_type,
                         entity_relationship_type)
        self.assertEqual(assertion.domain_entity, entity1)
        self.assertEqual(assertion.range_entity, entity2)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <entity_relationship_types>
        <entity_relationship_type ref="entity_relationship_type-1"/>
      </entity_relationship_types>
    </authority>
  </authorities>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-1" eats_id="%(entity_relationship_type)d">
      <name>is child of</name>
      <reverse_name>is parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity1)d">
      <entity_relationships>
        <entity_relationship authority="authority-1" domain_entity="entity-1" eats_id="%(assertion)d" entity_relationship_type="entity_relationship_type-1" range_entity="entity-2"/>
      </entity_relationships>
    </entity>
    <entity xml:id="entity-2" eats_id="%(entity2)d">
      <entity_relationships>
        <entity_relationship authority="authority-1" domain_entity="entity-1" entity_relationship_type="entity_relationship_type-1" range_entity="entity-2"/>
      </entity_relationships>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(),
                    'entity_relationship_type': entity_relationship_type.get_id(),
                    'entity1': entity1.get_id(), 'entity2': entity2.get_id(),
                    'assertion': assertion.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_new_entity_entity_type (self):
        authority = self.create_authority('Test')
        entity_type = self.create_entity_type('person')
        authority.set_entity_types([entity_type])
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <entity_types>
        <entity_type ref="entity_type-1"/>
      </entity_types>
    </authority>
  </authorities>
  <entity_types>
    <entity_type xml:id="entity_type-1" eats_id="%(entity_type)d">
      <name>person</name>
    </entity_type>
  </entity_types>
  <entities>
    <entity xml:id="entity-1">
      <entity_types>
        <entity_type authority="authority-1" entity_type="entity_type-1"/>
      </entity_types>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(),
                    'entity_type': entity_type.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        entity = Entity.objects.all()[0]
        entity_type_assertion = entity.get_entity_types()[0]
        self.assertEqual(entity_type_assertion.authority, authority)
        self.assertEqual(entity_type_assertion.entity_type, entity_type)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <entity_types>
        <entity_type ref="entity_type-1"/>
      </entity_types>
    </authority>
  </authorities>
  <entity_types>
    <entity_type xml:id="entity_type-1" eats_id="%(entity_type)d">
      <name>person</name>
    </entity_type>
  </entity_types>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity)d">
      <entity_types>
        <entity_type authority="authority-1" eats_id="%(entity_type_assertion)d" entity_type="entity_type-1"/>
      </entity_types>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'entity_type': entity_type.get_id(),
                    'entity_type_assertion': entity_type_assertion.get_id()}
        self._compare_XML(annotated_import, expected_xml)
        
    def test_import_new_entity_existence (self):
        authority = self.create_authority('Test')
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-1">
      <existences>
        <existence authority="authority-1"/>
      </existences>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        entity = Entity.objects.all()[0]
        existence = entity.get_existences()[0]
        self.assertEqual(existence.authority, authority)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity)d">
      <existences>
        <existence authority="authority-1" eats_id="%(existence)d"/>
      </existences>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'existence': existence.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_new_entity_name (self):
        authority = self.create_authority('Test')
        language = self.create_language('English', 'en')
        name_type = self.create_name_type('regular')
        given_name_part_type = self.create_name_part_type('given')
        family_name_part_type = self.create_name_part_type('family')
        script = self.create_script('Latin', 'Latn', ' ')
        language.name_part_types = [given_name_part_type, family_name_part_type]
        authority.set_languages([language])
        authority.set_name_part_types([given_name_part_type,
                                       family_name_part_type])
        authority.set_name_types([name_type])
        authority.set_scripts([script])
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test1</name>
      <languages>
        <language ref="language-1"/>
      </languages>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
        <name_part_type ref="name_part_type-2"/>
      </name_part_types>
      <name_types>
        <name_type ref="name_type-1"/>
      </name_types>
      <scripts>
        <script ref="script-1"/>
      </scripts>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-1" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
        <name_part_type ref="name_part_type-2"/>
      </name_part_types>
    </language>
  </languages>
  <name_part_types>
    <name_part_type xml:id="name_part_type-1" eats_id="%(given_name_part_type)d">
      <name>given</name>
    </name_part_type>
    <name_part_type xml:id="name_part_type-2" eats_id="%(family_name_part_type)d">
      <name>family</name>
    </name_part_type>
  </name_part_types>
  <name_types>
    <name_type xml:id="name_type-1" eats_id="%(name_type)d">
      <name>regular</name>
    </name_type>
  </name_types>
  <scripts>
    <script xml:id="script-1" eats_id="%(script)d">
      <name>Latin</name>
      <code>Latn</code>
      <separator> </separator>
    </script>
  </scripts>
  <entities>
    <entity xml:id="entity-1">
      <names>
        <name authority="authority-1" language="language-1" name_type="name_type-1" script="script-1">
          <display_form>Miri Frost</display_form>
          <name_parts>
            <name_part name_part_type="name_part_type-2" language="language-1" script="script-1">Frost</name_part>
            <name_part name_part_type="name_part_type-1" language="language-1" script="script-1">Miriam</name_part>
            <name_part name_part_type="name_part_type-1" language="language-1" script="script-1">Clare</name_part>
          </name_parts>
          <assembled_form></assembled_form>
        </name>
      </names>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(),
                    'language': language.get_id(), 'script': script.get_id(),
                    'name_type': name_type.get_id(),
                    'given_name_part_type': given_name_part_type.get_id(),
                    'family_name_part_type': family_name_part_type.get_id(),
                    }
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        entity = Entity.objects.all()[0]
        assertion = entity.get_eats_names()[0]
        self.assertEqual(assertion.authority, authority)
        name = assertion.name
        self.assertEqual(name.display_form, 'Miri Frost')
        self.assertEqual(name.language, language)
        self.assertEqual(name.script, script)
        name_parts = name.get_name_parts()
        family_name_parts = name_parts[family_name_part_type]
        self.assertEqual(len(family_name_parts), 1)
        family_name_part = family_name_parts[0]
        self.assertEqual(family_name_part.display_form, 'Frost')
        given_name_parts = name_parts[given_name_part_type]
        self.assertEqual(len(given_name_parts), 2)
        self.assertEqual(given_name_parts[0].display_form, 'Miriam')
        self.assertEqual(given_name_parts[1].display_form, 'Clare')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test1</name>
      <languages>
        <language ref="language-1"/>
      </languages>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
        <name_part_type ref="name_part_type-2"/>
      </name_part_types>
      <name_types>
        <name_type ref="name_type-1"/>
      </name_types>
      <scripts>
        <script ref="script-1"/>
      </scripts>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-1" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
        <name_part_type ref="name_part_type-2"/>
      </name_part_types>
    </language>
  </languages>
  <name_part_types>
    <name_part_type xml:id="name_part_type-1" eats_id="%(given_name_part_type)d">
      <name>given</name>
    </name_part_type>
    <name_part_type xml:id="name_part_type-2" eats_id="%(family_name_part_type)d">
      <name>family</name>
    </name_part_type>
  </name_part_types>
  <name_types>
    <name_type xml:id="name_type-1" eats_id="%(name_type)d">
      <name>regular</name>
    </name_type>
  </name_types>
  <scripts>
    <script xml:id="script-1" eats_id="%(script)d">
      <name>Latin</name>
      <code>Latn</code>
      <separator> </separator>
    </script>
  </scripts>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity)d">
      <names>
        <name authority="authority-1" eats_id="%(assertion)d" language="language-1" name_type="name_type-1" script="script-1">
          <display_form>Miri Frost</display_form>
          <name_parts>
            <name_part name_part_type="name_part_type-2" language="language-1" script="script-1">Frost</name_part>
            <name_part name_part_type="name_part_type-1" language="language-1" script="script-1">Miriam</name_part>
            <name_part name_part_type="name_part_type-1" language="language-1" script="script-1">Clare</name_part>
          </name_parts>
          <assembled_form></assembled_form>
        </name>
      </names>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'assertion': assertion.get_id(),
                    'language': language.get_id(), 'script': script.get_id(),
                    'name_type': name_type.get_id(),
                    'given_name_part_type': given_name_part_type.get_id(),
                    'family_name_part_type': family_name_part_type.get_id(),}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_new_entity_note (self):
        authority = self.create_authority('Test')
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-1">
      <notes>
        <note authority="authority-1">This is a note.</note>
      </notes>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        entity = Entity.objects.all()[0]
        assertion = entity.get_notes()[0]
        self.assertEqual(assertion.note, 'This is a note.')
        self.assertEqual(assertion.authority, authority)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity)d">
      <notes>
        <note authority="authority-1" eats_id="%(assertion)d">This is a note.</note>
      </notes>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'assertion': assertion.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_new_entity_subject_identifier (self):
        authority = self.create_authority('Test')
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-1">
      <subject_identifiers>
        <subject_identifier authority="authority-1">http://www.example.org/test/</subject_identifier>
      </subject_identifiers>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)
        entity = Entity.objects.all()[0]
        assertion = entity.get_subject_identifiers()[0]
        self.assertEqual(assertion.subject_identifier,
                         'http://www.example.org/test/')
        self.assertEqual(assertion.authority, authority)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity)d">
      <subject_identifiers>
        <subject_identifier authority="authority-1" eats_id="%(assertion)d">http://www.example.org/test/</subject_identifier>
      </subject_identifiers>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'assertion': assertion.get_id()}
        self._compare_XML(annotated_import, expected_xml)        
