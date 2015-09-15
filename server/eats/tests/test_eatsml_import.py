from io import BytesIO

from lxml import etree

from django.test import TestCase

from eats.exceptions import EATSMLException
from eats.lib.eatsml_importer import EATSMLImporter
from eats.models import Authority, Calendar, DatePeriod, DateType, Entity, EntityRelationshipType, EntityType, Language, NamePartType, NameType, Script
from eats.tests.base_test_case import BaseTestCase


class EATSMLImportTestCase (TestCase, BaseTestCase):

    def setUp (self):
        super(EATSMLImportTestCase, self).setUp()
        self.reset_managers()
        self.tm = self.create_topic_map()
        self.importer = EATSMLImporter(self.tm)
        admin_user = self.create_django_user('admin', 'admin@example.org',
                                             'password')
        self.admin = self.create_user(admin_user)

    def _compare_XML (self, import_tree, expected_xml):
        parser = etree.XMLParser(remove_blank_text=True)
        actual = BytesIO()
        import_tree.write_c14n(actual)
        expected = BytesIO()
        root = etree.XML(expected_xml, parser)
        root.getroottree().write_c14n(expected)
        self.assertEqual(actual.getvalue(), expected.getvalue())

    def test_prune_1 (self):
        # Elements with an eats_id that are not referenced by a new
        # element are removed.
        entity_type = self.create_entity_type('person')
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <entity_types>
    <entity_type xml:id="entity_type-1" eats_id="%(entity_type)d">
      <name>person</name>
    </entity_type>
  </entity_types>
</collection>
''' % {'entity_type': entity_type.get_id()}
        import_tree = self.importer.import_xml(import_xml, self.admin)[0]
        expected_xml = '<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/"></collection>'
        self._compare_XML(import_tree, expected_xml)

    def test_prune_2 (self):
        # Infrastructure elements without an eats_id are always
        # retained.
        authority = self.create_authority('Test')
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entity_types>
    <entity_type xml:id="entity_type-1">
      <name>person</name>
    </entity_type>
  </entity_types>
  <entities>
    <entity xml:id="entity-1">
      <existences>
        <existence authority="authority-1"/>
      </existences>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id()}
        import_tree = self.importer.import_xml(import_xml, self.admin)[0]
        self._compare_XML(import_tree, import_xml)

    def test_prune_3 (self):
        # An authority's references are only kept if the authority has
        # no eats_id, or if there are no entities. The importer does
        # not modify an existing authority's associated elements.
        authority = self.create_authority('Test1')
        entity_type = self.create_entity_type('person')
        authority.set_entity_types([entity_type])
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test1</name>
      <entity_types>
        <entity_type ref="entity_type-1"/>
      </entity_types>
    </authority>
    <authority xml:id="authority-2">
      <name>Test2</name>
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
</collection>
''' % {'authority': authority.get_id(), 'entity_type': entity_type.get_id()}
        import_tree = self.importer.import_xml(import_xml, self.admin)[0]
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test1</name>
    </authority>
    <authority xml:id="authority-2">
      <name>Test2</name>
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
</collection>
''' % {'authority': authority.get_id(), 'entity_type': entity_type.get_id()}
        self._compare_XML(import_tree, expected_xml)

    def test_prune_4 (self):
        # Pruning must retain referential integrity.
        authority = self.create_authority('Test1')
        calendar = self.create_calendar('Gregorian')
        date_period = self.create_date_period('lifespan')
        date_type = self.create_date_type('exact')
        entity_relationship_type = self.create_entity_relationship_type(
            'is a child of', 'is a parent of')
        entity_type = self.create_entity_type('person')
        language = self.create_language('English', 'en')
        name_part_type = self.create_name_part_type('given')
        name_type = self.create_name_type('regular')
        script = self.create_script('English', 'en', ' ')
        authority.set_entity_types([entity_type])
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1">
      <name>Test</name>
      <calendars>
        <calendar ref="calendar-1"/>
      </calendars>
      <date_periods>
        <date_period ref="date_period-1"/>
      </date_periods>
      <date_types>
        <date_type ref="date_type-1"/>
      </date_types>
      <entity_relationship_types>
        <entity_relationship_type ref="entity_relationship_type-1"/>
      </entity_relationship_types>
      <entity_types>
        <entity_type ref="entity_type-1"/>
        <entity_type ref="entity_type-2"/>
      </entity_types>
      <languages>
        <language ref="language-1"/>
      </languages>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
      </name_part_types>
      <name_types>
        <name_type ref="name_type-1"/>
      </name_types>
      <scripts>
        <script ref="script-1"/>
      </scripts>
    </authority>
  </authorities>
  <calendars>
    <calendar xml:id="calendar-1" eats_id="%(calendar)d">
      <name>Gregorian</name>
    </calendar>
  </calendars>
  <date_periods>
    <date_period xml:id="date_period-1" eats_id="%(date_period)d">
      <name>lifespan</name>
    </date_period>
  </date_periods>
  <date_types>
    <date_type xml:id="date_type-1" eats_id="%(date_type)d">
      <name>exact</name>
    </date_type>
  </date_types>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-1" eats_id="%(entity_relationship_type)d">
      <name>is a child of</name>
      <reverse_name>is a parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
  <entity_types>
    <entity_type xml:id="entity_type-1" eats_id="%(entity_type)d">
      <name>person</name>
    </entity_type>
    <entity_type xml:id="entity_type-2">
      <name>place</name>
    </entity_type>
  </entity_types>
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
      <entity_types>
        <entity_type authority="authority-1" entity_type="entity_type-2"/>
      </entity_types>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'calendar': calendar.get_id(),
       'date_period': date_period.get_id(), 'date_type': date_type.get_id(),
       'entity_relationship_type': entity_relationship_type.get_id(),
       'entity_type': entity_type.get_id(), 'language': language.get_id(),
       'name_part_type': name_part_type.get_id(),
       'name_type': name_type.get_id(), 'script': script.get_id()}
        import_tree = self.importer.import_xml(import_xml, self.admin)[0]
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1">
      <name>Test</name>
      <calendars>
        <calendar ref="calendar-1"/>
      </calendars>
      <date_periods>
        <date_period ref="date_period-1"/>
      </date_periods>
      <date_types>
        <date_type ref="date_type-1"/>
      </date_types>
      <entity_relationship_types>
        <entity_relationship_type ref="entity_relationship_type-1"/>
      </entity_relationship_types>
      <entity_types>
        <entity_type ref="entity_type-1"/>
        <entity_type ref="entity_type-2"/>
      </entity_types>
      <languages>
        <language ref="language-1"/>
      </languages>
      <name_part_types>
        <name_part_type ref="name_part_type-1"/>
      </name_part_types>
      <name_types>
        <name_type ref="name_type-1"/>
      </name_types>
      <scripts>
        <script ref="script-1"/>
      </scripts>
    </authority>
  </authorities>
  <calendars>
    <calendar xml:id="calendar-1" eats_id="%(calendar)d">
      <name>Gregorian</name>
    </calendar>
  </calendars>
  <date_periods>
    <date_period xml:id="date_period-1" eats_id="%(date_period)d">
      <name>lifespan</name>
    </date_period>
  </date_periods>
  <date_types>
    <date_type xml:id="date_type-1" eats_id="%(date_type)d">
      <name>exact</name>
    </date_type>
  </date_types>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-1" eats_id="%(entity_relationship_type)d">
      <name>is a child of</name>
      <reverse_name>is a parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
  <entity_types>
    <entity_type xml:id="entity_type-1" eats_id="%(entity_type)d">
      <name>person</name>
    </entity_type>
    <entity_type xml:id="entity_type-2">
      <name>place</name>
    </entity_type>
  </entity_types>
  <languages>
    <language xml:id="language-1" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
    </language>
  </languages>
  <name_part_types>
    <name_part_type xml:id="name_part_type-1" eats_id="%(name_part_type)d">
      <name>given</name>
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
      <entity_types>
        <entity_type authority="authority-1" entity_type="entity_type-2"/>
      </entity_types>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'calendar': calendar.get_id(),
       'date_period': date_period.get_id(), 'date_type': date_type.get_id(),
       'entity_relationship_type': entity_relationship_type.get_id(),
       'entity_type': entity_type.get_id(), 'language': language.get_id(),
       'name_part_type': name_part_type.get_id(),
       'name_type': name_type.get_id(), 'script': script.get_id()}
        self._compare_XML(import_tree, expected_xml)

    def test_import_authority (self):
        self.assertEqual(Authority.objects.count(), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1">
      <name>Test</name>
    </authority>
  </authorities>
</collection>
'''
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
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
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(Calendar.objects.count(), 0)
        self.assertEqual(authority.get_calendars().count(), 0)
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(Calendar.objects.count(), 1)
        self.assertEqual(authority.get_calendars().count(), 0)
        calendar = Calendar.objects.all()[0]
        # An import will not change an existing authority's references.
        self.assertFalse(calendar in authority.get_calendars())
        self.assertEqual(calendar.get_admin_name(), 'lifespan')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
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
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(DatePeriod.objects.count(), 0)
        self.assertEqual(authority.get_date_periods().count(), 0)
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(DatePeriod.objects.count(), 1)
        self.assertEqual(authority.get_date_periods().count(), 0)
        date_period = DatePeriod.objects.all()[0]
        # An import will not change an existing authority's references.
        self.assertFalse(date_period in authority.get_date_periods())
        self.assertEqual(date_period.get_admin_name(), 'lifespan')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
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
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(DateType.objects.count(), 0)
        self.assertEqual(authority.get_date_types().count(), 0)
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(DateType.objects.count(), 1)
        self.assertEqual(authority.get_date_types().count(), 0)
        date_type = DateType.objects.all()[0]
        # An import will not change an existing authority's references.
        self.assertFalse(date_type in authority.get_date_types())
        self.assertEqual(date_type.get_admin_name(), 'exact')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
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
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(EntityRelationshipType.objects.count(), 0)
        self.assertEqual(authority.get_entity_relationship_types().count(), 0)
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(EntityRelationshipType.objects.count(), 1)
        self.assertEqual(authority.get_entity_relationship_types().count(), 0)
        entity_relationship_type = EntityRelationshipType.objects.all()[0]
        # An import will not change an existing authority's references.
        self.assertFalse(entity_relationship_type in
                        authority.get_entity_relationship_types())
        self.assertEqual(entity_relationship_type.get_admin_forward_name(),
                         'is child of')
        self.assertEqual(entity_relationship_type.get_admin_reverse_name(),
                         'is parent of')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
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
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(EntityType.objects.count(), 0)
        self.assertEqual(authority.get_entity_types().count(), 0)
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(EntityType.objects.count(), 1)
        self.assertEqual(authority.get_entity_types().count(), 0)
        entity_type = EntityType.objects.all()[0]
        # An import will not change an existing authority's references.
        self.assertFalse(entity_type in authority.get_entity_types())
        self.assertEqual(entity_type.get_admin_name(), 'exact')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
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
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(Language.objects.count(), 0)
        self.assertEqual(authority.get_languages().count(), 0)
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(authority.get_languages().count(), 0)
        language = Language.objects.all()[0]
        # An import will not change an existing authority's references.
        self.assertFalse(language in authority.get_languages())
        self.assertEqual(language.get_admin_name(), 'English')
        self.assertEqual(language.get_code(), 'en')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <languages>
    <language xml:id="language-1" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
    </language>
  </languages>
</collection>
''' % {'authority': authority.get_id(), 'language': language.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_language_with_name_part_types (self):
        self.assertEqual(Authority.objects.count(), 0)
        self.assertEqual(Language.objects.count(), 0)
        self.assertEqual(NamePartType.objects.count(), 0)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1">
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
</collection>'''
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(NamePartType.objects.count(), 1)
        authority = Authority.objects.all()[0]
        language = Language.objects.all()[0]
        name_part_type = NamePartType.objects.all()[0]
        self.assertEqual(authority.get_languages().count(), 1)
        self.assertTrue(language in authority.get_languages())
        self.assertEqual(len(language.name_part_types), 1)
        self.assertTrue(name_part_type in language.name_part_types)
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
</collection>''' % {'authority': authority.get_id(),
                    'language': language.get_id(),
                    'name_part_type': name_part_type.get_id()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_name_part_type (self):
        authority = self.create_authority('Test')
        language = self.create_language('English', 'en')
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(NamePartType.objects.count(), 0)
        self.assertEqual(authority.get_name_part_types().count(), 0)
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(NamePartType.objects.count(), 1)
        # An import will not change an existing authority's references.
        self.assertEqual(authority.get_name_part_types().count(), 0)
        name_part_type = NamePartType.objects.all()[0]
        # An existing language can not have its associated name part
        # types changed by an import.
        self.assertEqual(language.name_part_types, [])
        self.assertFalse(name_part_type in authority.get_name_part_types())
        self.assertEqual(name_part_type.get_admin_name(), 'given')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
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
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(NameType.objects.count(), 0)
        self.assertEqual(authority.get_name_types().count(), 0)
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(NameType.objects.count(), 1)
        self.assertEqual(authority.get_name_types().count(), 0)
        name_type = NameType.objects.all()[0]
        # An import will not change an existing authority's references.
        self.assertFalse(name_type in authority.get_name_types())
        self.assertEqual(name_type.get_admin_name(), 'regular')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
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
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(Script.objects.count(), 0)
        self.assertEqual(authority.get_scripts().count(), 0)
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(Authority.objects.count(), 1)
        self.assertEqual(Script.objects.count(), 1)
        self.assertEqual(authority.get_scripts().count(), 0)
        script = Script.objects.all()[0]
        # An import will not change an existing authority's references.
        self.assertFalse(script in authority.get_scripts())
        self.assertEqual(script.get_admin_name(), 'Latin')
        self.assertEqual(script.get_code(), 'Latn')
        self.assertEqual(script.separator, ' ')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
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

    def test_import_xml_bad_eats_id (self):
        self.assertEqual(Authority.objects.count(), 0)
        # Due to pruning, the import XML must include a reference to
        # the authority.
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="1">
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
</collection>'''
        self.assertRaises(EATSMLException, self.importer.import_xml, import_xml,
                          self.admin)

    def test_import_invalid_xml_1 (self):
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

    def test_import_invalid_xml_2 (self):
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

    def test_import_existing_entity (self):
        authority1 = self.create_authority('Test')
        authority2 = self.create_authority('Test 2')
        entity = self.tm.create_entity(authority1)
        self.assertEqual(entity.get_existences().count(), 1)
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority1)d">
      <name>Test</name>
    </authority>
    <authority xml:id="authority-2" eats_id="%(authority2)d">
      <name>Test 2</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity)d">
      <existences>
        <existence authority="authority-2"/>
      </existences>
    </entity>
  </entities>
</collection>
''' % {'authority1': authority1.get_id(), 'authority2': authority2.get_id(),
       'entity': entity.get_id()}
        self.importer.import_xml(import_xml, self.admin)[1]
        self.assertEqual(entity.get_existences().count(), 2)

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
        <entity_relationship authority="authority-1" certainty="full" domain_entity="entity-1" entity_relationship_type="entity_relationship_type-1" range_entity="entity-2"/>
      </entity_relationships>
    </entity>
    <entity xml:id="entity-2">
      <entity_relationships>
        <entity_relationship authority="authority-1" certainty="full" domain_entity="entity-1" entity_relationship_type="entity_relationship_type-1" range_entity="entity-2"/>
      </entity_relationships>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(),
                    'entity_relationship_type': entity_relationship_type.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        entity1, entity2 = Entity.objects.all().order_by('id')
        assertion = entity1.get_entity_relationships()[0]
        self.assertEqual(assertion.authority, authority)
        self.assertEqual(assertion.entity_relationship_type,
                         entity_relationship_type)
        self.assertEqual(assertion.domain_entity, entity1)
        self.assertEqual(assertion.range_entity, entity2)
        self.assertEqual(assertion.certainty,
                         self.tm.property_assertion_full_certainty)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-1" eats_id="%(entity_relationship_type)d">
      <name>is child of</name>
      <reverse_name>is parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity1)d" url="%(entity1_url)s">
      <entity_relationships>
        <entity_relationship authority="authority-1" certainty="full" domain_entity="entity-1" eats_id="%(assertion)d" entity_relationship_type="entity_relationship_type-1" range_entity="entity-2"/>
      </entity_relationships>
    </entity>
    <entity xml:id="entity-2" eats_id="%(entity2)d" url="%(entity2_url)s">
      <entity_relationships>
        <entity_relationship authority="authority-1" certainty="full" domain_entity="entity-1" entity_relationship_type="entity_relationship_type-1" range_entity="entity-2"/>
      </entity_relationships>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(),
                    'entity_relationship_type': entity_relationship_type.get_id(),
                    'entity1': entity1.get_id(), 'entity2': entity2.get_id(),
                    'assertion': assertion.get_id(),
                    'entity1_url': entity1.get_eats_subject_identifier(),
                    'entity2_url': entity2.get_eats_subject_identifier()}
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        entity = Entity.objects.all()[0]
        entity_type_assertion = entity.get_entity_types()[0]
        self.assertEqual(entity_type_assertion.authority, authority)
        self.assertEqual(entity_type_assertion.entity_type, entity_type)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entity_types>
    <entity_type xml:id="entity_type-1" eats_id="%(entity_type)d">
      <name>person</name>
    </entity_type>
  </entity_types>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity)d" url="%(entity_url)s">
      <entity_types>
        <entity_type authority="authority-1" eats_id="%(entity_type_assertion)d" entity_type="entity_type-1"/>
      </entity_types>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'entity_type': entity_type.get_id(),
                    'entity_type_assertion': entity_type_assertion.get_id(),
                    'entity_url': entity.get_eats_subject_identifier()}
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
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
    <entity xml:id="entity-1" eats_id="%(entity)d" url="%(entity_url)s">
      <existences>
        <existence authority="authority-1" eats_id="%(existence)d"/>
      </existences>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'existence': existence.get_id(),
                    'entity_url': entity.get_eats_subject_identifier()}
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
        <name authority="authority-1" is_preferred="true" language="language-1" name_type="name_type-1" script="script-1">
          <display_form>Miri Frost</display_form>
          <name_parts>
            <name_part name_part_type="name_part_type-2" language="language-1" script="script-1">Frost</name_part>
            <name_part name_part_type="name_part_type-1" language="language-1" script="script-1">Miriam</name_part>
            <name_part name_part_type="name_part_type-1" language="language-1" script="script-1">Clare</name_part>
          </name_parts>
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        entity = Entity.objects.all()[0]
        assertion = entity.get_eats_names()[0]
        self.assertEqual(assertion.authority, authority)
        name = assertion.name
        self.assertEqual(name.display_form, 'Miri Frost')
        self.assertEqual(name.language, language)
        self.assertEqual(name.script, script)
        self.assertEqual(assertion.is_preferred, True)
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
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-1" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
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
    <entity xml:id="entity-1" eats_id="%(entity)d" url="%(entity_url)s">
      <names>
        <name authority="authority-1" eats_id="%(assertion)d" is_preferred="true" language="language-1" name_type="name_type-1" script="script-1">
          <display_form>Miri Frost</display_form>
          <name_parts>
            <name_part name_part_type="name_part_type-2" language="language-1" script="script-1">Frost</name_part>
            <name_part name_part_type="name_part_type-1" language="language-1" script="script-1">Miriam</name_part>
            <name_part name_part_type="name_part_type-1" language="language-1" script="script-1">Clare</name_part>
          </name_parts>
        </name>
      </names>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'assertion': assertion.get_id(),
                    'language': language.get_id(), 'script': script.get_id(),
                    'name_type': name_type.get_id(),
                    'given_name_part_type': given_name_part_type.get_id(),
                    'family_name_part_type': family_name_part_type.get_id(),
                    'entity_url': entity.get_eats_subject_identifier()}
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
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
    <entity xml:id="entity-1" eats_id="%(entity)d" url="%(entity_url)s">
      <notes>
        <note authority="authority-1" eats_id="%(assertion)d">This is a note.</note>
      </notes>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'assertion': assertion.get_id(),
                    'entity_url': entity.get_eats_subject_identifier()}
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
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        entity = Entity.objects.all()[0]
        assertion = entity.get_eats_subject_identifiers()[0]
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
    <entity xml:id="entity-1" eats_id="%(entity)d" url="%(entity_url)s">
      <subject_identifiers>
        <subject_identifier authority="authority-1" eats_id="%(assertion)d">http://www.example.org/test/</subject_identifier>
      </subject_identifiers>
    </entity>
  </entities>
</collection>''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
                    'assertion': assertion.get_id(),
                    'entity_url': entity.get_eats_subject_identifier()}
        self._compare_XML(annotated_import, expected_xml)

    def test_import_date (self):
        authority = self.create_authority('Test')
        calendar1 = self.create_calendar('Julian')
        calendar2 = self.create_calendar('Gregorian')
        date_period = self.create_date_period('lifespan')
        date_type1 = self.create_date_type('exact')
        date_type2 = self.create_date_type('circa')
        authority.set_calendars([calendar1, calendar2])
        authority.set_date_periods([date_period])
        authority.set_date_types([date_type1, date_type2])
        import_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
      <calendars>
        <calendar ref="calendar-1"/>
        <calendar ref="calendar-2"/>
      </calendars>
      <date_periods>
        <date_period ref="date_period-1"/>
      </date_periods>
      <date_types>
        <date_type ref="date_type-1"/>
        <date_type ref="date_type-2"/>
      </date_types>
    </authority>
  </authorities>
  <calendars>
    <calendar xml:id="calendar-1" eats_id="%(calendar1)d">
      <name>Julian</name>
    </calendar>
    <calendar xml:id="calendar-2" eats_id="%(calendar2)d">
      <name>Gregorian</name>
    </calendar>
  </calendars>
  <date_periods>
    <date_period xml:id="date_period-1" eats_id="%(date_period)d">
      <name>lifespan</name>
    </date_period>
  </date_periods>
  <date_types>
    <date_type xml:id="date_type-1" eats_id="%(date_type1)d">
      <name>exact</name>
    </date_type>
    <date_type xml:id="date_type-2" eats_id="%(date_type2)d">
      <name>circa</name>
    </date_type>
  </date_types>
  <entities>
    <entity xml:id="entity-1">
      <existences>
        <existence authority="authority-1">
          <dates>
            <date date_period="date_period-1">
              <assembled_form></assembled_form>
              <date_parts>
                <date_part calendar="calendar-1" certainty="full"
                           date_type="date_type-1" type="start">
                  <raw>1 January 2000</raw>
                  <normalised>2000-01-01</normalised>
                </date_part>
                <date_part calendar="calendar-2" certainty="none"
                           date_type="date_type-2" type="end">
                  <raw>21 March 2010</raw>
                  <normalised>2010-03-21</normalised>
                </date_part>
              </date_parts>
            </date>
          </dates>
        </existence>
      </existences>
    </entity>
  </entities>
</collection>''' % {
            'authority': authority.get_id(), 'calendar1': calendar1.get_id(),
            'calendar2': calendar2.get_id(),
            'date_period': date_period.get_id(),
            'date_type1': date_type1.get_id(),
            'date_type2': date_type2.get_id()}
        annotated_import = self.importer.import_xml(import_xml, self.admin)[1]
        entity = Entity.objects.all()[0]
        existence = entity.get_existences()[0]
        date = existence.get_dates()[0]
        self.assertEqual(existence.authority, authority)
        self.assertEqual(date.assembled_form,
                         '1 January 2000 \N{EN DASH} 21 March 2010?')
        self.assertEqual(date.period, date_period)
        start = date.start
        end = date.end
        self.assertEqual(start.calendar, calendar1)
        self.assertEqual(start.certainty, self.tm.date_full_certainty)
        self.assertEqual(start.date_type, date_type1)
        self.assertEqual(start.get_normalised_value(), '2000-01-01')
        self.assertEqual(start.get_value(), '1 January 2000')
        self.assertEqual(end.calendar, calendar2)
        self.assertEqual(end.certainty, self.tm.date_no_certainty)
        self.assertEqual(end.date_type, date_type2)
        self.assertEqual(end.get_normalised_value(), '2010-03-21')
        self.assertEqual(end.get_value(), '21 March 2010')
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-1" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <calendars>
    <calendar xml:id="calendar-1" eats_id="%(calendar1)d">
      <name>Julian</name>
    </calendar>
    <calendar xml:id="calendar-2" eats_id="%(calendar2)d">
      <name>Gregorian</name>
    </calendar>
  </calendars>
  <date_periods>
    <date_period xml:id="date_period-1" eats_id="%(date_period)d">
      <name>lifespan</name>
    </date_period>
  </date_periods>
  <date_types>
    <date_type xml:id="date_type-1" eats_id="%(date_type1)d">
      <name>exact</name>
    </date_type>
    <date_type xml:id="date_type-2" eats_id="%(date_type2)d">
      <name>circa</name>
    </date_type>
  </date_types>
  <entities>
    <entity xml:id="entity-1" eats_id="%(entity)d" url="%(entity_url)s">
      <existences>
        <existence authority="authority-1" eats_id="%(existence)d">
          <dates>
            <date date_period="date_period-1">
              <assembled_form></assembled_form>
              <date_parts>
                <date_part calendar="calendar-1" certainty="full"
                           date_type="date_type-1" type="start">
                  <raw>1 January 2000</raw>
                  <normalised>2000-01-01</normalised>
                </date_part>
                <date_part calendar="calendar-2" certainty="none"
                           date_type="date_type-2" type="end">
                  <raw>21 March 2010</raw>
                  <normalised>2010-03-21</normalised>
                </date_part>
              </date_parts>
            </date>
          </dates>
        </existence>
      </existences>
    </entity>
  </entities>
</collection>''' % {
            'authority': authority.get_id(), 'calendar1': calendar1.get_id(),
            'calendar2': calendar2.get_id(),
            'date_period': date_period.get_id(),
            'date_type1': date_type1.get_id(),
            'date_type2': date_type2.get_id(), 'entity': entity.get_id(),
            'existence': existence.get_id(),
            'entity_url': entity.get_eats_subject_identifier()}
        self._compare_XML(annotated_import, expected_xml)
