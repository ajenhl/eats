from tmapi.models import Topic

from eats.exceptions import EATSValidationException

from .infrastructure_manager import InfrastructureManager
from .calendar import Calendar
from .date_period import DatePeriod
from .date_type import DateType
from .entity_relationship_type import EntityRelationshipType
from .entity_type import EntityType
from .infrastructure import Infrastructure
from .language import Language
from .name_part_type import NamePartType
from .name_type import NameType
from .script import Script


class AuthorityManager (InfrastructureManager):

    def get_queryset (self):
        return super(AuthorityManager, self).get_queryset().filter(
            types=self.eats_topic_map.authority_type)


class Authority (Topic, Infrastructure):

    objects = AuthorityManager()

    class Meta:
        proxy = True
        app_label = 'eats'
        verbose_name_plural = 'authorities'

    def get_calendars (self):
        """Return the calendars available to this authority.

        :rtype: `QuerySet` of `Calendar`s

        """
        return Calendar.objects.filter_by_authority(self)

    def get_date_periods (self):
        return DatePeriod.objects.filter_by_authority(self)

    def get_date_types (self):
        return DateType.objects.filter_by_authority(self)

    def get_editors (self):
        """Returns a `QuerySet` of `EATSUser`s who are designated
        editors for this authority.

        :rtype: `QuerySet` of `EATSUser`s

        """
        return self.editors.all()

    def get_entity_types (self):
        return EntityType.objects.filter_by_authority(self)

    def get_entity_relationship_types (self):
        return EntityRelationshipType.objects.filter_by_authority(self)

    def get_languages (self):
        return Language.objects.filter_by_authority(self)

    def get_name_part_types (self):
        return NamePartType.objects.filter_by_authority(self)

    def get_name_types (self):
        return NameType.objects.filter_by_authority(self)

    def get_scripts (self):
        return Script.objects.filter_by_authority(self)

    def set_calendars (self, calendars):
        """Sets the calendars available to this authority to `calendars`.

        :param calendars: calendars to make available
        :type calendars: list of `Calendar`s

        """
        association_type = self.eats_topic_map.authority_has_calendar_association_type
        self._set_infrastructure_elements(
            self.get_calendars(), calendars, association_type, 'calendar')

    def set_date_periods (self, date_periods):
        """Sets the date periods available to this authority to
        `date_periods`.

        :param date_periods: date periods to make available
        :type date_periods: list of `DatePeriod`s

        """
        association_type = self.eats_topic_map.authority_has_date_period_association_type
        self._set_infrastructure_elements(
            self.get_date_periods(), date_periods, association_type,
            'date_period')

    def set_date_types (self, date_types):
        """Sets the date types available to this authority to
        `date_types`.

        :param date_types: date types to make available
        :type date_types: list of `DateType`s

        """
        association_type = self.eats_topic_map.authority_has_date_type_association_type
        self._set_infrastructure_elements(
            self.get_date_types(), date_types, association_type, 'date_type')

    def set_editors (self, editors):
        self.editors = editors

    def set_entity_relationship_types (self, entity_relationship_types):
        """Sets the entity relationship types available to this
        authority to `entity_relationship_types`.

        :param entity_relationship_types: entity relationship types to
          make available
        :type entity_relationship_types: list of `EntityRelationshipType`s

        """
        association_type = self.eats_topic_map.authority_has_entity_relationship_type_association_type
        self._set_infrastructure_elements(
            self.get_entity_relationship_types(), entity_relationship_types,
            association_type, 'entity_relationship_type')

    def set_entity_types (self, entity_types):
        """Sets the entity types available to this authority to
        `entity_types`.

        :param entity_types: entity types to make available
        :type entity_types: list of `EntityType`s

        """
        association_type = self.eats_topic_map.authority_has_entity_type_association_type
        self._set_infrastructure_elements(
            self.get_entity_types(), entity_types, association_type,
            'entity_type')

    def set_languages (self, languages):
        """Sets the languages available to this authority to `languages`.

        :param languages: languages to make available
        :type languages: list of `Language`s

        """
        association_type = self.eats_topic_map.authority_has_language_association_type
        self._set_infrastructure_elements(
            self.get_languages(), languages, association_type, 'language')

    def set_name_part_types (self, name_part_types):
        """Sets the name part types available to this authority to
        `name_part_types`.

        :param name_part_types: name part types to make available
        :type name_part_types: list of `NamePartType`s

        """
        association_type = self.eats_topic_map.authority_has_name_part_type_association_type
        self._set_infrastructure_elements(
            self.get_name_part_types(), name_part_types, association_type,
            'name_part_type')

    def set_name_types (self, name_types):
        """Sets the name types available to this authority to `name_types`.

        :param name_types: name types to make available
        :type name_types: list of `NameType`s

        """
        association_type = self.eats_topic_map.authority_has_name_type_association_type
        self._set_infrastructure_elements(
            self.get_name_types(), name_types, association_type, 'name_type')


    def set_scripts (self, scripts):
        """Sets the scripts available to this authority to `scripts`.

        :param scripts: scripts to make available
        :type scripts: list of `Script`s

        """
        association_type = self.eats_topic_map.authority_has_script_association_type
        self._set_infrastructure_elements(
            self.get_scripts(), scripts, association_type, 'script')

    def _set_infrastructure_elements (self, old_elements, new_elements,
                                      association_type, element_name):
        """Sets the infrastructure elements available to this authority.

        :param old_elements: infrastructure elements currently available
        :param old_elements: list of `Topic`s
        :param new_elements: infrastructure elements to make available
        :type new_elements: list of `Topic`s
        :param association_type: type of association
        :type association_type: `Topic`
        :param element_name: name of the element type
        :type model: `str`

        """
        authority_role_type = self.eats_topic_map.authority_role_type
        infrastructure_role_type = self.eats_topic_map.infrastructure_role_type
        roles = self.get_roles_played(authority_role_type, association_type)
        if not roles:
            # Create the association.
            association = self.eats_topic_map.create_association(
                association_type)
            association.create_role(authority_role_type, self)
        else:
            association = roles[0].get_parent()
            # Validate that no element is being removed that is
            # associated with a property assertion asserted by this
            # authority.
            self._validate_element_removal(element_name, old_elements,
                                           new_elements)
        infrastructure_roles = association.get_roles(infrastructure_role_type)
        for role in infrastructure_roles:
            role.remove()
        for element in new_elements:
            association.create_role(infrastructure_role_type, element)

    def validate_components (self, calendar=None, date_period=None,
                             date_type=None, entity_relationship_type=None,
                             entity_type=None, language=None,
                             name_part_type=None, name_type=None, script=None):
        if calendar and calendar not in self.get_calendars():
            raise EATSValidationException
        if date_period and date_period not in self.get_date_periods():
            raise EATSValidationException
        if date_type and date_type not in self.get_date_types():
            raise EATSValidationException
        if entity_relationship_type and entity_relationship_type \
                not in self.get_entity_relationship_types():
            raise EATSValidationException
        if entity_type and entity_type not in self.get_entity_types():
            raise EATSValidationException
        if language and language not in self.get_languages():
            raise EATSValidationException
        if name_part_type and name_part_type not in self.get_name_part_types():
            raise EATSValidationException
        if name_type and name_type not in self.get_name_types():
            raise EATSValidationException
        if script and script not in self.get_scripts():
            raise EATSValidationException

    def _validate_element_removal (self, element_name, old_elements,
                                   new_elements):
        """Raises an EATSValidationException if an element of
        old_elements is not in new_elements and is associated with a
        property assertion asserted by this authority.

        """
        removed = set(old_elements) - set(new_elements)
        if removed:
            method_name = '_validate_element_removal_' + element_name
            validate = getattr(self, method_name)
            for element in removed:
                if validate(element):
                    raise EATSValidationException

    def _validate_element_removal_calendar (self, element):
        from eats.models import Date
        return Date.objects.filter_by_authority_calendar(self, element).count()

    def _validate_element_removal_date_period (self, element):
        from eats.models import Date
        return Date.objects.filter_by_authority_date_period(
            self, element).count()

    def _validate_element_removal_date_type (self, element):
        from eats.models import Date
        return Date.objects.filter_by_authority_date_type(
            self, element).count()

    def _validate_element_removal_entity_relationship_type (self, element):
        from eats.models import EntityRelationshipPropertyAssertion
        return EntityRelationshipPropertyAssertion.objects.filter_by_authority_entity_relationship_type(self, element).count()

    def _validate_element_removal_entity_type (self, element):
        from eats.models import EntityTypePropertyAssertion
        return EntityTypePropertyAssertion.objects.filter_by_authority_entity_type(self, element).count()

    def _validate_element_removal_language (self, element):
        from eats.models import NamePropertyAssertion
        return NamePropertyAssertion.objects.filter_by_authority_language(
            self, element).count()

    def _validate_element_removal_name_part_type (self, element):
        from eats.models import NamePropertyAssertion
        return NamePropertyAssertion.objects.filter_by_authority_name_part_type(
            self, element).count()

    def _validate_element_removal_name_type (self, element):
        from eats.models import NamePropertyAssertion
        return NamePropertyAssertion.objects.filter_by_authority_name_type(
            self, element).count()

    def _validate_element_removal_script (self, element):
        from eats.models import NamePropertyAssertion
        return NamePropertyAssertion.objects.filter_by_authority_script(
            self, element).count()
