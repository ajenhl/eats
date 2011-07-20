from tmapi.models import Topic

from eats.exceptions import EATSValidationException

from infrastructure_manager import InfrastructureManager
from calendar import Calendar
from date_period import DatePeriod
from date_type import DateType
from entity_relationship_type import EntityRelationshipType
from entity_type import EntityType
from infrastructure import Infrastructure
from language import Language
from name_type import NameType
from script import Script


class AuthorityManager (InfrastructureManager):

    def get_query_set (self):
        return super(AuthorityManager, self).get_query_set().filter(
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

    def get_entity_types (self):
        return EntityType.objects.filter_by_authority(self)

    def get_entity_relationship_types (self):
        return EntityRelationshipType.objects.filter_by_authority(self)

    def get_languages (self):
        return Language.objects.filter_by_authority(self)

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
        self._set_infrastructure_elements(calendars, association_type)

    def set_date_periods (self, date_periods):
        """Sets the date periods available to this authority to
        `date_periods`.

        :param date_periods: date periods to make available
        :type date_periods: list of `DatePeriod`s

        """
        association_type = self.eats_topic_map.authority_has_date_period_association_type
        self._set_infrastructure_elements(date_periods, association_type)

    def set_date_types (self, date_types):
        """Sets the date types available to this authority to
        `date_types`.

        :param date_types: date types to make available
        :type date_types: list of `DateType`s

        """
        association_type = self.eats_topic_map.authority_has_date_type_association_type
        self._set_infrastructure_elements(date_types, association_type)
        
    def set_entity_relationship_types (self, entity_relationship_types):
        """Sets the entity relationship types available to this
        authority to `entity_relationship_types`.

        :param entity_relationship_types: entity relationship types to
          make available
        :type entity_relationship_types: list of `EntityRelationshipType`s

        """
        association_type = self.eats_topic_map.authority_has_entity_relationship_type_association_type
        self._set_infrastructure_elements(entity_relationship_types,
                                          association_type)
        
    def set_entity_types (self, entity_types):
        """Sets the entity types available to this authority to
        `entity_types`.

        :param entity_types: entity types to make available
        :type entity_types: list of `EntityType`s

        """
        association_type = self.eats_topic_map.authority_has_entity_type_association_type
        self._set_infrastructure_elements(entity_types, association_type)

    def set_languages (self, languages):
        """Sets the languages available to this authority to `languages`.

        :param languages: languages to make available
        :type languages: list of `Language`s

        """
        association_type = self.eats_topic_map.authority_has_language_association_type
        self._set_infrastructure_elements(languages, association_type)

    def set_name_types (self, name_types):
        """Sets the name types available to this authority to `name_types`.

        :param name_types: name types to make available
        :type name_types: list of `NameType`s

        """
        association_type = self.eats_topic_map.authority_has_name_type_association_type
        self._set_infrastructure_elements(name_types, association_type)


    def set_scripts (self, scripts):
        """Sets the scripts available to this authority to `scripts`.

        :param scripts: scripts to make available
        :type scripts: list of `Script`s

        """
        association_type = self.eats_topic_map.authority_has_script_association_type
        self._set_infrastructure_elements(scripts, association_type)
        
    def _set_infrastructure_elements (self, elements, association_type):
        """Sets the infrastructure elements available to this authority.

        :param elements: infrastructure elements to make available
        :type elements: list of `Topic`s
        :param association_type: type of association
        :type association_type: `Topic`

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
        infrastructure_roles = association.get_roles(infrastructure_role_type)
        for role in infrastructure_roles:
            role.remove()
        for element in elements:
            association.create_role(infrastructure_role_type, element)

    def validate_components (self, calendar=None, date_period=None,
                             date_type=None, entity_relationship_type=None,
                             entity_type=None, language=None, name_type=None,
                             script=None):
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
        if name_type and name_type not in self.get_name_types():
            raise EATSValidationException
        if script and script not in self.get_scripts():
            raise EATSValidationException
