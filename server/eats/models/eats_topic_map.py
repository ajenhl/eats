from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models import Q

from tmapi.models import Locator, TopicMap

from eats.constants import ADMIN_NAME_TYPE_IRI, AUTHORITY_HAS_CALENDAR_ASSOCIATION_TYPE_IRI, AUTHORITY_HAS_DATE_PERIOD_ASSOCIATION_TYPE_IRI, AUTHORITY_HAS_DATE_TYPE_ASSOCIATION_TYPE_IRI, AUTHORITY_HAS_ENTITY_RELATIONSHIP_TYPE_ASSOCIATION_TYPE_IRI, AUTHORITY_HAS_ENTITY_TYPE_ASSOCIATION_TYPE_IRI, AUTHORITY_HAS_LANGUAGE_ASSOCIATION_TYPE_IRI, AUTHORITY_HAS_NAME_PART_TYPE_ASSOCIATION_TYPE_IRI, AUTHORITY_HAS_NAME_TYPE_ASSOCIATION_TYPE_IRI, AUTHORITY_HAS_SCRIPT_ASSOCIATION_TYPE_IRI, AUTHORITY_ROLE_TYPE_IRI, AUTHORITY_TYPE_IRI, CALENDAR_TYPE_IRI, DATE_CERTAINTY_TYPE_IRI, DATE_FULL_CERTAINTY_IRI, DATE_NO_CERTAINTY_IRI, DATE_PERIOD_ASSOCIATION_TYPE, DATE_PERIOD_ROLE_TYPE, DATE_PERIOD_TYPE_IRI, DATE_ROLE_TYPE_IRI, DATE_TYPE_IRI, DATE_TYPE_TYPE_IRI, DOMAIN_ENTITY_ROLE_TYPE_IRI, END_DATE_TYPE_IRI, END_TAQ_DATE_TYPE_IRI, END_TPQ_DATE_TYPE_IRI, ENTITY_RELATIONSHIP_ASSERTION_TYPE_IRI, ENTITY_RELATIONSHIP_TYPE_ROLE_TYPE_IRI, ENTITY_RELATIONSHIP_TYPE_TYPE_IRI, ENTITY_ROLE_TYPE_IRI, ENTITY_TYPE_IRI, ENTITY_TYPE_ASSERTION_TYPE_IRI, ENTITY_TYPE_TYPE_IRI, EXISTENCE_IRI, EXISTENCE_ASSERTION_TYPE_IRI, INFRASTRUCTURE_ROLE_TYPE_IRI, IS_IN_LANGUAGE_TYPE_IRI, IS_IN_SCRIPT_TYPE_IRI, IS_PREFERRED_IRI, LANGUAGE_CODE_TYPE_IRI, LANGUAGE_ROLE_TYPE_IRI, LANGUAGE_TYPE_IRI, NAME_ASSERTION_TYPE_IRI, NAME_HAS_NAME_PART_ASSOCIATION_TYPE_IRI, NAME_PART_ORDER_TYPE_IRI, NAME_PART_ROLE_TYPE_IRI, NAME_PART_TYPE_IRI, NAME_PART_TYPE_ORDER_IN_LANGUAGE_TYPE_IRI, NAME_PART_TYPE_TYPE_IRI, NAME_ROLE_TYPE_IRI, NAME_TYPE_IRI, NAME_TYPE_TYPE_IRI, NORMALISED_DATE_FORM_TYPE_IRI, NOTE_ASSERTION_TYPE_IRI, POINT_DATE_TYPE_IRI, POINT_TAQ_DATE_TYPE_IRI, POINT_TPQ_DATE_TYPE_IRI, PROPERTY_ASSERTION_CERTAINTY_TYPE_IRI, PROPERTY_ASSERTION_FULL_CERTAINTY_IRI, PROPERTY_ASSERTION_NO_CERTAINTY_IRI, PROPERTY_ROLE_TYPE_IRI, RANGE_ENTITY_ROLE_TYPE_IRI, RELATIONSHIP_NAME_TYPE_IRI, REVERSE_RELATIONSHIP_NAME_TYPE_IRI, SCRIPT_CODE_TYPE_IRI, SCRIPT_ROLE_TYPE_IRI, SCRIPT_SEPARATOR_TYPE_IRI, SCRIPT_TYPE_IRI, START_DATE_TYPE_IRI, START_TAQ_DATE_TYPE_IRI, START_TPQ_DATE_TYPE_IRI, SUBJECT_IDENTIFIER_ASSERTION_TYPE_IRI
from eats.exceptions import EATSException
from eats.lib.name_form import create_name_forms
from .authority import Authority
from .calendar import Calendar
from .date_period import DatePeriod
from .date_type import DateType
from .entity import Entity
from .entity_relationship_property_assertion import EntityRelationshipPropertyAssertion
from .entity_relationship_type import EntityRelationshipType
from .entity_type import EntityType
from .entity_type_property_assertion import EntityTypePropertyAssertion
from .existence_property_assertion import ExistencePropertyAssertion
from .language import Language
from .name_part_type import NamePartType
from .name_property_assertion import NamePropertyAssertion
from .name_type import NameType
from .script import Script


class EATSTopicMap (TopicMap):

    class Meta:
        proxy = True

    @property
    def admin_name_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                ADMIN_NAME_TYPE_IRI), '_admin_name_type')

    @property
    def authority_has_calendar_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(AUTHORITY_HAS_CALENDAR_ASSOCIATION_TYPE_IRI),
            '_authority_has_calendar_association_type')

    @property
    def authority_has_date_period_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(AUTHORITY_HAS_DATE_PERIOD_ASSOCIATION_TYPE_IRI),
            '_authority_has_date_period_association_type')

    @property
    def authority_has_date_type_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(AUTHORITY_HAS_DATE_TYPE_ASSOCIATION_TYPE_IRI),
            '_authority_has_date_type_association_type')

    @property
    def authority_has_entity_relationship_type_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(AUTHORITY_HAS_ENTITY_RELATIONSHIP_TYPE_ASSOCIATION_TYPE_IRI),
            '_authority_has_entity_relationship_type_association_type')

    @property
    def authority_has_entity_type_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(AUTHORITY_HAS_ENTITY_TYPE_ASSOCIATION_TYPE_IRI),
            '_authority_has_entity_type_association_type')

    @property
    def authority_has_language_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(AUTHORITY_HAS_LANGUAGE_ASSOCIATION_TYPE_IRI),
            '_authority_has_language_association_type')

    @property
    def authority_has_name_part_type_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(AUTHORITY_HAS_NAME_PART_TYPE_ASSOCIATION_TYPE_IRI),
            '_authority_has_name_part_type_association_type')

    @property
    def authority_has_name_type_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(AUTHORITY_HAS_NAME_TYPE_ASSOCIATION_TYPE_IRI),
            '_authority_has_name_type_association_type')

    @property
    def authority_has_script_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(AUTHORITY_HAS_SCRIPT_ASSOCIATION_TYPE_IRI),
            '_authority_has_script_association_type')

    @property
    def authority_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                AUTHORITY_ROLE_TYPE_IRI), '_authority_role_type')

    @property
    def authority_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                AUTHORITY_TYPE_IRI), '_authority_type')

    @property
    def calendar_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                CALENDAR_TYPE_IRI), '_calendar_type')

    def create_authority (self, name):
        """Creates a new authority called `name`.

        :param name: name of the new authority
        :type name: `str`
        :rtype: `Authority`

        """
        try:
            Authority.objects.get_by_admin_name(name)
            # Raise a more specific exception.
            raise EATSException('An authority named "%s" already exists' %
                                name)
        except Authority.DoesNotExist:
            authority = self.create_topic(proxy=Authority)
            authority.add_type(self.authority_type)
            authority.create_name(name, name_type=self.admin_name_type)
            return authority

    def create_calendar (self, name):
        """Creates a new calendar called `name`.

        :param name: name of the new calendar
        :type name: `str`
        :rtype: `Calendar`

        """
        try:
            Calendar.objects.get_by_admin_name(name)
            # QAZ: Raise a more specific exception.
            raise EATSException('A calendar named "%s" already exists' % name)
        except Calendar.DoesNotExist:
            pass
        calendar = self.create_topic(proxy=Calendar)
        calendar.add_type(self.calendar_type)
        calendar.create_name(name, name_type=self.admin_name_type)
        return calendar

    def create_date_period (self, name):
        """Creates a new date period called `name`.

        :param name: name of the new date period
        :type name: `str`
        :rtype: `DatePeriod`

        """
        try:
            DatePeriod.objects.get_by_admin_name(name)
            # QAZ: Raise a more specific exception.
            raise EATSException('A date period named "%s" already exists' %
                                name)
        except DatePeriod.DoesNotExist:
            pass
        date_period = self.create_topic(proxy=DatePeriod)
        date_period.add_type(self.date_period_type)
        date_period.create_name(name, name_type=self.admin_name_type)
        return date_period

    def create_date_type (self, name):
        """Creates a new date type called `name`.

        :param name: name of the new date type
        :type name: `str`
        :rtype: `DateType`

        """
        try:
            DateType.objects.get_by_admin_name(name)
            # QAZ: Raise a more specific exception.
            raise EATSException('A date type named "%s" already exists' % name)
        except DateType.DoesNotExist:
            pass
        date_type = self.create_topic(proxy=DateType)
        date_type.add_type(self.date_type_type)
        date_type.create_name(name, name_type=self.admin_name_type)
        return date_type

    def create_entity (self, authority=None):
        """Creates a new entity.

        If `authority` is specified, create an accompanying existence
        property assertion.

        :param authority: authority used in the existence property assertion
        :type authority: `Topic`
        :rtype: `Entity`

        """
        entity = self.create_topic(proxy=Entity)
        entity_si = self.get_entity_subject_identifier(entity.get_id())
        entity.add_subject_identifier(entity_si)
        entity.add_type(self.entity_type)
        if authority is not None:
            entity.create_existence_property_assertion(authority)
        return entity

    def create_entity_relationship_type (self, name, reverse_name):
        """Creates a new entity relationship type.

        :param name: forward name of the new entity relationship type
        :type name: `str`
        :param reverse_name: reverse name of the new entity relationship type
        :type reverse_name: `str`
        :rtype: `EntityRelationshipType`

        """
        try:
            EntityRelationshipType.objects.get_by_admin_name(name, reverse_name)
            # QAZ: Raise a more specific exception.
            raise EATSException(
                'An entity relationship type named "%s" already exists' % name)
        except EntityRelationshipType.DoesNotExist:
            pass
        entity_relationship_type = self.create_topic(
            proxy=EntityRelationshipType)
        entity_relationship_type.add_type(self.entity_relationship_type_type)
        entity_relationship_type.create_name(
            name, name_type=self.relationship_name_type)
        entity_relationship_type.create_name(
            reverse_name, name_type=self.reverse_relationship_name_type)
        return entity_relationship_type

    def create_entity_type (self, name):
        """Creates a new entity type called `name`.

        :param name: name of the new entity type
        :type name: `str`
        :rtype: `EntityType`

        """
        try:
            EntityType.objects.get_by_admin_name(name)
            # QAZ: Raise a more specific exception.
            raise EATSException('An entity type named "%s" already exists' %
                                name)
        except EntityType.DoesNotExist:
            pass
        entity_type = self.create_topic(proxy=EntityType)
        entity_type.add_type(self.entity_type_type)
        entity_type.create_name(name, name_type=self.admin_name_type)
        return entity_type

    def create_language (self, name, code):
        """Creates a new language called `name`, with ISO code `code`.

        :param name: name of the new language
        :type name: `str`
        :param code: ISO code of the new language
        :type code: string
        :rtype: `Language`

        """
        try:
            Language.objects.get_by_admin_name(name)
            # QAZ: Raise a more specific exception.
            raise EATSException('A language named "%s" already exists' % name)
        except Language.DoesNotExist:
            pass
        try:
            Language.objects.get_by_code(code)
            # QAZ: Raise a more specific exception.
            raise EATSException('A language coded "%s" already exists' % code)
        except Language.DoesNotExist:
            pass
        language = self.create_topic(proxy=Language)
        language.add_type(self.language_type)
        language.create_name(name, name_type=self.admin_name_type)
        language.create_name(code, name_type=self.language_code_type)
        return language

    def create_name_part_type (self, name):
        """Creates a new name part type called `name`.

        :param name: name of the new name part type
        :type name: `str`
        :rtype: `NamePartType`

        """
        try:
            NamePartType.objects.get_by_admin_name(name)
            # QAZ: Raise a more specific exception.
            raise EATSException('A name part type named "%s" already exists' %
                                name)
        except NamePartType.DoesNotExist:
            pass
        name_part_type = self.create_topic(proxy=NamePartType)
        name_part_type.add_type(self.name_part_type_type)
        name_part_type.create_name(name, name_type=self.admin_name_type)
        return name_part_type

    def create_name_type (self, name):
        """Creates a new name type called `name`.

        :param name: name of the new name type
        :type name: `str`
        :rtype: `NameType`

        """
        try:
            NameType.objects.get_by_admin_name(name)
            # QAZ: Raise a more specific exception.
            raise EATSException('A name type named "%s" already exists' % name)
        except NameType.DoesNotExist:
            pass
        name_type = self.create_topic(proxy=NameType)
        name_type.add_type(self.name_type_type)
        name_type.create_name(name, name_type=self.admin_name_type)
        return name_type

    def create_script (self, name, code, separator):
        """Creates a new script called `name`, with ISO code `code`.

        :param name: name of the new script
        :type name: `str`
        :param code: ISO code of the new script
        :type code: string
        :param separator: separator to be used between name parts
        :type separator: `str`
        :rtype: `Script`

        """
        try:
            Script.objects.get_by_admin_name(name)
            # QAZ: Raise a more specific exception with error message.
            raise EATSException('A script named "%s" already exists' % name)
        except Script.DoesNotExist:
            pass
        try:
            Script.objects.get_by_code(code)
            # QAZ: Raise a more specific exception with error message.
            raise Exception('A script coded "%s" already exists' % code)
        except Script.DoesNotExist:
            pass
        script = self.create_topic(proxy=Script)
        script.add_type(self.script_type)
        script.create_name(name, name_type=self.admin_name_type)
        script.create_name(code, name_type=self.script_code_type)
        script.separator = separator
        return script

    def create_topic_by_subject_identifier (self, locator, attr=None):
        if attr is None:
            return super(EATSTopicMap, self).create_topic_by_subject_identifier(
                locator)
        value = getattr(self, attr, None)
        if value is None:
            value = super(EATSTopicMap, self).create_topic_by_subject_identifier(locator)
            setattr(self, attr, value)
        return value

    @property
    def date_certainty_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                DATE_CERTAINTY_TYPE_IRI), '_date_certainty_type')

    @property
    def date_full_certainty (self):
        if not hasattr(self, '_date_full_certainty'):
            self._date_full_certainty = self.create_topic_by_subject_identifier(
                Locator(DATE_FULL_CERTAINTY_IRI))
            self._date_full_certainty.add_type(self.date_certainty_type)
        return self._date_full_certainty

    @property
    def date_no_certainty (self):
        if not hasattr(self, '_date_no_certainty'):
            self._date_no_certainty = self.create_topic_by_subject_identifier(
                Locator(DATE_NO_CERTAINTY_IRI))
            self._date_no_certainty.add_type(self.date_certainty_type)
        return self._date_no_certainty

    @property
    def date_period_association_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                DATE_PERIOD_ASSOCIATION_TYPE), '_date_period_association_type')

    @property
    def date_period_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                DATE_PERIOD_ROLE_TYPE), '_date_period_role_type')

    @property
    def date_period_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                DATE_PERIOD_TYPE_IRI), '_date_period_type')

    @property
    def date_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                DATE_ROLE_TYPE_IRI), '_date_role_type')

    @property
    def date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                DATE_TYPE_IRI), '_date_type')

    @property
    def date_type_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                DATE_TYPE_TYPE_IRI), '_date_type_type')

    @property
    def domain_entity_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                DOMAIN_ENTITY_ROLE_TYPE_IRI), '_domain_entity_role_type')

    @property
    def end_date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                END_DATE_TYPE_IRI), '_end_date_type')

    @property
    def end_taq_date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                END_TAQ_DATE_TYPE_IRI), '_end_taq_date_type')

    @property
    def end_tpq_date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                END_TPQ_DATE_TYPE_IRI), '_end_tpq_date_type')

    @property
    def entity_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                ENTITY_ROLE_TYPE_IRI), '_entity_role_type')

    @property
    def entity_type_assertion_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                ENTITY_TYPE_ASSERTION_TYPE_IRI), '_entity_type_assertion_type')

    @property
    def entity_relationship_assertion_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(ENTITY_RELATIONSHIP_ASSERTION_TYPE_IRI),
            '_entity_relationship_assertion_type')

    @property
    def entity_relationship_type_role_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(ENTITY_RELATIONSHIP_TYPE_ROLE_TYPE_IRI),
            '_entity_relationship_type_role_type')

    @property
    def entity_relationship_type_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                ENTITY_RELATIONSHIP_TYPE_TYPE_IRI), '_entity_relationship_type')

    @property
    def entity_type (self):
        return self.create_topic_by_subject_identifier(Locator(ENTITY_TYPE_IRI),
                                                       '_entity_type')

    @property
    def entity_type_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                ENTITY_TYPE_TYPE_IRI), '_entity_type_type')

    @property
    def existence (self):
        """Returns the existence topic, that serves as the property
        topic for all existences.

        :rtype: `Topic`

        """
        return self.create_topic_by_subject_identifier(
            Locator(EXISTENCE_IRI), '_existence')

    @property
    def existence_assertion_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                EXISTENCE_ASSERTION_TYPE_IRI), '_existence_assertion_type')

    def get_assertion_type (self, assertion):
        """Returns the specific class of `assertion`.

        :param assertion: property assertion
        :type assertion: `PropertyAssertion`
        :rtype: class or None

        """
        association_type = assertion.get_type()
        if association_type == self.entity_relationship_assertion_type:
            assertion_class = EntityRelationshipPropertyAssertion
        elif association_type == self.entity_type_assertion_type:
            assertion_class = EntityTypePropertyAssertion
        elif association_type == self.existence_assertion_type:
            assertion_class = ExistencePropertyAssertion
        elif association_type == self.name_assertion_type:
            assertion_class = NamePropertyAssertion
        else:
            assertion_class = None
        return assertion_class

    def get_entity_subject_identifier (self, entity_id):
        view_url = reverse('entity-view', kwargs={'entity_id': entity_id})
        url = 'http://%s%s' % (Site.objects.get_current().domain, view_url)
        return Locator(url)

    @property
    def infrastructure_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                INFRASTRUCTURE_ROLE_TYPE_IRI), '_infrastructure_role_type')

    @property
    def is_in_language_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                IS_IN_LANGUAGE_TYPE_IRI), '_is_in_language_type')

    @property
    def is_in_script_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                IS_IN_SCRIPT_TYPE_IRI), '_is_in_script_type')

    @property
    def is_preferred (self):
        """Returns the is_preferred topic, that is used as a scoping
        topic for all preferred property assertions.

        :rtype: `Topic`

        """
        return self.create_topic_by_subject_identifier(Locator(
                IS_PREFERRED_IRI), '_is_preferred')

    @property
    def language_code_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                LANGUAGE_CODE_TYPE_IRI), '_language_code_type')

    @property
    def language_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                LANGUAGE_ROLE_TYPE_IRI), '_language_role_type')

    @property
    def language_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                LANGUAGE_TYPE_IRI), '_language_type')

    def lookup_entities (self, query, entity_type=None):
        names = query.split()
        queries = []
        for name in names:
            query = self._create_lookup_query(str(name))
            queries.append(query)
        sets = []
        for query in queries:
            if entity_type:
                results = Entity.objects.filter_by_entity_type(entity_type)
            else:
                results = Entity.objects.all()
            sets.append(set(results.filter(query)))
        if len(sets) == 0:
            intersected_set = set()
        else:
            intersected_set = sets[0]
        for i in range(1, len(sets)):
            intersected_set = intersected_set.intersection(sets[i])
        # QAZ: Is there any reason to return a list rather than a set?
        return list(intersected_set)

    def _create_lookup_query (self, name):
        query = None
        name_forms = create_name_forms(str(name))
        for name_form in name_forms:
            if query is None:
                query = Q(indexed_names__form__istartswith=name_form)
            else:
                query = query | Q(indexed_names__form__istartswith=name_form)
        return query

    @property
    def name_assertion_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NAME_ASSERTION_TYPE_IRI), '_name_assertion_type')

    @property
    def name_has_name_part_association_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(NAME_HAS_NAME_PART_ASSOCIATION_TYPE_IRI),
            '_name_has_name_part_association_type')

    @property
    def name_part_order_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NAME_PART_ORDER_TYPE_IRI), '_name_part_order_type')

    @property
    def name_part_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NAME_PART_ROLE_TYPE_IRI), '_name_part_role_type')

    @property
    def name_part_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NAME_PART_TYPE_IRI), '_name_part_type')

    @property
    def name_part_type_order_in_language_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(NAME_PART_TYPE_ORDER_IN_LANGUAGE_TYPE_IRI),
            '_name_part_type_order_in_language_type')

    @property
    def name_part_type_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NAME_PART_TYPE_TYPE_IRI), '_name_part_type_type')

    @property
    def name_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NAME_ROLE_TYPE_IRI), '_name_role_type')

    @property
    def name_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NAME_TYPE_IRI), '_name_type')

    @property
    def name_type_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NAME_TYPE_TYPE_IRI), '_name_type_type')

    @property
    def normalised_date_form_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NORMALISED_DATE_FORM_TYPE_IRI), '_normalised_date_form_type')

    @property
    def note_assertion_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                NOTE_ASSERTION_TYPE_IRI), '_note_assertion_type')

    @property
    def point_date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                POINT_DATE_TYPE_IRI), '_point_date_type')

    @property
    def point_taq_date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                POINT_TAQ_DATE_TYPE_IRI), '_point_taq_date_type')

    @property
    def point_tpq_date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                POINT_TPQ_DATE_TYPE_IRI), '_point_tpq_date_type')

    @property
    def property_assertion_certainty_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(PROPERTY_ASSERTION_CERTAINTY_TYPE_IRI),
            '_property_assertion_certainty_type')

    @property
    def property_assertion_full_certainty (self):
        if not hasattr(self, '_property_assertion_full_certainty'):
            self._property_assertion_full_certainty = \
                self.create_topic_by_subject_identifier(
                Locator(PROPERTY_ASSERTION_FULL_CERTAINTY_IRI))
            self._property_assertion_full_certainty.add_type(
                self.property_assertion_certainty_type)
        return self._property_assertion_full_certainty

    @property
    def property_assertion_no_certainty (self):
        if not hasattr(self, '_property_assertion_no_certainty'):
            self._property_assertion_no_certainty = \
                self.create_topic_by_subject_identifier(
                Locator(PROPERTY_ASSERTION_NO_CERTAINTY_IRI))
            self._property_assertion_no_certainty.add_type(
                self.property_assertion_certainty_type)
        return self._property_assertion_no_certainty

    @property
    def property_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                PROPERTY_ROLE_TYPE_IRI), '_property_role_type')

    @property
    def range_entity_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                RANGE_ENTITY_ROLE_TYPE_IRI), '_range_entity_role_type')

    @property
    def relationship_name_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                RELATIONSHIP_NAME_TYPE_IRI), '_relationship_name_type')

    @property
    def reverse_relationship_name_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(REVERSE_RELATIONSHIP_NAME_TYPE_IRI),
            '_reverse_relationship_name_type')

    @property
    def script_code_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                SCRIPT_CODE_TYPE_IRI), '_script_code_type')

    @property
    def script_separator_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                SCRIPT_SEPARATOR_TYPE_IRI), '_script_separator_type')

    @property
    def script_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                SCRIPT_TYPE_IRI), '_script_type')

    @property
    def script_role_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                SCRIPT_ROLE_TYPE_IRI), '_script_role_type')

    @property
    def start_date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                START_DATE_TYPE_IRI), '_start_date_type')

    @property
    def start_taq_date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                START_TAQ_DATE_TYPE_IRI), '_start_taq_date_type')

    @property
    def start_tpq_date_type (self):
        return self.create_topic_by_subject_identifier(Locator(
                START_TPQ_DATE_TYPE_IRI), '_start_tpq_date_type')

    @property
    def subject_identifier_assertion_type (self):
        return self.create_topic_by_subject_identifier(
            Locator(SUBJECT_IDENTIFIER_ASSERTION_TYPE_IRI),
            '_subject_identifier_assertion_type')
