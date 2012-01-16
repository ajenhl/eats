from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

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
        self.assertEqual(len(entity.subject_identifiers.all()), 1)
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
