import copy

from lxml import etree

from eats.constants import EATS_NAMESPACE, XML
from eats.lib.eatsml_handler import EATSMLHandler
from eats.models import Authority


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
            'date_period': {},
            'date_type': {},
            'language': {},
            'name_type': {},
            'script': {},
            }

    def import_xml (self, eatsml, user):
        """Imports EATSML document into EATS.

        Returns an XML tree of the original document annotated with
        ids.
        
        :param eatsml: XML of EATSML to import
        :type eatsml: `str`
        :param user: user performing the import
        :type user: `EATSUser`
        :rtype: `ElementTree`

        """
        # QAZ: check the authorities listed in the EATSML against the
        # user's editable authorities - abort the import if the former
        # isn't a subset of the latter. Except in the case of an
        # administrator.
        parser = etree.XMLParser(remove_blank_text=True)
        import_tree = etree.XML(eatsml, parser).getroottree()
        self._validate(import_tree)
        annotated_tree = copy.deepcopy(import_tree)
        self._import_infrastructure(annotated_tree)
        return annotated_tree

    def _import_infrastructure (self, tree):
        """Imports the infrastructural elements from XML `tree`.

        :param tree: XML tree of EATSML to import
        :type tree: `ElementTree`

        """
        self._import_date_periods(tree)
        self._import_date_types(tree)
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
            else:
                authority = Authority.objects.get_by_identifier(eats_id)
            self._add_mapping('authority', xml_id, authority)
            date_period_elements = authority_element.xpath(
                'e:date_periods/e:date_period', namespaces=NSMAP)
            self._import_authority_infrastructure(
                authority.set_date_periods, 'date_period', date_period_elements)
            date_type_elements = authority_element.xpath(
                'e:date_types/e:date_type', namespaces=NSMAP)
            self._import_authority_infrastructure(
                authority.set_date_types, 'date_type', date_type_elements)
            language_elements = authority_element.xpath(
                'e:languages/e:language', namespaces=NSMAP)
            self._import_authority_infrastructure(
                authority.set_languages, 'language', language_elements)
            name_type_elements = authority_element.xpath(
                'e:name_types/e:name_type', namespaces=NSMAP)
            self._import_authority_infrastructure(
                authority.set_name_types, 'name_type', name_type_elements)
            script_elements = authority_element.xpath(
                'e:scripts/e:script', namespaces=NSMAP)
            self._import_authority_infrastructure(
                authority.set_scripts, 'script', script_elements)

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
        for element  in elements:
            xml_id = element.get('ref')
            obj = self._xml_object_map[object_type][xml_id]
            objects.append(obj)
        if objects:
            setter(objects)

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
            self._add_mapping('date_type', xml_id, date_type)

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
            self._add_mapping('language', xml_id, language)

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
            self._add_mapping('script', xml_id, script)

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
            text = result[0].text.strip()
        else:
            text = ''
        return text
