# -*- coding: utf-8 -*-

from io import BytesIO

from lxml import etree

from django.test import TestCase

from eats.lib.eatsml_exporter import EATSMLExporter
from eats.tests.base_test_case import BaseTestCase


class EATSMLExportTestCase (TestCase, BaseTestCase):

    def setUp (self):
        super(EATSMLExportTestCase, self).setUp()
        self.reset_managers()
        self.tm = self.create_topic_map()
        self.exporter = EATSMLExporter(self.tm)

    def _compare_XML (self, export, expected_xml):
        parser = etree.XMLParser(remove_blank_text=True)
        actual = BytesIO()
        export.write_c14n(actual)
        expected = BytesIO()
        root = etree.XML(expected_xml, parser)
        root.getroottree().write_c14n(expected)
        self.assertEqual(actual.getvalue(), expected.getvalue())

    def test_export_no_entities (self):
        export = self.exporter.export_entities([])
        expected_xml = '<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/"/>'
        self._compare_XML(export, expected_xml)

    def test_export_entity_existence (self):
        authority = self.create_authority('Test')
        entity = self.tm.create_entity()
        existence = entity.create_existence_property_assertion(authority)
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-%(entity)d" eats_id="%(entity)d" url="%(url)s">
      <existences>
        <existence authority="authority-%(authority)d" eats_id="%(existence)d"/>
      </existences>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'existence': existence.get_id(),
       'url': entity.get_eats_subject_identifier()}
        self._compare_XML(export, expected_xml)

    def test_export_entity_entity_type (self):
        authority = self.create_authority('Test')
        entity_type = self.create_entity_type('person')
        authority.set_entity_types([entity_type])
        entity = self.tm.create_entity()
        assertion = entity.create_entity_type_property_assertion(
            authority, entity_type)
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d">
      <name>Test</name>
      <entity_types>
        <entity_type ref="entity_type-%(entity_type)d"/>
      </entity_types>
    </authority>
  </authorities>
  <entity_types>
    <entity_type xml:id="entity_type-%(entity_type)d" eats_id="%(entity_type)d">
      <name>person</name>
    </entity_type>
  </entity_types>
  <entities>
    <entity xml:id="entity-%(entity)d" eats_id="%(entity)d" url="%(url)s">
      <entity_types>
        <entity_type authority="authority-%(authority)d" eats_id="%(assertion)d" entity_type="entity_type-%(entity_type)d"/>
      </entity_types>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'entity_type': entity_type.get_id(), 'assertion': assertion.get_id(),
       'url': entity.get_eats_subject_identifier()}
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
        entity = self.tm.create_entity()
        assertion = entity.create_name_property_assertion(
            authority, name_type, language, script, '', True)
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
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d">
      <name>Test</name>
      <languages>
        <language ref="language-%(language)d"/>
      </languages>
      <name_part_types>
        <name_part_type ref="name_part_type-%(family_name_part_type)d"/>
        <name_part_type ref="name_part_type-%(given_name_part_type)d"/>
      </name_part_types>
      <name_types>
        <name_type ref="name_type-%(name_type)d"/>
      </name_types>
      <scripts>
        <script ref="script-%(script)d"/>
      </scripts>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-%(language)d" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
      <name_part_types>
        <name_part_type ref="name_part_type-%(given_name_part_type)d"/>
        <name_part_type ref="name_part_type-%(family_name_part_type)d"/>
      </name_part_types>
    </language>
  </languages>
  <name_part_types>
    <name_part_type xml:id="name_part_type-%(family_name_part_type)d" eats_id="%(family_name_part_type)d">
      <name>family</name>
    </name_part_type>
    <name_part_type xml:id="name_part_type-%(given_name_part_type)d" eats_id="%(given_name_part_type)d">
      <name>given</name>
    </name_part_type>
  </name_part_types>
  <name_types>
    <name_type xml:id="name_type-%(name_type)d" eats_id="%(name_type)d">
      <name>regular</name>
    </name_type>
  </name_types>
  <scripts>
    <script xml:id="script-%(script)d" eats_id="%(script)d">
      <name>Latin</name>
      <code>Latn</code>
      <separator> </separator>
    </script>
  </scripts>
  <entities>
    <entity xml:id="entity-%(entity)d" eats_id="%(entity)d" url="%(url)s">
      <names>
        <name authority="authority-%(authority)d" eats_id="%(name)d" is_preferred="true" language="language-%(language)d" name_type="name_type-%(name_type)d" script="script-%(script)d">
          <assembled_form>Miriam Clare Frost</assembled_form>
          <display_form></display_form>
          <name_parts>
            <name_part name_part_type="name_part_type-%(given_name_part_type)d" language="language-%(language)d" script="script-%(script)d">Miriam</name_part>
            <name_part name_part_type="name_part_type-%(given_name_part_type)d" language="language-%(language)d" script="script-%(script)d">Clare</name_part>
            <name_part name_part_type="name_part_type-%(family_name_part_type)d" language="language-%(language)d" script="script-%(script)d">Frost</name_part>
          </name_parts>
        </name>
      </names>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'language': language.get_id(), 'script': script.get_id(),
       'given_name_part_type': given_name_part_type.get_id(),
       'family_name_part_type': family_name_part_type.get_id(),
       'name_type': name_type.get_id(), 'name': assertion.get_id(),
       'url': entity.get_eats_subject_identifier()}
        self._compare_XML(export, expected_xml)

    def test_export_entity_name_with_user (self):
        authority = self.create_authority('Test')
        english = self.create_language('English', 'en')
        french = self.create_language('French', 'fr')
        name_type = self.create_name_type('regular')
        latin = self.create_script('Latin', 'Latn', ' ')
        arabic = self.create_script('Arabic', 'Arab', ' ')
        authority.set_name_types([name_type])
        authority.set_languages([english, french])
        authority.set_scripts([arabic, latin])
        entity = self.tm.create_entity()
        name1 = entity.create_name_property_assertion(authority, name_type,
                                                      english, latin, 'Gerald')
        name2 = entity.create_name_property_assertion(
            authority, name_type, french, arabic, 'عبّاس', False)
        django_user = self.create_django_user('test', 'test@example.org',
                                              'password')
        user = self.create_user(django_user)
        user.editable_authorities.add(authority)
        user.set_current_authority(authority)
        user.set_language(french)
        user.set_script(latin)
        export = self.exporter.export_entities([entity], user=user)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d" user_preferred="true">
      <name>Test</name>
      <languages>
        <language ref="language-%(english)d"/>
        <language ref="language-%(french)d"/>
      </languages>
      <name_types>
        <name_type ref="name_type-%(name_type)d"/>
      </name_types>
      <scripts>
        <script ref="script-%(arabic)d"/>
        <script ref="script-%(latin)d"/>
      </scripts>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-%(english)d" eats_id="%(english)d">
      <name>English</name>
      <code>en</code>
    </language>
    <language xml:id="language-%(french)d" eats_id="%(french)d" user_preferred="true">
      <name>French</name>
      <code>fr</code>
    </language>
  </languages>
  <name_types>
    <name_type xml:id="name_type-%(name_type)d" eats_id="%(name_type)d">
      <name>regular</name>
    </name_type>
  </name_types>
  <scripts>
    <script xml:id="script-%(arabic)d" eats_id="%(arabic)d">
      <name>Arabic</name>
      <code>Arab</code>
      <separator> </separator>
    </script>
    <script xml:id="script-%(latin)d" eats_id="%(latin)d" user_preferred="true">
      <name>Latin</name>
      <code>Latn</code>
      <separator> </separator>
    </script>
  </scripts>
  <entities>
    <entity xml:id="entity-%(entity)d" eats_id="%(entity)d" url="%(url)s">
      <names>
        <name authority="authority-%(authority)d" eats_id="%(name1)d" is_preferred="true" language="language-%(english)d" name_type="name_type-%(name_type)d" script="script-%(latin)d" user_preferred="true">
          <assembled_form>Gerald</assembled_form>
          <display_form>Gerald</display_form>
        </name>
        <name authority="authority-%(authority)d" eats_id="%(name2)d" is_preferred="false" language="language-%(french)d" name_type="name_type-%(name_type)d" script="script-%(arabic)d">
          <assembled_form>عبّاس</assembled_form>
          <display_form>عبّاس</display_form>
        </name>
      </names>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'english': english.get_id(), 'french': french.get_id(),
       'arabic': arabic.get_id(), 'latin': latin.get_id(),
       'name_type': name_type.get_id(), 'name1': name1.get_id(),
       'name2': name2.get_id(), 'url': entity.get_eats_subject_identifier()}
        self._compare_XML(export, expected_xml)

    def test_export_entity_entity_relationship (self):
        authority = self.create_authority('Test')
        entity = self.tm.create_entity()
        relationship_type = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        authority.set_entity_relationship_types([relationship_type])
        other = self.tm.create_entity()
        assertion = entity.create_entity_relationship_property_assertion(
            authority, relationship_type, entity, other,
            self.tm.property_assertion_full_certainty)
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d">
      <name>Test</name>
      <entity_relationship_types>
        <entity_relationship_type ref="entity_relationship_type-%(relationship_type)d"/>
      </entity_relationship_types>
    </authority>
  </authorities>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-%(relationship_type)d" eats_id="%(relationship_type)d">
      <name>is child of</name>
      <reverse_name>is parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
  <entities>
    <entity xml:id="entity-%(entity)d" eats_id="%(entity)d" url="%(entity_url)s">
      <entity_relationships>
        <entity_relationship authority="authority-%(authority)d" certainty="full" eats_id="%(assertion)d" entity_relationship_type="entity_relationship_type-%(relationship_type)d" domain_entity="entity-%(entity)d" range_entity="entity-%(other)d"/>
      </entity_relationships>
    </entity>
    <entity xml:id="entity-%(other)d" eats_id="%(other)d" related_entity="true" url="%(other_url)s"></entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'other': other.get_id(), 'relationship_type': relationship_type.get_id(),
       'assertion': assertion.get_id(),
       'entity_url': entity.get_eats_subject_identifier(),
       'other_url': other.get_eats_subject_identifier()}
        self._compare_XML(export, expected_xml)

    def test_export_entity_note (self):
        authority = self.create_authority('Test')
        entity = self.tm.create_entity()
        note = entity.create_note_property_assertion(authority, 'A note.')
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-%(entity)d" eats_id="%(entity)d" url="%(url)s">
      <notes>
        <note authority="authority-%(authority)d" eats_id="%(note)d">A note.</note>
      </notes>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'note': note.get_id(), 'url': entity.get_eats_subject_identifier()}
        self._compare_XML(export, expected_xml)

    def test_export_entity_subject_identifier (self):
        authority = self.create_authority('Test')
        entity = self.tm.create_entity()
        assertion = entity.create_subject_identifier_property_assertion(
            authority, 'http://www.example.org/test/')
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <entities>
    <entity xml:id="entity-%(entity)d" eats_id="%(entity)d" url="%(url)s">
      <subject_identifiers>
        <subject_identifier authority="authority-%(authority)d" eats_id="%(assertion)d">http://www.example.org/test/</subject_identifier>
      </subject_identifiers>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'assertion': assertion.get_id(),
       'url': entity.get_eats_subject_identifier()}
        self._compare_XML(export, expected_xml)

    def test_export_entity_date (self):
        authority = self.create_authority('Test')
        calendar = self.create_calendar('Julian')
        authority.set_calendars([calendar])
        date_type = self.create_date_type('exact')
        authority.set_date_types([date_type])
        date_period = self.create_date_period('lifespan')
        authority.set_date_periods([date_period])
        entity = self.tm.create_entity(authority)
        existence = entity.get_existences()[0]
        certainty = self.tm.date_full_certainty
        certainty_value = 'full'
        date = existence.create_date({
                'date_period': date_period, 'start': '1 January 2001',
                'start_calendar': calendar, 'start_certainty': certainty,
                'start_normalised': '2001-01-01', 'start_type': date_type,
                })
        export = self.exporter.export_entities([entity])
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d">
      <name>Test</name>
      <calendars>
        <calendar ref="calendar-%(calendar)d"/>
      </calendars>
      <date_periods>
        <date_period ref="date_period-%(date_period)d"/>
      </date_periods>
      <date_types>
        <date_type ref="date_type-%(date_type)d"/>
      </date_types>
    </authority>
  </authorities>
  <calendars>
    <calendar xml:id="calendar-%(calendar)d" eats_id="%(calendar)d">
      <name>Julian</name>
    </calendar>
  </calendars>
  <date_periods>
    <date_period xml:id="date_period-%(date_period)d" eats_id="%(date_period)d">
      <name>lifespan</name>
    </date_period>
  </date_periods>
  <date_types>
    <date_type xml:id="date_type-%(date_type)d" eats_id="%(date_type)d">
      <name>exact</name>
    </date_type>
  </date_types>
  <entities>
    <entity xml:id="entity-%(entity)d" eats_id="%(entity)d" url="%(url)s">
      <existences>
        <existence authority="authority-%(authority)d" eats_id="%(existence)d">
          <dates>
            <date date_period="date_period-%(date_period)d">
              <assembled_form>%(date_assembled)s</assembled_form>
              <date_parts>
                <date_part type="start" calendar="calendar-%(calendar)d" date_type="date_type-%(date_type)d" certainty="%(certainty)s">
                  <raw>1 January 2001</raw>
                  <normalised>2001-01-01</normalised>
                </date_part>
              </date_parts>
            </date>
          </dates>
        </existence>
      </existences>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'entity': entity.get_id(),
       'date_assembled': date.assembled_form, 'calendar': calendar.get_id(),
       'date_type': date_type.get_id(), 'date_period': date_period.get_id(),
       'certainty': certainty_value, 'existence': existence.get_id(),
       'url': entity.get_eats_subject_identifier()}
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
        calendar = self.create_calendar('Julian')
        authority2.set_calendars([calendar])
        date_type = self.create_date_type('exact')
        authority2.set_date_types([date_type])
        date_period = self.create_date_period('lifespan')
        authority2.set_date_periods([date_period])
        export = self.exporter.export_infrastructure()
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority1)d" eats_id="%(authority1)d">
      <name>Test1</name>
      <entity_types>
        <entity_type ref="entity_type-%(person)d"/>
        <entity_type ref="entity_type-%(place)d"/>
      </entity_types>
      <languages>
        <language ref="language-%(english)d"/>
      </languages>
      <name_part_types>
        <name_part_type ref="name_part_type-%(family)d"/>
        <name_part_type ref="name_part_type-%(given)d"/>
      </name_part_types>
      <name_types>
        <name_type ref="name_type-%(regular)d"/>
      </name_types>
      <scripts>
        <script ref="script-%(latin)d"/>
      </scripts>
    </authority>
    <authority xml:id="authority-%(authority2)d" eats_id="%(authority2)d">
      <name>Test2</name>
      <calendars>
        <calendar ref="calendar-%(calendar)d"/>
      </calendars>
      <date_periods>
        <date_period ref="date_period-%(date_period)d"/>
      </date_periods>
      <date_types>
        <date_type ref="date_type-%(date_type)d"/>
      </date_types>
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
  <calendars>
    <calendar xml:id="calendar-%(calendar)d" eats_id="%(calendar)d">
      <name>Julian</name>
    </calendar>
  </calendars>
  <date_periods>
    <date_period xml:id="date_period-%(date_period)d" eats_id="%(date_period)d">
      <name>lifespan</name>
    </date_period>
  </date_periods>
  <date_types>
    <date_type xml:id="date_type-%(date_type)d" eats_id="%(date_type)d">
      <name>exact</name>
    </date_type>
  </date_types>
  <entity_relationship_types>
    <entity_relationship_type xml:id="entity_relationship_type-%(child)d" eats_id="%(child)d">
      <name>is child of</name>
      <reverse_name>is parent of</reverse_name>
    </entity_relationship_type>
  </entity_relationship_types>
  <entity_types>
    <entity_type xml:id="entity_type-%(person)d" eats_id="%(person)d">
      <name>person</name>
    </entity_type>
    <entity_type xml:id="entity_type-%(place)d" eats_id="%(place)d">
      <name>place</name>
    </entity_type>
  </entity_types>
  <languages>
    <language xml:id="language-%(english)d" eats_id="%(english)d">
      <name>English</name>
      <code>en</code>
      <name_part_types>
        <name_part_type ref="name_part_type-%(title)d"/>
        <name_part_type ref="name_part_type-%(given)d"/>
        <name_part_type ref="name_part_type-%(family)d"/>
      </name_part_types>
    </language>
    <language xml:id="language-%(french)d" eats_id="%(french)d">
      <name>French</name>
      <code>fr</code>
    </language>
  </languages>
  <name_part_types>
    <name_part_type xml:id="name_part_type-%(family)d" eats_id="%(family)d">
      <name>family</name>
    </name_part_type>
    <name_part_type xml:id="name_part_type-%(given)d" eats_id="%(given)d">
      <name>given</name>
    </name_part_type>
    <name_part_type xml:id="name_part_type-%(title)d" eats_id="%(title)d">
      <name>title</name>
    </name_part_type>
  </name_part_types>
  <name_types>
    <name_type xml:id="name_type-%(regular)d" eats_id="%(regular)d">
      <name>regular</name>
    </name_type>
  </name_types>
  <scripts>
    <script xml:id="script-%(arabic)d" eats_id="%(arabic)d">
      <name>Arabic</name>
      <code>Arab</code>
      <separator></separator>
    </script>
    <script xml:id="script-%(latin)d" eats_id="%(latin)d">
      <name>Latin</name>
      <code>Latn</code>
      <separator> </separator>
    </script>
  </scripts>
</collection>
''' % {'authority1': authority1.get_id(), 'authority2': authority2.get_id(),
       'english': english.get_id(), 'french': french.get_id(),
       'latin': latin.get_id(), 'arabic': arabic.get_id(),
       'given': given.get_id(), 'family': family.get_id(),
       'person': person.get_id(), 'place': place.get_id(),
       'regular': regular.get_id(), 'title': title.get_id(),
       'child': child.get_id(), 'calendar': calendar.get_id(),
       'date_period': date_period.get_id(), 'date_type': date_type.get_id()}
        self._compare_XML(export, expected_xml)

    def test_export_infrastructure_limited (self):
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
        french = self.create_language('French', 'fr')
        french.name_part_types = [title, given, family]
        authority1.set_languages([english])
        authority2.set_languages([french])
        child = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        latin = self.create_script('Latin', 'Latn', ' ')
        arabic = self.create_script('Arabic', 'Arab', '')
        authority1.set_scripts([latin])
        authority2.set_scripts([arabic])
        calendar = self.create_calendar('Julian')
        authority2.set_calendars([calendar])
        date_type = self.create_date_type('exact')
        authority2.set_date_types([date_type])
        date_period = self.create_date_period('lifespan')
        authority2.set_date_periods([date_period])
        django_user = self.create_django_user('test', 'test@example.org',
                                              'password')
        user = self.create_user(django_user)
        user.editable_authorities.add(authority2)
        user.set_current_authority(authority2)
        user.set_language(french)
        user.set_script(latin)
        export = self.exporter.export_infrastructure(user=user)
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority2)d" eats_id="%(authority2)d" user_preferred="true">
      <name>Test2</name>
      <calendars>
        <calendar ref="calendar-%(calendar)d"/>
      </calendars>
      <date_periods>
        <date_period ref="date_period-%(date_period)d"/>
      </date_periods>
      <date_types>
        <date_type ref="date_type-%(date_type)d"/>
      </date_types>
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
  <calendars>
    <calendar xml:id="calendar-%(calendar)d" eats_id="%(calendar)d">
      <name>Julian</name>
    </calendar>
  </calendars>
  <date_periods>
    <date_period xml:id="date_period-%(date_period)d" eats_id="%(date_period)d">
      <name>lifespan</name>
    </date_period>
  </date_periods>
  <date_types>
    <date_type xml:id="date_type-%(date_type)d" eats_id="%(date_type)d">
      <name>exact</name>
    </date_type>
  </date_types>
  <entity_types>
    <entity_type xml:id="entity_type-%(place)d" eats_id="%(place)d">
      <name>place</name>
    </entity_type>
  </entity_types>
  <languages>
    <language xml:id="language-%(french)d" eats_id="%(french)d" user_preferred="true">
      <name>French</name>
      <code>fr</code>
      <name_part_types>
        <name_part_type ref="name_part_type-%(family)d"/>
      </name_part_types>
    </language>
  </languages>
  <name_part_types>
    <name_part_type xml:id="name_part_type-%(family)d" eats_id="%(family)d">
      <name>family</name>
    </name_part_type>
  </name_part_types>
  <scripts>
    <script xml:id="script-%(arabic)d" eats_id="%(arabic)d">
      <name>Arabic</name>
      <code>Arab</code>
      <separator></separator>
    </script>
  </scripts>
</collection>
''' % {'authority2': authority2.get_id(), 'place': place.get_id(),
       'french': french.get_id(), 'family': family.get_id(),
       'arabic': arabic.get_id(), 'calendar': calendar.get_id(),
       'date_period': date_period.get_id(), 'date_type': date_type.get_id()}
        self._compare_XML(export, expected_xml)

    def test_export_full (self):
        authority = self.create_authority('Test')
        language = self.create_language('English', 'en')
        calendar = self.create_calendar('Gregorian')
        entity = self.tm.create_entity(authority)
        existence = entity.get_existences()[0]
        export = self.exporter.export_full()
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <calendars>
    <calendar xml:id="calendar-%(calendar)d" eats_id="%(calendar)d">
      <name>Gregorian</name>
    </calendar>
  </calendars>
  <languages>
    <language xml:id="language-%(language)d" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
    </language>
  </languages>
  <entities>
    <entity xml:id="entity-%(entity)d" eats_id="%(entity)d" url="%(url)s">
      <existences>
        <existence authority="authority-%(authority)d" eats_id="%(existence)d"/>
      </existences>
    </entity>
  </entities>
</collection>
''' % {'authority': authority.get_id(), 'calendar': calendar.get_id(),
       'language': language.get_id(), 'entity': entity.get_id(),
       'existence': existence.get_id(),
       'url': entity.get_eats_subject_identifier()}
        self._compare_XML(export, expected_xml)

    def test_export_full_no_entities (self):
        authority = self.create_authority('Test')
        language = self.create_language('English', 'en')
        export = self.exporter.export_full()
        expected_xml = '''
<collection xmlns="http://eats.artefact.org.nz/ns/eatsml/">
  <authorities>
    <authority xml:id="authority-%(authority)d" eats_id="%(authority)d">
      <name>Test</name>
    </authority>
  </authorities>
  <languages>
    <language xml:id="language-%(language)d" eats_id="%(language)d">
      <name>English</name>
      <code>en</code>
    </language>
  </languages>
</collection>
''' % {'authority': authority.get_id(), 'language': language.get_id()}
        self._compare_XML(export, expected_xml)
