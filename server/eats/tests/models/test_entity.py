from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from eats.exceptions import EATSMergedIdentifierException
from eats.models import Entity, EntityRelationshipPropertyAssertion, ExistencePropertyAssertion, Name, NameCache, NameIndex, NamePropertyAssertion
from eats.tests.models.model_test_case import ModelTestCase


class EntityTestCase (ModelTestCase):

    def setUp (self):
        super(EntityTestCase, self).setUp()
        self.authority2 = self.create_authority('Test2')
        self.name_type = self.create_name_type('regular')
        self.language1 = self.create_language('English', 'en')
        self.language2 = self.create_language('Arabic', 'ar')
        self.script1 = self.create_script('Latin', 'Latn', ' ')
        self.script2 = self.create_script('Arabic', 'Arab', ' ')
        self.authority.set_languages([self.language1, self.language2])
        self.authority.set_name_types([self.name_type])
        self.authority.set_scripts([self.script1, self.script2])
        self.authority2.set_languages([self.language1, self.language2])
        self.authority2.set_name_types([self.name_type])
        self.authority2.set_scripts([self.script1, self.script2])

    def test_get_eats_subject_identifier (self):
        entity = self.tm.create_entity()
        self.assertEqual(len(entity.get_subject_identifiers()), 1)
        view_url = reverse('entity-view', kwargs={'entity_id': entity.get_id()})
        url = 'http://%s%s' % (Site.objects.get_current().domain, view_url)
        subject_identifier = entity.get_eats_subject_identifier()
        self.assertEqual(subject_identifier.address, url)

    def test_get_eats_names (self):
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(len(entity.get_eats_names()), 0)
        name1 = entity.create_name_property_assertion(
            self.authority, self.name_type, self.language1, self.script1,
            'Name1')
        names = entity.get_eats_names()
        self.assertEqual(len(names), 1)
        self.assertTrue(name1 in names)
        name2 = entity.create_name_property_assertion(
            self.authority, self.name_type, self.language2, self.script1,
            'Name2')
        names = entity.get_eats_names()
        self.assertEqual(len(names), 2)
        self.assertTrue(name1 in names)
        self.assertTrue(name2 in names)
        names = entity.get_eats_names(exclude=name1)
        self.assertEqual(len(names), 1)
        self.assertTrue(name2 in names)

    def test_get_existence_dates (self):
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(len(entity.get_existence_dates()), 0)
        calendar = self.create_calendar('Gregorian')
        date_type = self.create_date_type('exact')
        date_period = self.create_date_period('lifespan')
        self.authority.set_calendars([calendar])
        self.authority.set_date_types([date_type])
        self.authority.set_date_periods([date_period])
        existence = entity.get_existences()[0]
        date1 = existence.create_date(
            {'point': '1 January 1900', 'point_calendar': calendar,
             'point_certainty': self.tm.date_full_certainty,
             'point_normalised': '', 'point_type': date_type,
             'date_period': date_period})
        dates = entity.get_existence_dates()
        self.assertEqual(len(dates), 1)
        self.assertTrue(date1 in dates)
        date2 = existence.create_date(
            {'point': '2 January 1900', 'point_calendar': calendar,
             'point_certainty': self.tm.date_full_certainty,
             'point_normalised': '', 'point_type': date_type,
             'date_period': date_period})
        dates = entity.get_existence_dates()
        self.assertEqual(len(dates), 2)
        self.assertTrue(date1 in dates)
        self.assertTrue(date2 in dates)
        entity2 = self.tm.create_entity(self.authority)
        date3 = entity2.get_existences()[0].create_date(
            {'point': '3 January 1900', 'point_calendar': calendar,
             'point_certainty': self.tm.date_full_certainty,
             'point_normalised': '', 'point_type': date_type,
             'date_period': date_period})
        dates = entity.get_existence_dates()
        self.assertEqual(len(dates), 2)
        self.assertTrue(date1 in dates)
        self.assertTrue(date2 in dates)
        self.assertTrue(date3 not in dates)

    def test_get_preferred_name (self):
        entity = self.tm.create_entity(self.authority)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script1)
        self.assertEqual(preferred_name, None)
        name1 = entity.create_name_property_assertion(
            self.authority, self.name_type, self.language1, self.script1,
            'Name1', False)
        # With a single name, get_preferred_name will return in that
        # one name regardless of the parameters.
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script1)
        self.assertEqual(name1, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language1, self.script1)
        self.assertEqual(name1, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language2, self.script1)
        self.assertEqual(name1, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script2)
        self.assertEqual(name1, preferred_name)
        # Create a second name, differing from the first in language.
        name2 = entity.create_name_property_assertion(
            self.authority, self.name_type, self.language2, self.script1,
            'Name2', True)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script1)
        self.assertEqual(name1, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language2, self.script1)
        self.assertEqual(name2, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language2, self.script1)
        self.assertEqual(name2, preferred_name)
        # Create a third name, differing from the first in authority.
        name3 = entity.create_name_property_assertion(
            self.authority2, self.name_type, self.language1, self.script1,
            'Name3', True)
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language1, self.script1)
        self.assertEqual(name3, preferred_name)
        preferred_name = entity.get_preferred_name(
            None, self.language2, self.script1)
        self.assertEqual(name2, preferred_name)
        # Authority trumps language.
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language2, self.script1)
        self.assertEqual(name3, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script1)
        self.assertEqual(name1, preferred_name)
        # Create a fourth name, differing from the first in script and
        # authority.
        name4 = entity.create_name_property_assertion(
            self.authority2, self.name_type, self.language2, self.script2,
            'Name4', True)
        # Script trumps authority.
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language1, self.script1)
        self.assertEqual(name3, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language1, self.script2)
        self.assertEqual(name4, preferred_name)
        # Script trumps language.
        preferred_name = entity.get_preferred_name(
            self.authority, self.language2, self.script2)
        self.assertEqual(name4, preferred_name)
        # Create a fifth name, differing from the first in is_preferred.
        name5 = entity.create_name_property_assertion(
            self.authority, self.name_type, self.language1, self.script1,
            'Name5', True)
        # is_preferred trumps not is_preferred.
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script1)
        self.assertEqual(name5, preferred_name)

    def test_manager_filter_by_entity_type (self):
        self.assertEqual(Entity.objects.count(), 0)
        entity_type_1 = self.create_entity_type('person')
        entity_type_2 = self.create_entity_type('place')
        self.authority.set_entity_types([entity_type_1, entity_type_2])
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_1.id).count(), 0)
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_2.id).count(), 0)
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(Entity.objects.count(), 1)
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_1.id).count(), 0)
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_2.id).count(), 0)
        assertion1 = entity.create_entity_type_property_assertion(
            self.authority, entity_type_1)
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_1.id).count(), 1)
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_2.id).count(), 0)
        assertion2 = entity.create_entity_type_property_assertion(
            self.authority, entity_type_2)
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_1.id).count(), 1)
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_2.id).count(), 1)
        assertion1.remove()
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_1.id).count(), 0)
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_2.id).count(), 1)
        assertion2.remove()
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_1.id).count(), 0)
        self.assertEqual(Entity.objects.filter_by_entity_type(
                entity_type_2.id).count(), 0)

    def test_simple_merge (self):
        # Test merging of two entities that only have property
        # assertions from the same authority, with no dates or entity
        # relationships.
        entity1 = self.tm.create_entity(self.authority)
        entity2 = self.tm.create_entity(self.authority)
        si1 = set(entity1.get_eats_subject_identifiers())
        si2 = set(entity1.get_eats_subject_identifiers())
        entity1_id = entity1.get_id()
        entity2_id = entity2.get_id()
        self.assertEqual(Entity.objects.count(), 2)
        name1 = entity1.create_name_property_assertion(
            self.authority, self.name_type, self.language1, self.script1,
            'Name1', False)
        name2 = entity2.create_name_property_assertion(
            self.authority, self.name_type, self.language1, self.script1,
            'Name1', False)
        self.assertEqual(Name.objects.count(), 2)
        entity1.merge_in(entity2)
        self.assertEqual(Entity.objects.count(), 1)
        self.assertEqual(Entity.objects.all()[0], entity1)
        self.assertEqual(set(entity1.get_eats_subject_identifiers()), si1 & si2)
        self.assertEqual(set(entity1.get_eats_names()), set([name1, name2]))
        self.assertEqual(entity1.get_id(), entity1_id)
        self.assertRaises(EATSMergedIdentifierException,
                          Entity.objects.get_by_identifier, entity2_id)

    def test_date_merge (self):
        # Test that two identical entity type property assertions are
        # merged into one.
        entity1 = self.tm.create_entity(self.authority)
        entity2 = self.tm.create_entity(self.authority)
        entity_type = self.create_entity_type('Person')
        self.authority.set_entity_types([entity_type])
        entity_type1 = entity1.create_entity_type_property_assertion(
            self.authority, entity_type)
        entity_type2 = entity2.create_entity_type_property_assertion(
            self.authority, entity_type)
        entity1.merge_in(entity2)
        self.assertEqual(set(entity1.get_entity_types()), set([entity_type1]))
        # Test that having a date on an otherwise identical entity
        # type property assertions means that the two are not merged
        # into one.
        entity3 = self.tm.create_entity(self.authority)
        date_period = self.create_date_period('lifespan')
        calendar = self.create_calendar('Gregorian')
        date_type = self.create_date_type('exact')
        self.authority.set_date_periods([date_period])
        self.authority.set_calendars([calendar])
        self.authority.set_date_types([date_type])
        entity_type3 = entity3.create_entity_type_property_assertion(
            self.authority, entity_type)
        entity_type3.create_date({
            'point': '1 January 1930', 'point_calendar': calendar,
            'point_type': date_type, 'point_normalised': '1930-01-01',
            'point_certainty': self.tm.date_full_certainty,
            'date_period': date_period})
        entity1.merge_in(entity3)
        self.assertEqual(set(entity1.get_entity_types()),
                         set([entity_type1, entity_type3]))

    def test_entity_relationship_merge (self):
        entity1 = self.tm.create_entity(self.authority)
        entity2 = self.tm.create_entity(self.authority)
        entity3 = self.tm.create_entity(self.authority)
        entity_relationship_type = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        self.authority.set_entity_relationship_types(
            [entity_relationship_type])
        er1 = entity2.create_entity_relationship_property_assertion(
            self.authority, entity_relationship_type, entity2, entity3,
            self.tm.property_assertion_full_certainty)
        er2 = entity2.create_entity_relationship_property_assertion(
            self.authority, entity_relationship_type, entity2, entity1,
            self.tm.property_assertion_no_certainty)
        self.assertEqual(EntityRelationshipPropertyAssertion.objects.count(), 2)
        entity1.merge_in(entity2)
        self.assertEqual(EntityRelationshipPropertyAssertion.objects.count(), 2)
        self.assertEqual(Entity.objects.count(), 2)
        self.assertEqual(set(entity1.get_entity_relationships()),
                         set([er1, er2]))

    def test_remove (self):
        self.assertEqual(Entity.objects.count(), 0)
        self.assertEqual(ExistencePropertyAssertion.objects.count(), 0)
        # Create an entity with no property assertions.
        entity = self.tm.create_entity()
        self.assertEqual(Entity.objects.count(), 1)
        self.assertEqual(ExistencePropertyAssertion.objects.count(), 0)
        entity.remove()
        self.assertEqual(Entity.objects.count(), 0)
        self.assertEqual(ExistencePropertyAssertion.objects.count(), 0)
        # Create an entity with an existence property assertion.
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(Entity.objects.count(), 1)
        self.assertEqual(ExistencePropertyAssertion.objects.count(), 1)
        entity.remove()
        self.assertEqual(Entity.objects.count(), 0)
        self.assertEqual(ExistencePropertyAssertion.objects.count(), 0)
        entity = self.tm.create_entity()
        entity2 = self.tm.create_entity()
        self.assertEqual(Entity.objects.count(), 2)
        self.assertEqual(EntityRelationshipPropertyAssertion.objects.count(), 0)
        entity_relationship_type = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        self.authority.set_entity_relationship_types(
            [entity_relationship_type])
        entity.create_entity_relationship_property_assertion(
            self.authority, entity_relationship_type, entity, entity2,
            self.tm.property_assertion_full_certainty)
        self.assertEqual(EntityRelationshipPropertyAssertion.objects.count(), 1)
        entity.remove()
        self.assertEqual(Entity.objects.count(), 1)
        self.assertEqual(EntityRelationshipPropertyAssertion.objects.count(), 0)
        entity2.remove()
        # Test removal of an entity with a name, since names are
        # referenced from other models.
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(Entity.objects.count(), 1)
        self.assertEqual(Name.objects.count(), 0)
        self.assertEqual(NameCache.objects.count(), 0)
        self.assertEqual(NameIndex.objects.count(), 0)
        self.assertEqual(NamePropertyAssertion.objects.count(), 0)
        entity.create_name_property_assertion(
            self.authority, self.name_type, self.language1, self.script1,
            'Name', False)
        self.assertEqual(Name.objects.count(), 1)
        self.assertEqual(NameCache.objects.count(), 1)
        self.assertEqual(NameIndex.objects.count(), 1)
        self.assertEqual(NamePropertyAssertion.objects.count(), 1)
        entity.remove()
        self.assertEqual(Entity.objects.count(), 0)
        self.assertEqual(Name.objects.count(), 0)
        self.assertEqual(NameCache.objects.count(), 0)
        self.assertEqual(NameIndex.objects.count(), 0)
        self.assertEqual(NamePropertyAssertion.objects.count(), 0)

    def test_traverse_to_entity (self):
        entity_relationship_type = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        self.authority.set_entity_relationship_types([entity_relationship_type])
        entity1 = self.tm.create_entity(self.authority)
        entity2 = self.tm.create_entity(self.authority)
        assertion = entity1.create_entity_relationship_property_assertion(
            self.authority, entity_relationship_type, entity1, entity2,
            self.tm.property_assertion_full_certainty)
        self.assertEqual(entity1.get_assertion(assertion.get_id()), assertion)
        self.assertEqual(entity2.get_assertion(assertion.get_id()), assertion)
