"""Module providing custom element classes and lookup for lxml parsing
of EATSML."""

from lxml import etree

from constants import EATSML, XML, XPATH_NSMAP


_get_assembled_form = etree.XPath('e:assembled_form', namespaces=XPATH_NSMAP)
_get_authorities = etree.XPath('e:authorities/e:authority',
                               namespaces=XPATH_NSMAP)
_get_display_form = etree.XPath('e:display_form/text()[1]',
                                namespaces=XPATH_NSMAP)
_get_display_form_element = etree.XPath('e:display_form',
                                        namespaces=XPATH_NSMAP)
_get_element_by_id = etree.XPath('id($xml_id)')
_get_entities = etree.XPath('e:entities/e:entity', namespaces=XPATH_NSMAP)
_get_entity_types = etree.XPath('e:entity_types/e:entity_type',
                                namespaces=XPATH_NSMAP)
_get_entity_types_element = etree.XPath('e:entity_types',
                                        namespaces=XPATH_NSMAP)
_get_existence_dates = etree.XPath('e:existences/e:existence/e:dates/e:date',
                                   namespaces=XPATH_NSMAP)
_get_existences_element = etree.XPath('e:existences', namespaces=XPATH_NSMAP)
_get_languages = etree.XPath('e:languages/e:language', namespaces=XPATH_NSMAP)
_get_name = etree.XPath('e:name', namespaces=XPATH_NSMAP)
_get_name_part_type = etree.XPath(
    'e:name_part_types/e:name_part_type[e:name=$name]',
    namespaces=XPATH_NSMAP)
_get_name_parts = etree.XPath(
    'e:name_parts/e:name_part[@name_part_type=$name_part_type]',
    namespaces=XPATH_NSMAP)
_get_name_parts_element = etree.XPath('e:name_parts', namespaces=XPATH_NSMAP)
_get_name_types = etree.XPath('e:name_types/e:name_type',
                              namespaces=XPATH_NSMAP)
_get_names = etree.XPath('e:names/e:name', namespaces=XPATH_NSMAP)
_get_names_element = etree.XPath('e:names', namespaces=XPATH_NSMAP)
_get_notes = etree.XPath('e:notes/e:note', namespaces=XPATH_NSMAP)
_get_notes_element = etree.XPath('e:notes', namespaces=XPATH_NSMAP)
_get_preferred_entity_types = etree.XPath('/e:collection/e:entity_types/e:entity_type[@xml:id=id($current)/e:entity_types/e:entity_type[@authority=$authority]/@entity_type]',
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
        elif tag == EATSML + 'entity_type':
            if self._is_infrastructure(element):
                _class = EntityType
            else:
                _class = EntityTypePropertyAssertion
        elif tag == EATSML + 'existence':
            _class = ExistencePropertyAssertion
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
        elif tag == EATSML + 'note' and \
                element.getparent().tag == EATSML + 'notes':
            _class = NotePropertyAssertion
        return _class

    def _is_infrastructure (self, element):
        """Returns True if `element` is an infrastructure element (not
        a descendant of either an authority or an entity element).

        :param element: element to check
        :type element:
        :rtype: `bool`

        """
        return element.getparent().getparent().tag == EATSML + 'collection'


class EATSMLElementBase (etree.ElementBase):

    """Base class for all EATSML elements."""

    def _get_element_by_id (self, xml_id):
        """Returns the element whose xml:id is `xml_id`.

        :param xml_id: xml:id of element to return
        :type xml_id: `str`
        :rtype: `etree.ElementBase`

        """
        nodeset = _get_element_by_id(self, xml_id=xml_id)
        return nodeset[0]

    def _get_element_index (self, tag):
        """Returns the index at which to insert a new element named
        `tag`.

        :param tag: name of element to find the index for
        :type tag: `str`
        :rtype: `int`

        """
        full_index = self._indices[tag]
        possible_index = full_index
        count = len(self)
        if count == 0:
            index = 0
        elif full_index == 0:
            index = 0
        else:
            if full_index >= count:
                possible_index = count - 1
            index = get_element_index(self, self._indices, full_index,
                                      possible_index)
        return index

    def _get_or_create_element (self, xpath, tag):
        """Returns the element matching `xpath`, creating it if it
        doesn't already exist.

        :param xpath: XPath function
        :param tag: name of element to be found and/or created
        :type tag: `str`

        """
        nodeset = xpath(self)
        if len(nodeset):
            element = nodeset[0]
        else:
            element = etree.Element(tag)
            index = self._get_element_index(tag)
            self.insert(index, element)
        return element


class NameElement (EATSMLElementBase):

    """Base class for names and name parts."""

    @property
    def language (self):
        """Returns the language of this name.

        :rtype: `Language`

        """
        language_id = self.get('language')
        return self._get_element_by_id(language_id)

    @language.setter
    def language (self, language):
        """Sets the language of this name.

        :param language: language to set
        :type language: `Language`

        """
        language_id = language.get(XML + 'id')
        self.set('language', language_id)

    @property
    def script (self):
        """Returns the script of this name.

        :rtype: `Script`

        """
        script_id = self.get('script')
        return self._get_element_by_id(script_id)

    @script.setter
    def script (self, script):
        """Sets the script of this name.

        :param script: script to set
        :type script: `Script`

        """
        script_id = script.get(XML + 'id')
        self.set('script', script_id)


class NamedElement (EATSMLElementBase):

    """Base class for elements that have a name."""

    @property
    def name (self):
        return _get_name(self)[0].text


class UserPreferredElement (EATSMLElementBase):

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


class PropertyAssertion (EATSMLElementBase):

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


class Collection (EATSMLElementBase):

    def create_entity (self, xml_id):
        """Creates a new `Entity` element.

        :param xml_id: XML id of new entity
        :type xml_id: `str`
        :rtype: `Entity`

        """
        if len(self) == 0 or self[-1].tag != EATSML + 'entities':
            entities = etree.SubElement(self, EATSML + 'entities')
        else:
            entities = self[-1]
        entity = etree.SubElement(entities, EATSML + 'entity')
        entity.set(XML + 'id', xml_id)
        return entity

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


class Date (EATSMLElementBase):

    @property
    def assembled_form (self):
        """Return's this date's assembled form.

        :rtype: `str`

        """
        return _get_assembled_form(self)[0].text


class Entity (EATSMLElementBase):

    _indices = {
        EATSML + 'entity_relationships': 0,
        EATSML + 'entity_types': 1,
        EATSML + 'existences': 2,
        EATSML + 'names': 3,
        EATSML + 'notes': 4,
        EATSML + 'subject_identifiers': 5}

    def create_entity_type (self, authority, entity_type):
        entity_types = self._get_or_create_element(_get_entity_types_element,
                                                   EATSML + 'entity_types')
        assertion = etree.SubElement(entity_types, EATSML + 'entity_type')
        assertion.authority = authority
        assertion.entity_type = entity_type

    def create_existence (self, authority):
        existences = self._get_or_create_element(_get_existences_element,
                                                 EATSML + 'existences')
        assertion = etree.SubElement(existences, EATSML + 'existence')
        assertion.authority = authority

    def create_name (self, authority, name_type, language, script,
                     display_form, is_preferred=True):
        """Returns a newly created `NamePropertyAssertion`, using the
        details provided.

        :param authority: authority asserting the name
        :type authority: `Authority`
        :param name_type: type of the name
        :type name_type: `NameType`
        :param language: language of the name
        :type language: `Language`
        :param script: script of the name
        :type script: `Script`
        :param display_form: display form of the name
        :type display_form: `str`
        :param is_preferred: whether the name is preferred
        :type is_preferred: `bool`
        :rtype: `NamePropertyAssertion`

        """
        names = self._get_or_create_element(_get_names_element,
                                            EATSML + 'names')
        assertion = etree.SubElement(names, EATSML + 'name')
        assertion.authority = authority
        assertion.name_type = name_type
        assertion.language = language
        assertion.script = script
        assertion.display_form = display_form
        assertion.is_preferred = is_preferred
        return assertion

    def create_note (self, authority, note):
        notes = self._get_or_create_element(_get_notes_element,
                                            EATSML + 'notes')
        assertion = etree.SubElement(notes, EATSML + 'note')
        assertion.authority = authority
        assertion.note = note
        return assertion

    def get_entity_types (self):
        return _get_entity_types(self, current=self.get(XML + 'id'))

    def get_existence_dates (self):
        return _get_existence_dates(self)

    def get_names (self):
        return _get_names(self)

    def get_notes (self):
        return _get_notes(self)

    def get_preferred_entity_types (self, authority):
        """Returns the `EntityType`\s that are used in assertions for
        this entity that are associated with `authority`.

        :param authority: authority the entity types must be associated with
        :type authority: `Authority`
        :rtype: list of `EntityType`\s

        """
        authority_id = authority.get(XML + 'id')
        return _get_preferred_entity_types(self, authority=authority_id,
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


class EntityRelationship (EATSMLElementBase):

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


class EntityTypePropertyAssertion (PropertyAssertion):

    @property
    def entity_type (self):
        entity_type_id = self.get('entity_type')
        return self._get_element_by_id(entity_type_id)

    @entity_type.setter
    def entity_type (self, entity_type):
        entity_type_id = entity_type.get(XML + 'id')
        self.set('entity_type', entity_type_id)


class ExistencePropertyAssertion (PropertyAssertion):

    pass


class Language (NamedElement, UserPreferredElement):

    pass


class NamePart (NameElement):

    @property
    def display_form (self):
        """Returns the display form of this name part.

        :rtype: `str`

        """
        return self.text

    @display_form.setter
    def display_form (self, display_form):
        """Sets the display form of this name part.

        :param display_form: display form to set
        :type display_form: `str`

        """
        self.text = display_form.decode('utf-8')

    @property
    def name_part_type (self):
        """Returns the type of this name part.

        :rtype: `NamePartType`

        """
        name_part_type_id = self.get('name_part_type')
        return self._get_element_by_id(name_part_type_id)

    @name_part_type.setter
    def name_part_type (self, name_part_type):
        """Sets the type of this name part.

        :param name_part_type: type to set
        :type name_part_type: `NamePartType`

        """
        name_part_type_id = name_part_type.get(XML + 'id')
        self.set('name_part_type', name_part_type_id)


class NamePropertyAssertion (NameElement, PropertyAssertion):

    _indices = {
        EATSML + 'assembled_form': 0,
        EATSML + 'display_form': 1,
        EATSML + 'name_parts': 2}

    @property
    def assembled_form (self):
        """Returns this name's assembled form.

        :rtype: `str`

        """
        return _get_assembled_form(self)[0].text

    def create_name_part (self, name_part_type, display_form, language=None,
                          script=None):
        name_parts = self._get_or_create_element(_get_name_parts_element,
                                                 EATSML + 'name_parts')
        name_part = etree.SubElement(name_parts, EATSML + 'name_part')
        name_part.name_part_type = name_part_type
        name_part.language = language or self.language
        name_part.script = script or self.script
        name_part.display_form = display_form

    @property
    def display_form (self):
        """Returns the display form of this name.

        :rtype: `str`

        """
        return _get_display_form(self)

    @display_form.setter
    def display_form (self, display_form):
        """Sets the display form of this name.

        :param display_form: display form to set
        :type display_form: `str`

        """
        element = self._get_or_create_element(_get_display_form_element,
                                              EATSML + 'display_form')
        element.text = display_form.decode('utf-8')

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

    @property
    def is_preferred (self):
        """Returns whether this name is preferred or not.

        :rtype: `bool`

        """
        text = self.get('is_preferred')
        if text == 'true':
            value = True
        else:
            value = False
        return value

    @is_preferred.setter
    def is_preferred (self, is_preferred):
        """Sets whether this name is preferred.

        :param is_preferred: preference value to set
        :type is_preferred: `bool`

        """
        if is_preferred:
            value = 'true'
        else:
            value = 'false'
        self.set('is_preferred', value)

    @property
    def name_type (self):
        """Returns the type of this name.

        :rtype: `NameType`

        """
        name_type_id = self.get('name_type')
        return self._get_element_by_id(name_type_id)

    @name_type.setter
    def name_type (self, name_type):
        """Sets the type of this name.

        :param name_type: type to set
        :type name_type: `NameType`

        """
        name_type_id = name_type.get(XML + 'id')
        self.set('name_type', name_type_id)


class NotePropertyAssertion (PropertyAssertion):

    @property
    def note (self):
        """Returns the text of this note.

        :rtype: `str`

        """
        return self.text

    @note.setter
    def note (self, text):
        """Sets the text of this note.

        :param note: note text to set
        :type note: `str`

        """
        self.text = text.decode('utf-8')


class NameType (NamedElement):

    pass


class Script (NamedElement, UserPreferredElement):

    @property
    def separator (self):
        """Returns this script's separator.

        :rtype: `str`

        """
        return _get_separator(self)[0]


def get_element_index (parent, indices, full_index, possible_index):
    """Returns the index of the position among `parent`'s children
    that best corresponds to the index `full_index` (which is the
    index when all children are present in the correct order).

    This functions recurses, and assumes that on the first call,
    `possible_index` is the highest meaningful value - the recursion
    operates on a reduced value each call.

    :param parent: parent element
    :type parent: `etree.ElementBase`
    :param indices: dictionary of child elements and their indices
      within a full set of children
    :type indices: `dict`
    :param full_index: index of element within a full set of children
    :type full_index: `int`
    :param possible_index: index that is a candidate for being the
      correct index within `parent`'s children
    :type possible_index: `int`
    :rtype: `int`

    """
    if possible_index == -1:
        index = 0
    else:
        element_at_index = parent[possible_index]
        element_full_index = indices[element_at_index.tag]
        if element_full_index < full_index:
            # element_at_index is an element that occurs before the
            # element whose index we want, so that index is one greater
            # than the possible index.
            index = possible_index + 1
        else:
            index = get_element_index(parent, indices, full_index,
                                      possible_index - 1)
    return index


parser = etree.XMLParser()
parser.set_element_class_lookup(EATSMLElementLookup())
