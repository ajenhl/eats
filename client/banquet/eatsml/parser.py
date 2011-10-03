"""Module providing custom element classes and lookup for lxml parsing
of EATSML."""

from lxml import etree

from constants import EATSML, XML, XPATH_NSMAP


_get_assembled_form = etree.XPath('e:assembled_form', namespaces=XPATH_NSMAP)
_get_authorities = etree.XPath('e:authorities/e:authority',
                               namespaces=XPATH_NSMAP)
_get_element_by_id = etree.XPath('id($xml_id)')
_get_entities = etree.XPath('e:entities/e:entity', namespaces=XPATH_NSMAP)
_get_entity_types = etree.XPath('e:entity_types/e:entity_type',
                                namespaces=XPATH_NSMAP)
_get_existence_dates = etree.XPath('e:existences/e:existence/e:dates/e:date',
                                   namespaces=XPATH_NSMAP)
_get_languages = etree.XPath('e:languages/e:language', namespaces=XPATH_NSMAP)
_get_name = etree.XPath('e:name', namespaces=XPATH_NSMAP)
_get_name_part_type = etree.XPath(
    'e:name_part_types/e:name_part_type[e:name=$name]',
    namespaces=XPATH_NSMAP)
_get_name_parts = etree.XPath(
    'e:name_parts/e:name_part[@name_part_type=$name_part_type]',
    namespaces=XPATH_NSMAP)
_get_name_types = etree.XPath('e:name_types/e:name_type',
                              namespaces=XPATH_NSMAP)
_get_names = etree.XPath('e:names/e:name', namespaces=XPATH_NSMAP)
_get_notes = etree.XPath('e:notes/e:note', namespaces=XPATH_NSMAP)
_get_preferred_entity_types = etree.XPath('/e:collection/e:entity_types/e:entity_type[@xml:id=id($current)/e:entity_types/e:entity_type[@authority=$authority]/@entity_type]/e:name/text()',
    namespaces=XPATH_NSMAP)
_get_preferred_name = etree.XPath('e:names/e:name[@user_preferred="true"]',
                                  namespaces=XPATH_NSMAP)
_get_relationships = etree.XPath('e:entity_relationships/e:entity_relationship',
                                 namespaces=XPATH_NSMAP)
_get_reverse_name = etree.XPath('e:reverse_name', namespaces=XPATH_NSMAP)
_get_scripts = etree.XPath('e:scripts/e:script', namespaces=XPATH_NSMAP)
_get_separator = etree.XPath('e:separator/text()', namespaces=XPATH_NSMAP)


class EATSMLElementLookup (etree.PythonElementClassLookup):

    def lookup (self, document, element):
        _class = None
        tag = element.tag
        if tag == EATSML + 'authority':
            _class = Authority
        elif tag == EATSML + 'collection':
            _class = Collection
        elif tag == EATSML + 'date':
            _class = Date
        elif tag == EATSML + 'entity':
            _class = Entity
        elif tag == EATSML + 'entity_relationship':
            _class = EntityRelationship
        elif tag == EATSML + 'entity_relationship_type' and \
                self._is_infrastructure:
            _class = EntityRelationshipType
        elif tag == EATSML + 'entity_type' and self._is_infrastructure(element):
            _class = EntityType
        elif tag == EATSML + 'language' and self._is_infrastructure(element):
            _class = Language
        elif tag == EATSML + 'name' and \
                element.getparent().tag == EATSML + 'names':
            _class = NamePropertyAssertion
        elif tag == EATSML + 'name_part':
            _class = NamePart
        elif tag == EATSML + 'name_type' and self._is_infrastructure(element):
            _class = NameType
        elif tag == EATSML + 'script':
            if element.getparent().getparent().tag == EATSML + 'collection':
                _class = Script
        return _class

    def _is_infrastructure (self, element):
        """Returns True if `element` is an infrastructure element (not
        a descendant of either an authority or an entity element).

        :param element: element to check
        :type element:
        :rtype: `bool`

        """
        return element.getparent().getparent().tag == EATSML + 'collection'


class NameElement (etree.ElementBase):

    """Base class for names and name parts."""

    @property
    def script (self):
        """Returns this name-like element's script.

        :rtype: `Script`

        """
        script_id = self.get('script')
        return self._get_element_by_id(script_id)


class NamedElement (etree.ElementBase):

    """Base class for elements that have a name."""

    @property
    def name (self):
        return _get_name(self)[0].text


class ReferencingElement (etree.ElementBase):

    """Base class for elements that reference other elements."""

    def _get_element_by_id (self, xml_id):
        """Returns the element whose xml:id is `xml_id`.

        :param xml_id: xml:id of element to return
        :type xml_id: `str`
        :rtype: `etree.ElementBase`

        """
        nodeset = _get_element_by_id(self, xml_id=xml_id)
        return nodeset[0]


class UserPreferredElement (etree.ElementBase):

    """Base class for elements that may be a user's preference."""

    @property
    def user_preferred (self):
        """Returns True if this element is preferred by the user.

        :rtype: `bool`

        """
        value = self.get('user_preferred')
        if value == 'true':
            return True
        return False


class PropertyAssertion (ReferencingElement):

    """Base class for property assertion elements."""

    @property
    def authority (self):
        """Returns the `Authority` asserting this property.

        :rtype: `Authority`

        """
        authority_id = self.get('authority')
        return self._get_element_by_id(authority_id)

    @authority.setter
    def authority (self, authority):
        """Sets the authority asserting the property.

        :param authority: authority asserting the property
        :type authority: `Authority`

        """
        authority_id = authority.get(XML + 'id')
        self.set('authority', authority_id)


class Authority (NamedElement, UserPreferredElement):

    def get_entity_types (self):
        """Returns the entity types associated with this authority.

        :rtype: `list` of `EntityType`\s

        """
        entity_type_refs = _get_entity_types(self)
        entity_types = [self._get_referenced_element(entity_type_ref) for
                        entity_type_ref in entity_type_refs]
        return entity_types

    def get_languages (self):
        """Returns the languages associated with this authority.

        :rtype: `list` of `Language`\s

        """
        language_refs = _get_languages(self)
        languages = [self._get_referenced_element(language_ref) for
                     language_ref in language_refs]
        return languages
    
    def get_name_types (self):
        """Returns the name types associated with this authority.

        :rtype: `list` of `NameType`\s

        """
        name_type_refs = _get_name_types(self)
        name_types = [self._get_referenced_element(name_type_ref) for
                      name_type_ref in name_type_refs]
        return name_types

    def get_scripts (self):
        """Returns the scripts associated with this authority.

        :rtype: `list` of `Script`\s

        """
        script_refs = _get_scripts(self)
        scripts = [self._get_referenced_element(script_ref) for script_ref in
                   script_refs]
        return scripts

    def _get_referenced_element (self, referencing_element):
        """Returns the element referenced by `referencing_element`.

        :param referencing_element: element containing reference
        :type referencing_element: `etree.ElementBase`
        :rtype: `etree.ElementBase`

        """
        xml_id = referencing_element.get('ref')
        return _get_element_by_id(self, xml_id=xml_id)[0]


class Collection (etree.ElementBase):

    def get_authorities (self):
        """Returns a list of the authorities in the document.

        :rtype: `list` of `Authority`\s

        """
        return _get_authorities(self)

    def get_entities (self):
        """Returns a list of the entities in the document.

        :rtype: `list` of `Entity`\s

        """
        return _get_entities(self)

    def get_name_part_type (self, name):
        """Returns the name part type element called `name`.

        :param name: name of name part type
        :type name: `str`
        :rtype: `NamePartType`

        """
        return _get_name_part_type(self, name=name)[0]


class Date (etree.ElementBase):

    @property
    def assembled_form (self):
        """Return's this date's assembled form.

        :rtype: `str`

        """
        return _get_assembled_form(self)[0].text


class Entity (etree.ElementBase):

    def get_existence_dates (self):
        return _get_existence_dates(self)

    def get_names (self):
        return _get_names(self)

    def get_notes (self):
        return _get_notes(self)

    def get_preferred_entity_types (self, authority):
        return _get_preferred_entity_types(self, authority=authority,
                                           current=self.get(XML + 'id'))
    
    def get_preferred_name (self):
        return _get_preferred_name(self)[0]

    def get_relationships (self):
        return _get_relationships(self)

    @property
    def url (self):
        """Returns the URL (EATS subject identifier) for this entity.

        :rtype: `str`

        """
        return self.get('url')


class EntityRelationship (ReferencingElement):

    def get_assembled_form (self):
        entity_id = self.getparent().getparent().get(XML + 'id')
        domain_entity_id = self.get('domain_entity')
        relationship_type_id = self.get('entity_relationship_type')
        relationship_type = self._get_element_by_id(relationship_type_id)
        if domain_entity_id == entity_id:
            range_entity_id = self.get('range_entity')
            other_entity = self._get_element_by_id(range_entity_id)
            relationship = relationship_type.name
        else:
            other_entity = self._get_element_by_id(domain_entity_id)
            relationship = relationship_type.reverse_name
        other_entity_name = other_entity.get_preferred_name().assembled_form
        return '%s %s' % (relationship, other_entity_name)


class EntityRelationshipType (NamedElement):
    
    @property
    def reverse_name (self):
        return _get_reverse_name(self)[0].text


class EntityType (NamedElement):

    pass


class Language (NamedElement, UserPreferredElement):

    pass


class NamePropertyAssertion (NameElement, ReferencingElement):

    @property
    def assembled_form (self):
        """Return's this name's assembled form.

        :rtype: `str`

        """
        return _get_assembled_form(self)[0].text
    
    def get_name_part (self, name_part_type):
        """Returns the combined display form of all name parts of
        `name_part_type` in this name.

        :param name_part_type: type of name parts to return the display form of
        :type name_part_type: `NamePartType`
        :rtype: `str`

        """
        name_part_type_id = name_part_type.get(XML + 'id')
        name_parts = _get_name_parts(self, name_part_type=name_part_type_id)
        separator = self.script.separator
        return separator.join([name_part.text for name_part in name_parts])


class NamePart (NameElement):

    pass


class NameType (NamedElement):

    pass


class Script (NamedElement, UserPreferredElement):

    @property
    def separator (self):
        """Returns this script's separator.

        :rtype: `str`

        """
        return _get_separator(self)[0]


parser = etree.XMLParser()
parser.set_element_class_lookup(EATSMLElementLookup())
