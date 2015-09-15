import copy

from lxml import etree

from eats.constants import EATS_NAMESPACE, XML
from eats.exceptions import EATSMLException
from eats.lib.eatsml_handler import EATSMLHandler
from eats.models import Authority, Calendar, DatePeriod, DateType, Entity, EntityRelationshipType, EntityType, Language, NamePartType, NameType, Script


NSMAP = {'e': EATS_NAMESPACE}


class EATSMLImporter (EATSMLHandler):

    """An importer of EATSML documents into the EATS system.

    Importing EATSML allows only for adding material to an EATS topic
    map, not deleting or modifying existing material. Subject to the
    permissions of the user performing the import, the following may
    be created:

       * infrastructure elements (authorities, languages, calendars,
         etc)
       * entities
       * property assertions (for both new and existing entities)
       * dates (for new property assertions only)

    Entity relationship property assertions, because they are
    bi-directional, are handled specially. A new assertion will be
    created only when the domain_entity attribute references the
    entity ancestor's XML ID, preventing the same relationship being
    created twice.

    Associations between infrastructural elements (the scripts
    associated with an authority, for example, or the name parts
    associated with a language) are only imported if the containing
    element is new (ie, has no eats_id); otherwise, the XML is
    ignored.

    Since an import may create database objects before encountering a
    fatal error (for example, an attempt to create an infrastructure
    object with the same name as an existing object), an import must
    be run within a single transaction.

    """

    def __init__ (self, topic_map):
        super(EATSMLImporter, self).__init__(topic_map)
        # A mapping between an XML ID and an object, broken down by
        # type of object. Even though the XML IDs are guaranteed to be
        # unique, the RNG schema cannot enforce that, for example,
        # "<language ref='language-1'>" is a reference to a language
        # element and not an entity_type element.
        self._xml_object_map = {
            'authority': {},
            'calendar': {},
            'date_period': {},
            'date_type': {},
            'entity': {},
            'entity_relationship_type': {},
            'entity_type': {},
            'language': {},
            'name_part_type': {},
            'name_type': {},
            'script': {},
            }

    def import_xml (self, eatsml, user):
        """Imports EATSML document into EATS.

        Returns a tuple of two XML trees, the original document and
        the original document annotated with ids.

        :param eatsml: XML of EATSML to import
        :type eatsml: `str`
        :param user: user performing the import
        :type user: `EATSUser`
        :rtype: tuple of `ElementTree`

        """
        # QAZ: check the authorities listed in the EATSML against the
        # user's editable authorities - abort the import if the former
        # isn't a subset of the latter. Except in the case of an
        # administrator.
        parser = etree.XMLParser(remove_blank_text=True)
        try:
            import_tree = etree.XML(eatsml, parser).getroottree()
        except etree.XMLSyntaxError as e:
            message = 'EATSML is not well-formed: %s' % str(e)
            raise EATSMLException(message)
        self._validate(import_tree)
        import_tree = self._prune_eatsml(import_tree)
        annotated_tree = copy.deepcopy(import_tree)
        self._import_infrastructure(annotated_tree)
        self._import_entities(annotated_tree)
        return (import_tree, annotated_tree)

    def _import_infrastructure (self, tree):
        """Imports the infrastructural elements from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        self._import_calendars(tree)
        self._import_date_periods(tree)
        self._import_date_types(tree)
        self._import_entity_relationship_types(tree)
        self._import_entity_types(tree)
        # Name part types may be referenced by languages, so import
        # before them.
        self._import_name_part_types(tree)
        self._import_languages(tree)
        self._import_name_types(tree)
        self._import_scripts(tree)
        # Authorities may contain references to other infrastructural
        # elements, so import after them.
        self._import_authorities(tree)

    def _import_authorities (self, tree):
        """Imports authorities from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        authority_elements = tree.xpath(
            '/e:collection/e:authorities/e:authority', namespaces=NSMAP)
        for authority_element in authority_elements:
            xml_id = authority_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(authority_element)
            if eats_id is None:
                name = self._get_text(authority_element, 'e:name')
                authority = self._topic_map.create_authority(name)
                eats_id = authority.get_id()
                authority_element.set('eats_id', str(eats_id))
                calendar_elements = authority_element.xpath(
                    'e:calendars/e:calendar', namespaces=NSMAP)
                self._import_authority_infrastructure(
                    authority.set_calendars, 'calendar', calendar_elements)
                date_period_elements = authority_element.xpath(
                    'e:date_periods/e:date_period', namespaces=NSMAP)
                self._import_authority_infrastructure(
                    authority.set_date_periods, 'date_period',
                    date_period_elements)
                date_type_elements = authority_element.xpath(
                    'e:date_types/e:date_type', namespaces=NSMAP)
                self._import_authority_infrastructure(
                    authority.set_date_types, 'date_type', date_type_elements)
                entity_relationship_type_elements = authority_element.xpath(
                    'e:entity_relationship_types/e:entity_relationship_type',
                    namespaces=NSMAP)
                self._import_authority_infrastructure(
                    authority.set_entity_relationship_types,
                    'entity_relationship_type',
                    entity_relationship_type_elements)
                entity_type_elements = authority_element.xpath(
                    'e:entity_types/e:entity_type', namespaces=NSMAP)
                self._import_authority_infrastructure(
                    authority.set_entity_types, 'entity_type',
                    entity_type_elements)
                language_elements = authority_element.xpath(
                    'e:languages/e:language', namespaces=NSMAP)
                self._import_authority_infrastructure(
                    authority.set_languages, 'language', language_elements)
                name_part_type_elements = authority_element.xpath(
                    'e:name_part_types/e:name_part_type', namespaces=NSMAP)
                self._import_authority_infrastructure(
                    authority.set_name_part_types, 'name_part_type',
                    name_part_type_elements)
                name_type_elements = authority_element.xpath(
                    'e:name_types/e:name_type', namespaces=NSMAP)
                self._import_authority_infrastructure(
                    authority.set_name_types, 'name_type', name_type_elements)
                script_elements = authority_element.xpath(
                    'e:scripts/e:script', namespaces=NSMAP)
                self._import_authority_infrastructure(
                    authority.set_scripts, 'script', script_elements)
            else:
                authority = self._get_by_identifier(Authority, eats_id)
            self._add_mapping('authority', xml_id, authority)

    def _import_authority_infrastructure (self, setter, object_type,
                                          elements):
        """Imports `elements` as infrastructural elements associated
        with an authority, using `setter`.

        :param setter: method to associate objects with authority
        :type authority: `instancemethod`
        :param object_type: name of the object type, being the key to
          self._xml_object_map
        :type object_type: `str`
        :param elements: XML elements to be imported
        :type elements: `list` of `Element`\s

        """
        # QAZ: If there are existing elements set for this authority,
        # then having elements specified in the EATSML should raise an
        # error.
        objects = []
        for element in elements:
            xml_id = element.get('ref')
            obj = self._xml_object_map[object_type][xml_id]
            objects.append(obj)
        if objects:
            setter(objects)

    def _import_calendars (self, tree):
        """Imports calendars from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        calendar_elements = tree.xpath(
            '/e:collection/e:calendars/e:calendar', namespaces=NSMAP)
        for calendar_element in calendar_elements:
            xml_id = calendar_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(calendar_element)
            if eats_id is None:
                name = calendar_element[0].text
                calendar = self._topic_map.create_calendar(name)
                eats_id = calendar.get_id()
                calendar_element.set('eats_id', str(eats_id))
            else:
                calendar = self._get_by_identifier(Calendar, eats_id)
            self._add_mapping('calendar', xml_id, calendar)

    def _import_date_periods (self, tree):
        """Imports date periods from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        date_period_elements = tree.xpath(
            '/e:collection/e:date_periods/e:date_period', namespaces=NSMAP)
        for date_period_element in date_period_elements:
            xml_id = date_period_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(date_period_element)
            if eats_id is None:
                name = date_period_element[0].text
                date_period = self._topic_map.create_date_period(name)
                eats_id = date_period.get_id()
                date_period_element.set('eats_id', str(eats_id))
            else:
                date_period = self._get_by_identifier(DatePeriod, eats_id)
            self._add_mapping('date_period', xml_id, date_period)

    def _import_date_types (self, tree):
        """Imports date types from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        date_type_elements = tree.xpath(
            '/e:collection/e:date_types/e:date_type', namespaces=NSMAP)
        for date_type_element in date_type_elements:
            xml_id = date_type_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(date_type_element)
            if eats_id is None:
                name = date_type_element[0].text
                date_type = self._topic_map.create_date_type(name)
                eats_id = date_type.get_id()
                date_type_element.set('eats_id', str(eats_id))
            else:
                date_type = self._get_by_identifier(DateType, eats_id)
            self._add_mapping('date_type', xml_id, date_type)

    def _import_entity_relationship_types (self, tree):
        """Imports entity relationship types from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        elements = tree.xpath(
            '/e:collection/e:entity_relationship_types/e:entity_relationship_type', namespaces=NSMAP)
        for element in elements:
            xml_id = element.get(XML + 'id')
            eats_id = self._get_element_eats_id(element)
            if eats_id is None:
                name = element[0].text
                reverse_name = element[1].text
                entity_relationship_type = self._topic_map.create_entity_relationship_type(name, reverse_name)
                eats_id = entity_relationship_type.get_id()
                element.set('eats_id', str(eats_id))
            else:
                entity_relationship_type = self._get_by_identifier(
                    EntityRelationshipType, eats_id)
            self._add_mapping('entity_relationship_type', xml_id,
                              entity_relationship_type)

    def _import_entity_types (self, tree):
        """Imports entity types from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        entity_type_elements = tree.xpath(
            '/e:collection/e:entity_types/e:entity_type', namespaces=NSMAP)
        for entity_type_element in entity_type_elements:
            xml_id = entity_type_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(entity_type_element)
            if eats_id is None:
                name = entity_type_element[0].text
                entity_type = self._topic_map.create_entity_type(name)
                eats_id = entity_type.get_id()
                entity_type_element.set('eats_id', str(eats_id))
            else:
                entity_type = self._get_by_identifier(EntityType, eats_id)
            self._add_mapping('entity_type', xml_id, entity_type)

    def _import_languages (self, tree):
        """Imports languages from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        language_elements = tree.xpath(
            '/e:collection/e:languages/e:language', namespaces=NSMAP)
        for language_element in language_elements:
            xml_id = language_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(language_element)
            if eats_id is None:
                name = language_element[0].text
                code = language_element[1].text
                language = self._topic_map.create_language(name, code)
                eats_id = language.get_id()
                language_element.set('eats_id', str(eats_id))
                name_part_types = []
                for name_part_type_element in language_element.xpath(
                    'e:name_part_types/e:name_part_type', namespaces=NSMAP):
                    name_part_type_xml_id = name_part_type_element.get('ref')
                    name_part_type = self._xml_object_map['name_part_type'][
                        name_part_type_xml_id]
                    name_part_types.append(name_part_type)
                if name_part_types:
                    language.name_part_types = name_part_types
            else:
                language = self._get_by_identifier(Language, eats_id)
            self._add_mapping('language', xml_id, language)

    def _import_name_part_types (self, tree):
        """Imports name part types from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        name_part_type_elements = tree.xpath(
            '/e:collection/e:name_part_types/e:name_part_type',
            namespaces=NSMAP)
        for name_part_type_element in name_part_type_elements:
            xml_id = name_part_type_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(name_part_type_element)
            if eats_id is None:
                name = name_part_type_element[0].text
                name_part_type = self._topic_map.create_name_part_type(name)
                eats_id = name_part_type.get_id()
                name_part_type_element.set('eats_id', str(eats_id))
            else:
                name_part_type = self._get_by_identifier(NamePartType, eats_id)
            self._add_mapping('name_part_type', xml_id, name_part_type)

    def _import_name_types (self, tree):
        """Imports name types from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        name_type_elements = tree.xpath(
            '/e:collection/e:name_types/e:name_type', namespaces=NSMAP)
        for name_type_element in name_type_elements:
            xml_id = name_type_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(name_type_element)
            if eats_id is None:
                name = name_type_element[0].text
                name_type = self._topic_map.create_name_type(name)
                eats_id = name_type.get_id()
                name_type_element.set('eats_id', str(eats_id))
            else:
                name_type = self._get_by_identifier(NameType, eats_id)
            self._add_mapping('name_type', xml_id, name_type)

    def _import_scripts (self, tree):
        """Imports scripts from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        script_elements = tree.xpath(
            '/e:collection/e:scripts/e:script', namespaces=NSMAP)
        for script_element in script_elements:
            xml_id = script_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(script_element)
            if eats_id is None:
                name = script_element[0].text
                code = script_element[1].text
                separator = script_element[2].text
                script = self._topic_map.create_script(name, code, separator)
                eats_id = script.get_id()
                script_element.set('eats_id', str(eats_id))
            else:
                script = self._get_by_identifier(Script, eats_id)
            self._add_mapping('script', xml_id, script)

    def _import_entities (self, tree):
        """Imports entities from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        entity_elements = tree.xpath('/e:collection/e:entities/e:entity',
                                     namespaces=NSMAP)
        for entity_element in entity_elements:
            xml_id = entity_element.get(XML + 'id')
            eats_id = self._get_element_eats_id(entity_element)
            if eats_id is None:
                entity = self._topic_map.create_entity()
                entity_element.set('eats_id', str(entity.get_id()))
                url = entity.get_eats_subject_identifier().to_external_form()
                entity_element.set('url', url)
            else:
                entity = self._get_by_identifier(Entity, eats_id)
            self._add_mapping('entity', xml_id, entity)
            self._import_entity_type_assertions(entity, entity_element)
            self._import_existence_assertions(entity, entity_element)
            self._import_name_assertions(entity, entity_element)
            self._import_note_assertions(entity, entity_element)
            self._import_subject_identifier_assertions(entity, entity_element)
        self._import_entity_relationship_assertions(tree)

    def _import_entity_type_assertions (self, entity, entity_element):
        """Imports entity type assertions from `entity_element` into
        `entity`.

        :param entity: entity to import into
        :type entity: `Entity`
        :param entity_element: XML element representing `entity`
        :type entity_element: `Element`

        """
        elements = entity_element.xpath('e:entity_types/e:entity_type',
                                        namespaces=NSMAP)
        for element in elements:
            eats_id = self._get_element_eats_id(element)
            if eats_id is None:
                authority = self._get_mapped_object(element, 'authority',
                                                    'authority')
                entity_type = self._get_mapped_object(element, 'entity_type',
                                                      'entity_type')
                assertion = entity.create_entity_type_property_assertion(
                    authority, entity_type)
                element.set('eats_id', str(assertion.get_id()))
                self._import_dates(element, assertion)

    def _import_existence_assertions (self, entity, entity_element):
        """Imports existence assertions from `entity_element` into
        `entity`.

        :param entity: entity to import into
        :type entity: `Entity`
        :param entity_element: XML element representing `entity`
        :type entity_element: `Element`

        """
        elements = entity_element.xpath('e:existences/e:existence',
                                        namespaces=NSMAP)
        for element in elements:
            eats_id = self._get_element_eats_id(element)
            if eats_id is None:
                authority = self._get_mapped_object(element, 'authority',
                                                    'authority')
                assertion = entity.create_existence_property_assertion(
                    authority)
                element.set('eats_id', str(assertion.get_id()))
                self._import_dates(element, assertion)

    def _import_name_assertions (self, entity, entity_element):
        """Imports name assertions from `entity_element` into
        `entity`.

        :param entity: entity to import into
        :type entity: `Entity`
        :param entity_element: XML element representing `entity`
        :type entity_element: `Element`

        """
        elements = entity_element.xpath('e:names/e:name', namespaces=NSMAP)
        for element in elements:
            eats_id = self._get_element_eats_id(element)
            if eats_id is None:
                authority = self._get_mapped_object(element, 'authority',
                                                    'authority')
                is_preferred = self._get_boolean(element.get('is_preferred'))
                name_type = self._get_mapped_object(element, 'name_type',
                                                    'name_type')
                language = self._get_mapped_object(element, 'language',
                                                   'language')
                script = self._get_mapped_object(element, 'script', 'script')
                display_form = self._get_text(element, 'e:display_form')
                assertion = entity.create_name_property_assertion(
                    authority, name_type, language, script, display_form,
                    is_preferred)
                element.set('eats_id', str(assertion.get_id()))
                self._import_name_parts(assertion.name, element)
                self._import_dates(element, assertion)

    def _import_name_parts (self, name, name_element):
        """Imports name parts from `name_element` into `name`.

        :param name: name to import into
        :type name: `Name`
        :param name_element: XML element representing `name`
        :type name_element: `Element`

        """
        for element in name_element.xpath('e:name_parts/e:name_part',
                                          namespaces=NSMAP):
            name_part_type = self._get_mapped_object(element, 'name_part_type',
                                                     'name_part_type')
            language = self._get_mapped_object(element, 'language', 'language')
            script = self._get_mapped_object(element, 'script', 'script')
            display_form = self._get_text(element, '.')
            order = element.xpath('count(preceding-sibling::e:name_part[@name_part_type="%s"])+1' % name_part_type, namespaces=NSMAP)
            name.create_name_part(name_part_type, language, script,
                                  display_form, order)

    def _import_note_assertions (self, entity, entity_element):
        """Imports note assertions from `entity_element` into
        `entity`.

        :param entity: entity to import into
        :type entity: `Entity`
        :param entity_element: XML element representing `entity`
        :type entity_element: `Element`

        """
        elements = entity_element.xpath('e:notes/e:note', namespaces=NSMAP)
        for element in elements:
            eats_id = self._get_element_eats_id(element)
            if eats_id is None:
                authority = self._get_mapped_object(element, 'authority',
                                                    'authority')
                note = self._get_text(element, '.')
                assertion = entity.create_note_property_assertion(
                    authority, note)
                element.set('eats_id', str(assertion.get_id()))

    def _import_subject_identifier_assertions (self, entity, entity_element):
        """Imports subject identifier assertions from `entity_element`
        into `entity`.

        :param entity: entity to import into
        :type entity: `Entity`
        :param entity_element: XML element representing `entity`
        :type entity_element: `Element`

        """
        elements = entity_element.xpath(
            'e:subject_identifiers/e:subject_identifier', namespaces=NSMAP)
        for element in elements:
            eats_id = self._get_element_eats_id(element)
            if eats_id is None:
                authority = self._get_mapped_object(element, 'authority',
                                                    'authority')
                subject_identifier = self._get_text(element, '.')
                assertion = entity.create_subject_identifier_property_assertion(
                    authority, subject_identifier)
                element.set('eats_id', str(assertion.get_id()))

    def _import_entity_relationship_assertions (self, tree):
        """Imports entity relationship assertions.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        elements = tree.xpath(
            '/e:collection/e:entities/e:entity/e:entity_relationships/e:entity_relationship', namespaces=NSMAP)
        for element in elements:
            eats_id = self._get_element_eats_id(element)
            if eats_id is None:
                self._import_entity_relationship_assertion(element)

    def _import_entity_relationship_assertion (self, element):
        """Imports entity relationship assertion from `element`.

        :param element: XML element representing entity relationship assertion
        :type element: `Element`

        """
        entity_element = element.xpath('ancestor::e:entity',
                                       namespaces=NSMAP)[0]
        entity = self._get_mapped_object(entity_element, XML + 'id', 'entity')
        domain_entity = self._get_mapped_object(element, 'domain_entity',
                                                'entity')
        # Only import an entity relationship if the domain
        # entity is the current entity. This prevents the same
        # relationship between imported twice.
        if domain_entity == entity:
            authority = self._get_mapped_object(element, 'authority',
                                                'authority')
            entity_relationship_type = self._get_mapped_object(
                element, 'entity_relationship_type', 'entity_relationship_type')
            range_entity = self._get_mapped_object(element, 'range_entity',
                                                   'entity')
            certainty = self._topic_map.property_assertion_no_certainty
            if element.get('certainty') == 'full':
                certainty = self._topic_map.property_assertion_full_certainty
            assertion = entity.create_entity_relationship_property_assertion(
                authority, entity_relationship_type, domain_entity,
                range_entity, certainty)
            element.set('eats_id', str(assertion.get_id()))
            self._import_dates(element, assertion)

    def _import_dates (self, assertion_element, assertion):
        """Imports any dates associated with `assertion_element`,
        assigning them to `assertion`.

        :param assertion_element: XML element representing a property
          assertion
        :type assertion_element: `Element`
        :param assertion: Django property assertion object
        :type assertion: `Association`

        """
        for date_element in assertion_element.xpath('e:dates/e:date',
                                                    namespaces=NSMAP):
            date_period = self._get_mapped_object(date_element, 'date_period',
                                                  'date_period')
            data = {'date_period': date_period}
            date_part_elements = date_element.xpath('e:date_parts/e:date_part',
                                                    namespaces=NSMAP)
            for element in date_part_elements:
                date_part_type = element.get('type')
                data[date_part_type] = self._get_text(element, 'e:raw')
                data[date_part_type + '_calendar'] = self._get_mapped_object(
                    element, 'calendar', 'calendar')
                certainty = self._topic_map.date_no_certainty
                if element.get('certainty') == 'full':
                    certainty = self._topic_map.date_full_certainty
                data[date_part_type + '_certainty'] = certainty
                data[date_part_type + '_normalised'] = self._get_text(
                    element, 'e:normalised')
                data[date_part_type + '_type'] = self._get_mapped_object(
                    element, 'date_type', 'date_type')
            assertion.create_date(data)

    def _add_mapping (self, object_type, xml_id, obj):
        """Adds a mapping between `xml_id` and `obj` within the
        mapping for `object_type`.

        :param object_type: name of the object type, being the key to
          self._xml_object_map
        :type object_type: `str`
        :param xml_id: XML ID of mapped object
        :type xml_id: `str`
        :param obj: mapped object
        :type obj: `Topic`

        """
        self._xml_object_map[object_type][xml_id] = obj

    def _get_mapped_object (self, element, attribute_name, object_type):
        """Returns the object mapped to `object_type` with the ID
        taken from `attribute_name` on `element`.

        :param element: XML element holding the attribute
        :type element: `Element`
        :param attribute_name: name of the attribute holding the ID
        :type attribute_name: `str`
        :param object_type: name of the type of object to look up
        :type object_type: `str`
        :rtype: `Construct`

        """
        xml_id = element.get(attribute_name)
        return self._xml_object_map[object_type][xml_id]

    @staticmethod
    def _get_by_identifier (model, eats_id):
        try:
            item = model.objects.get_by_identifier(eats_id)
        except model.DoesNotExist:
            message = '%s with EATS ID "%s" does not exist' % \
                (model._meta.verbose_name.title(), eats_id)
            raise EATSMLException(message)
        return item

    @staticmethod
    def _get_element_id (element):
        """Returns the XML ID of `element`.

        :rtype: `str`

        """
        return element.get(XML + 'id')

    @staticmethod
    def _get_element_eats_id (element):
        """Returns the EATS ID of `element`.

        :rtype: `int`

        """
        eats_id = element.get('eats_id')
        if eats_id:
            eats_id = int(eats_id)
        return eats_id

    @staticmethod
    def _get_text (element, xpath):
        """Returns the text of the element result of performing
        `xpath` query on `element`.

        :param element: root element of `xpath` query
        :type element: `Element`
        :param xpath: XPath query
        :type xpath: `str`
        :rtype: `str`

        """
        result = element.xpath(xpath, namespaces=NSMAP)
        if result:
            text = result[0].text or ''
        else:
            text = ''
        return text.strip()

    def _get_boolean (self, value):
        """Returns a Boolean derived from `value`.

        :param value: value to be converted to a Boolean
        :type value: XSD Boolean string
        :rtype: `bool`

        """
        if value == 'true':
            result = True
        else:
            result = False
        return result
