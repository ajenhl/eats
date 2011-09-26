"""Module providing custom element classs and lookup for lxml parsing
of EATSML."""

from lxml import etree

from constants import EATSML, XML, XPATH_NSMAP

# Compile XPath expressions into functions (for performance). While
# most are specific to a single element class defined below, some are
# not and so all are defined here.
_get_element_by_id = etree.XPath('id($element_id)')
_get_authorities = etree.XPath('e:authorities/e:authority',
                               namespaces=XPATH_NSMAP)
_get_default_authority = etree.XPath('e:authorities/e:authority[@user_default="true"]',
                                     namespaces=XPATH_NSMAP)
_get_entity_types = etree.XPath('e:entity_types/e:entity_type',
                                namespaces=XPATH_NSMAP)
_get_entity_relationship_types = etree.XPath('e:entity_relationship_types/e:entity_relationship_type',
                                             namespaces=XPATH_NSMAP)
_get_entity_relationship_type = etree.XPath('e:entity_relationship_types/e:entity_relationship_type[@authority=$authority][.=$name]',
                                            namespaces=XPATH_NSMAP)
_get_languages = etree.XPath('e:languages/e:language', namespaces=XPATH_NSMAP)
_get_language = etree.XPath('e:languages/e:language[e:code=$code]',
                            namespaces=XPATH_NSMAP)
_get_scripts = etree.XPath('e:scripts/e:script', namespaces=XPATH_NSMAP)
_get_script = etree.XPath('e:scripts/e:script[e:code=$code]',
                          namespaces=XPATH_NSMAP)
_get_name_types = etree.XPath('e:name_types/e:name_type',
                              namespaces=XPATH_NSMAP)
_get_name_type = etree.XPath('e:name_types/e:name_type[@authority=$authority][.=$name]',
                             namespaces=XPATH_NSMAP)
_get_name_part_types = etree.XPath('e:name_part_types/e:name_part_type',
                                   namespaces=XPATH_NSMAP)
_get_name_part_type = etree.XPath('e:name_part_types/e:name_part_type[@authority=$authority][. = $part_name]',
                                  namespaces=XPATH_NSMAP)
_get_authority_records_element = etree.XPath('e:authority_records',
                                             namespaces=XPATH_NSMAP)
_get_entities = etree.XPath('e:entities/e:entity[not(@is_related="true")]',
                            namespaces=XPATH_NSMAP)
_get_default_authority_records = etree.XPath('/e:collection/e:authority_records/e:authority_record[@authority=$authority][id($id)/e:existence_assertions/e:existence_assertion/@authority_record=@xml:id]',
                                             namespaces=XPATH_NSMAP)
_get_existence_dates = etree.XPath('e:existence_assertions/e:existence_assertion/e:dates/e:date',
                                   namespaces=XPATH_NSMAP)
_get_entity_type_assertions = etree.XPath('e:entity_type_assertions/e:entity_type_assertion',
                                          namespaces=XPATH_NSMAP)
_get_default_entity_types = etree.XPath('/e:collection/e:entity_types/e:entity_type[@xml:id=id($current)/e:entity_type_assertions/e:entity_type_assertion[id(@authority_record)/@authority=$authority]/@entity_type]',
                                        namespaces=XPATH_NSMAP)
_get_names = etree.XPath('e:name_assertions/e:name_assertion',
                         namespaces=XPATH_NSMAP)
_get_default_name = etree.XPath('e:name_assertions/e:name_assertion[@user_default="true"]',
                                namespaces=XPATH_NSMAP)
_get_relationships = etree.XPath('e:entity_relationship_assertions/e:entity_relationship_assertion',
                                 namespaces=XPATH_NSMAP)
_get_reverse_relationships = etree.XPath('../e:entity/e:entity_relationship_assertions/e:entity_relationship_assertion[@related_entity=$entity]',
                                         namespaces=XPATH_NSMAP)
_get_entity_notes = etree.XPath('e:entity_note_assertions/e:entity_note_assertion',
                         namespaces=XPATH_NSMAP)
_get_existences = etree.XPath('e:existence_assertions', namespaces=XPATH_NSMAP)
_get_entity_type_assertions_element = etree.XPath('e:entity_type_assertions',
                                                  namespaces=XPATH_NSMAP)
_get_name_assertions_element = etree.XPath('e:name_assertions',
                                           namespaces=XPATH_NSMAP)
_get_entity_relationship_assertions_element = etree.XPath('e:entity_relationship_assertions',
                                                          namespaces=XPATH_NSMAP)
_get_dates = etree.XPath('e:dates/e:date', namespaces=XPATH_NSMAP)
_get_display_form = etree.XPath('e:display_form', namespaces=XPATH_NSMAP)
_get_name_part = etree.XPath('e:name_parts/e:name_part[@type=$name_part_type]',
                             namespaces=XPATH_NSMAP)
_get_name_parts_element = etree.XPath('e:name_parts', namespaces=XPATH_NSMAP)
_get_name_relationships_element = etree.XPath('../../e:name_relationship_assertions',
                                              namespaces=XPATH_NSMAP)
_get_entity_notes_element = etree.XPath('e:entity_note_assertions',
                                       namespaces=XPATH_NSMAP)
_get_authorities_element = etree.XPath('e:authorities',
                                       namespaces=XPATH_NSMAP)

# Dictionaries of child element names with their prescribed order
# index, for determing where to insert a new element.
_collection_indices = {EATSML + 'authorities': 0,
                       EATSML + 'entity_types': 1,
                       EATSML + 'entity_relationship_types': 2,
                       EATSML + 'name_types': 3,
                       EATSML + 'system_name_part_types': 4,
                       EATSML + 'name_part_types': 5,
                       EATSML + 'languages': 6,
                       EATSML + 'scripts': 7,
                       EATSML + 'name_relationship_types': 8,
                       EATSML + 'date_periods': 9,
                       EATSML + 'date_types': 10,
                       EATSML + 'calendars': 11,
                       EATSML + 'authority_records': 12,
                       EATSML + 'entities': 13}

_entity_indices = {EATSML + 'existence_assertions': 0,
                   EATSML + 'entity_type_assertions': 1,
                   EATSML + 'entity_note_assertions': 2,
                   EATSML + 'entity_reference_assertions': 3,
                   EATSML + 'name_assertions': 4,
                   EATSML + 'entity_relationship_assertions': 5,
                   EATSML + 'name_relationship_assertions': 6}


class ElementLookup (etree.CustomElementClassLookup):

    def lookup (self, node_type, document, namespace, name):
        _class = None
        if node_type == 'element':
            if name == 'collection':
                _class = CollectionElementClass
            elif name == 'authority':
                _class = AuthorityElementClass
            elif name == 'entity_type':
                _class = EntityTypeItemElementClass
            elif name == 'entity_relationship_type':
                _class = EntityRelationshipTypeElementClass
            elif name == 'name_type':
                _class = NameTypeElementClass
            elif name == 'language':
                _class = LanguageElementClass
            elif name == 'script':
                _class = ScriptElementClass
            elif name == 'name_relationship_type':
                _class = NameRelationshipTypeElementClass
            elif name == 'name_part_type':
                _class = NamePartTypeElementClass
            elif name == 'date_period':
                _class = DatePeriodElementClass
            elif name == 'date_type':
                _class = DateTypeElementClass
            elif name == 'calendar':
                _class = CalendarElementClass
            elif name == 'authority_record':
                _class = AuthorityRecordElementClass
            elif name == 'entity':
                _class = EntityElementClass
            elif name == 'existence_assertion':
                _class = ExistenceElementClass
            elif name == 'entity_type_assertion':
                _class = EntityTypeElementClass
            elif name == 'name_assertion':
                _class = NameElementClass
            elif name == 'name_part':
                _class = NamePartElementClass
            elif name == 'name_relationship_assertion':
                _class = NameRelationshipElementClass
            elif name == 'entity_relationship_assertion':
                _class = EntityRelationshipElementClass
            elif name == 'entity_note_assertion':
                _class = EntityNoteElementClass
            elif name == 'date':
                _class = DateElementClass
        return _class


class EATSMLElementBase (etree.ElementBase):

    """Superclass for all EATSML element classes."""

    child_indices = None

    def __get_id (self):
        """Return the xml:id of the element."""
        return self.get(XML + 'id')

    def __set_id (self, id):
        """Set the xml:id of the element."""
        self.set(XML+ 'id', id)

    id = property(__get_id, __set_id)

    def __get_eats_id (self):
        """Return the EATS ID of the element."""
        return self.get('eats_id')

    def __set_eats_id (self, eats_id):
        """Set the EATS ID of the element."""
        self.set('eats_id', eats_id)

    eats_id = property(__get_eats_id, __set_eats_id)

    def delete (self):
        """Delete the element."""
        self.getparent().remove(self)

    def get_element_by_id (self, element_id):
        """Return element with XML ID of `element_id`.

        Arguments:

        - `element_id`: string

        """
        if element_id is None:
            element = None
        else:
            nodeset = _get_element_by_id(self, element_id=element_id)
            element = self.get_node_or_none(nodeset)
        return element

    def get_element_index (self, parent, element_name):
        """Return the index at which to insert a new element of name
        `element_name`.

        Arguments:

        - `parent`: element parent of new element
        - `element_name`: string name of element to find the index for

        """
        child_indices = parent.child_indices
        try:
            full_index = child_indices[element_name]
        except KeyError:
            # QAZ
            raise Exception
        except TypeError:
            # QAZ
            raise Exception
        check_index = full_index
        if full_index >= len(parent):
            check_index = len(parent) - 1
        index = self.__get_element_index(parent, child_indices, full_index, check_index)
        return index

    def __get_element_index (self, parent, child_indices, full_index, check_index):
        """Return the index of the position among `parent`'s children
        that best corresponds to the index `full_index` (which is the
        index when all children are present in the correct order).

        Arguments:

        - `parent`: parent element
        - `child_indices`: dictionary of child elements and their
          indices within a full set of children
        - `full_index`: index of element within a full set of children
        - `check_index`: index that is a candidate for being the
          correct index within `parent`'s children

        """
        if check_index == -1:
            index = 0
        else:
            element_at_index = parent[check_index]
            element_full_index = child_indices[element_at_index.tag]
            if element_full_index < full_index:
                # element_at_index is an element that occurs before the
                # element whose index we want, so that index is one
                # greater than the check_index.
                index = check_index + 1
            else:
                index = self.__get_element_index(parent, child_indices, full_index, check_index-1)
        return index

    def get_or_create_element (self, xpath, element_name, parent):
        """Return the element that matches `xpath`, first creating it
        if it doesn't already exist.

        Arguments:

        - `xpath`: XPath function
        - `element_name`: string name of element to be found/created
        - `parent`: element of parent of new element

        """
        nodeset = xpath(self)
        if nodeset:
            element = nodeset[0]
        else:
            element = etree.Element(element_name)
            index = self.get_element_index(parent, element_name)
            parent.insert(index, element)
        return element

    @staticmethod
    def get_node_or_none (nodeset):
        """Return the sole member of nodeset, or None if the nodeset
        is empty.

        Arguments:

        - `nodeset`: list of `lxml.etree.Element` objects

        """
        if len(nodeset) == 1:
            return nodeset[0]
        elif len(nodeset) == 0:
            return None
        else:
            # QAZ
            raise Exception

    @staticmethod
    def convert_none_to_text (text):
        """If `text` is None, return an empty string; else return
        `text`. Necessary due to a bug in lxml before 2.2 where
        `Element.findtext()` would return None if there was no text
        content."""
        if text is None:
            text = ''
        return text


class UserDefaultableElement (object):

    """Superclass for those element classes that can have a user
    default."""

    @property
    def is_user_default (self):
        """Return True if this element's user_default attribute value
        is true."""
        value = self.get('user_default')
        if value in ('true', '1'):
            return True
        return False
    
        
class AuthorityDataElementBase (EATSMLElementBase):

    """Superclass for those element classes that model
    authority-specific data."""

    def __get_authority (self):
        authority_id = self.get('authority')
        return self.get_element_by_id(authority_id)

    def __set_authority (self, authority):
        """Set the authority for this element.

        Arguments:

        - `authority`: authority element

        """
        self.set('authority', authority.id)

    authority = property(__get_authority, __set_authority)

        
class CollectionElementClass (EATSMLElementBase):

    child_indices = _collection_indices

    def get_authorities (self):
        """Return a list of the authorities in the document."""
        return _get_authorities(self)

    def get_default_authority (self):
        """Return the user's default authority."""
        nodeset = _get_default_authority(self)
        return self.get_node_or_none(nodeset)
    
    def get_entity_types (self):
        """Return a list of the entity types in the document."""
        return _get_entity_types(self)

    def get_entity_relationship_types (self):
        """Return a list of the entity relationships types in the
        document."""
        return _get_entity_relationship_types(self)
    
    def get_entity_relationship_type (self, authority, name):
        """Return the entity relationship type element associated with
        `authority` and named `name`.

        Arguments:

        - `authority`: authority element
        - `name`: string name of type

        """
        nodeset = _get_entity_relationship_type(self, authority=authority.id, name=name)
        return self.get_node_or_none(nodeset)

    def get_languages (self):
        """Return a list of the language elements in the document."""
        return _get_languages(self)

    def get_language (self, code):
        """Return the language element identified by `code`.

        - `code`: language code

        """
        nodeset = _get_language(self, code=code)
        return self.get_node_or_none(nodeset)

    def get_scripts (self):
        """Return a list of the script elements in the document."""
        return _get_scripts(self)

    def get_script (self, code):
        """Return the script element identified by `code`.

        - `code`: script code

        """
        nodeset = _get_script(self, code=code)
        return self.get_node_or_none(nodeset)

    def get_name_types (self):
        """Return a list of the name type elements in the document."""
        return _get_name_types(self)

    def get_name_type (self, authority, name):
        """Return the name type element associated with `authority`
        and called `name`.

        Arguments:

        - `authority`: authority element
        - `name`: string name of type

        """
        nodeset = _get_name_type(self, name=name, authority=authority.id)
        return self.get_node_or_none(nodeset)

    def get_name_part_types (self):
        """Return a list of the name part type elements in the document."""
        return _get_name_part_types(self)
    
    def get_name_part_type (self, authority, part_name):
        """Return the name part type element associated with
        `authority_id` and called `part_name`.

        Arguments:

        - `authority`: associated authority element
        - `part_name`: string name of the name part type

        """
        nodeset = _get_name_part_type(self, authority=authority.id,
                                      part_name=part_name)
        return self.get_node_or_none(nodeset)

    def create_authority (self, id=None):
        """Return a new authority element.

        Creates the containing authorities element if such does not
        already exist.

        Arguments:

        - `id`: string ID of the new element

        """
        authorities = self.get_or_create_element(
            _get_authorities_element, EATSML + 'authorities',
            self)
        authority = etree.SubElement(authorities,
                                     EATSML + 'authority')
        # Create required children.
        etree.SubElement(authority, EATSML + 'name')
        etree.SubElement(authority, EATSML + 'abbreviated_name')
        etree.SubElement(authority, EATSML + 'base_id')
        etree.SubElement(authority, EATSML + 'base_url')
        if id is not None:
            authority.id = id
        return authority

    def create_authority_record (self, id=None, eats_id=None, authority=None):
        """Return a new authority record element.

        Create the containing authority records element if such does
        not already exist.

        Arguments:

        - `id`: string xml:id
        - `eats_id`: string EATS ID
        - `authority`: authority element

        """
        authority_records = self.get_or_create_element(
            _get_authority_records_element,
            EATSML + 'authority_records', self)
        authority_record = etree.SubElement(authority_records,
                                            EATSML + 'authority_record')
        if id is not None:
            authority_record.id = id
        if eats_id is not None:
            authority_record.eats_id = eats_id
        if authority is not None:
            authority_record.authority = authority
        return authority_record
    
    def get_entities (self):
        """Return a list of the primary entity elements in the
        document."""
        return _get_entities(self)

    def create_entity (self, id=None, eats_id=None):
        """Return a new entity element.

        Creates the containing entities element if such does not
        already exist.

        Arguments:

        - `id`: string xml:id
        - `eats_id`: string EATS ID

        """
        if self[-1].tag == EATSML + 'entities':
            entities = self[-1]
        else:
            entities = etree.SubElement(self, EATSML + 'entities')
        entity = etree.SubElement(entities, EATSML + 'entity')
        if id is not None:
            entity.id = id
        if eats_id is not None:
            entity.eats_id = eats_id
        return entity
    

class AuthorityElementClass (EATSMLElementBase, UserDefaultableElement):

    # It is assumed that an authority element already has the required
    # child elements; these are created by
    # CollectionElementClass.create_authority.

    def __get_name (self):
        return self.convert_none_to_text(self[0].text)

    def __set_name (self, name):
        """Set the name of this authority.

        Assumes that all of the required children of the authority
        element are present.

        Arguments:

        - `name`: string

        """
        name_element = self[0]
        name_element.text = name

    name = property(__get_name, __set_name)

    def __get_short_name (self):
        """Return the abbreviated name of this authority."""
        return self.convert_none_to_text(self[1].text) or self.name

    def __set_short_name (self, short_name):
        """Set the abbreviated name of this authority.

        Assumes that all of the required children of the authority
        element are present.

        Arguments:

        - `short_name`: string

        """
        short_name_element = self[1]
        short_name_element.text = short_name

    short_name = property(__get_short_name, __set_short_name)

    def __get_base_id (self):
        """Return the base ID of this authority."""
        return self.convert_none_to_text(self[2].text)

    def __set_base_id (self, base_id):
        """Set the base ID of this authority.

        Assumes that all of the required children of the authority
        element are present.

        Arguments:

        - `base_id`: string

        """
        base_id_element = self[2]
        base_id_element.text = base_id

    base_id = property(__get_base_id, __set_base_id)

    def __get_base_url (self):
        """Return the base URL of this authority."""
        return self.convert_none_to_text(self[3].text)

    def __set_base_url (self, base_url):
        """Set the base URL of this authority.

        Assumes that all of the required children of the authority
        element are present.

        Arguments:

        - `base_url`: string

        """
        base_url_element = self[3]
        base_url_element.text = base_url

    base_url = property(__get_base_url, __set_base_url)


class NameTypeElementClass (AuthorityDataElementBase, UserDefaultableElement):

    def __unicode__ (self):
        return self.text

        
class EntityTypeItemElementClass (AuthorityDataElementBase):

    def __unicode__ (self):
        return self.text


class EntityRelationshipTypeElementClass (AuthorityDataElementBase):

    def __unicode__ (self):
        return self.text


class LanguageElementClass (EATSMLElementBase, UserDefaultableElement):

    def __get_code (self):
        return self.convert_none_to_text(self[1].text)

    def __set_code (self, code):
        """Set the code for this language.

        Arguments:

        - `code`: string

        """
        code_element = self[1]
        code_element.text = code
    
    code = property(__get_code, __set_code)
    
    def __get_name (self):
        return self.convert_none_to_text(self[0].text)

    def __set_name (self, name):
        """Set the name for this language.

        Arguments:

        - `name`: string

        """
        name_element = self[0]
        name_element.text = name

    name = property(__get_name, __set_name)


class ScriptElementClass (EATSMLElementBase, UserDefaultableElement):

    def __get_code (self):
        return self.convert_none_to_text(self[1].text)

    def __set_code (self, code):
        """Set the code for this language.

        Arguments:

        - `code`: string

        """
        code_element = self[1]
        code_element.text = code
    
    code = property(__get_code, __set_code)
    
    def __get_name (self):
        return self.convert_none_to_text(self[0].text)

    def __set_name (self, name):
        """Set the name for this language.

        Arguments:

        - `name`: string

        """
        name_element = self[0]
        name_element.text = name

    name = property(__get_name, __set_name)


class NameRelationshipTypeElementClass (AuthorityDataElementBase):

    def __unicode__ (self):
        return self.text


class NamePartTypeElementClass (EATSMLElementBase):

    pass


class DatePeriodElementClass (EATSMLElementBase):

    def __unicode__ (self):
        return self.text


class DateTypeElementClass (EATSMLElementBase):

    def __unicode__ (self):
        return self.text


class CalendarElementClass (EATSMLElementBase):

    def __unicode__ (self):
        return self.text


class AuthorityRecordElementClass (AuthorityDataElementBase):

    def __get_authority_system_id (self):
        """Return the full authority system id."""
        system_id_element = self.find(EATSML + 'authority_system_id')
        if system_id_element is None:
            system_id = None
        else:
            system_id = system_id_element.text
            if system_id_element.get('is_complete') == 'false':
                authority = self.authority
                if authority is not None:
                    system_id = authority.base_id + system_id
        return system_id

    def __set_authority_system_id (self, authority_system_id):
        """Set the authority system id for this authority record.

        Arguments:

        - `authority_system_id`: string
        
        """
        system_id_element = self.find(EATSML + 'authority_system_id')
        if system_id_element is None:
            system_id_element = etree.Element(EATSML + 'authority_system_id')
            self.insert(0, system_id_element)
        system_id_element.text = authority_system_id
    
    system_id = property(__get_authority_system_id, __set_authority_system_id)

    def __get_authority_system_id_is_complete (self):
        """Return a Boolean of whether the system id is complete."""
        system_id_element = self.find(EATSML + 'authority_system_id')
        if system_id_element is None:
            is_complete = None
        else:
            if system_id_element.get('is_complete') == 'false':
                is_complete = False
            else:
                is_complete = True
        return is_complete

    def __set_authority_system_id_is_complete (self, is_complete):
        """Set the is_complete attribute of the system id.

        Arguments:

        - `is_complete`: Boolean

        """
        system_id_element = self.find(EATSML + 'authority_system_id')
        if system_id_element is not None:
            system_id_element.set('is_complete', str(is_complete).lower())

    system_id_is_complete = property(__get_authority_system_id_is_complete,
                                     __set_authority_system_id_is_complete)

    def __get_authority_system_url (self):
        """Return the full authority system URL."""
        system_url_element = self.find(EATSML + 'authority_system_url')
        if system_url_element is None:
            system_url = None
        else:
            system_url = system_url_element.text
            if system_url_element.get('is_complete') == 'false':
                authority = self.authority
                if authority is not None:
                    system_url = authority.base_url + system_url
        return system_url

    def __set_authority_system_url (self, authority_system_url):
        """Set the authority system id for this authority record.

        Arguments:

        - `authority_system_id`: string
        
        """
        system_url_element = self.find(EATSML + 'authority_system_url')
        if system_url_element is None:
            system_url_element = etree.Element(EATSML + 'authority_system_url')
            self.insert(1, system_url_element)
        system_url_element.text = authority_system_url
    
    system_url = property(__get_authority_system_url, __set_authority_system_url)
    
    def __get_authority_system_url_is_complete (self):
        """Return a Boolean of whether the system url is complete."""
        system_url_element = self.find(EATSML + 'authority_system_url')
        if system_url_element is None:
            is_complete = None
        else:
            if system_url_element.get('is_complete') == 'false':
                is_complete = False
            else:
                is_complete = True
        return is_complete

    def __set_authority_system_url_is_complete (self, is_complete):
        """Set the is_complete attribute of the system url.

        Arguments:

        - `is_complete`: Boolean

        """
        system_url_element = self.find(EATSML + 'authority_system_url')
        if system_url_element is not None:
            system_url_element.set('is_complete', str(is_complete).lower())

    system_url_is_complete = property(__get_authority_system_url_is_complete,
                                      __set_authority_system_url_is_complete)

    def set_auto_create_data (self, auto_create=True):
        """Set the authority record to have an auto_create_data
        attribute if `auto_create` is true, and remove any such
        attribute if false.

        Arguments:

        - `auto_create`: Boolean

        """
        if auto_create:
            self.set('auto_create_data', 'true')
            # Remove any system ID and URL that may have been set.
            self[:] = []
        else:
            del self.attrib['auto_create_data']


class EntityElementClass (EATSMLElementBase):

    child_indices = _entity_indices

    def get_default_authority_records (self):
        """Return a list of default (user preferred) authority records
        that are relevant to this entity."""
        collection = self.getparent().getparent()
        try:
            default_authority_id = collection.get_default_authority().id
            records = _get_default_authority_records(
                self, authority=default_authority_id, id=self.id)
        except AttributeError:
            records = []
        return records

    def get_existence_dates (self):
        """Return a list of date elements associated with existence
        records for this entity."""
        dates = _get_existence_dates(self)
        return dates

    def get_entity_types (self):
        """Return a list of entity types for this entity."""
        return _get_entity_type_assertions(self)

    def get_default_entity_types (self):
        """Return a list of default (user preferred) entity types for
        this entity."""
        collection = self.getparent().getparent()
        try:
            default_authority_id = collection.get_default_authority().id
            entity_types = _get_default_entity_types(
                self, authority=default_authority_id, current=self.id)
        except AttributeError:
            # The default authority is not part of this EATSML
            # document.
            entity_types = []
        return entity_types

    def get_names (self):
        """Return a list of names for this entity."""
        return _get_names(self)

    def get_default_name (self):
        """Return the default (user preferred) name for this entity,
        or None if there isn't such."""
        nodeset = _get_default_name(self)
        return self.get_node_or_none(nodeset)

    def get_relationships (self):
        """Return a list of relationships for this entity."""
        return _get_relationships(self)

    def get_reverse_relationships (self):
        """Return a list of reverse relationships for this entity.

        The relationship elements returned are descendants of entities
        other than this one."""
        return _get_reverse_relationships(self, entity=self.id)

    def get_notes (self):
        """Return a list of notes (both internal and external) for
        this entity."""
        return _get_entity_notes(self)

    def create_existence (self, id=None, authority_record=None,
                          is_preferred=False):
        """Create and return a new existence assertion element.

        Creates an existence assertions element if none such exists
        already.

        Arguments:

        - `id`: string ID
        - `authority_record`: authority record element
        - `is_preferred`: Boolean

        """
        existences = self.get_or_create_element(
            _get_existences, EATSML + 'existence_assertions',
            self)
        existence = etree.SubElement(existences, EATSML + 'existence_assertion')
        if id is not None:
            existence.id = id
        if authority_record is not None:
            existence.authority_record = authority_record
        existence.is_preferred = is_preferred
        return existence

    def create_entity_type (self, id=None, authority_record=None,
                            entity_type=None, is_preferred=False):
        """Create and return a new entity type assertion element.

        Creates an entity type assertions element if none such exists
        already.

        Arguments:

        - `id`: string ID
        - `authority_record`: authority record element
        - `entity_type`: entity type element
        - `is_preferred`: Boolean

        """
        entity_types = self.get_or_create_element(
            _get_entity_type_assertions_element, EATSML + 'entity_type_assertions',
            self)
        entity_type_element = etree.SubElement(
            entity_types, EATSML + 'entity_type_assertion')
        if id is not None:
            entity_type_element.id = id
        if authority_record is not None:
            entity_type_element.authority_record = authority_record
        if entity_type is not None:
            entity_type_element.entity_type = entity_type
        entity_type_element.is_preferred = is_preferred
        return entity_type_element

    def create_name (self, id=None, authority_record=None,
                     name_type=None, is_preferred=False):
        """Create and return a new name assertion element.

        Creates a name assertions element if none such exists already.

        Arguments:

        - `id`: string ID
        - `authority_record`: authority record element
        - `name_type`: name type element
        - `is_preferred`: Boolean

        """
        name_assertions = self.get_or_create_element(
            _get_name_assertions_element,
            EATSML + 'name_assertions', self)
        name = etree.SubElement(name_assertions, EATSML +
                                'name_assertion')
        if id is not None:
            name.id = id
        if authority_record is not None:
            name.authority_record = authority_record
        if name_type is not None:
            name.type = name_type
        name.is_preferred = is_preferred
        return name

    def create_entity_relationship (self, id=None, authority_record=None,
                                    related_entity=None, relationship_type=None,
                                    is_preferred=False):
        """Create and return a new entity relationship assertion
        element.

        Creates an entity relationship assertions element if none such
        exists already.

        Arguments:

        - `id`: string ID of new element
        - `authority_record`: authority record element
        - `related_entity`: entity element
        - `relationship_type`: entity relationship type element
        - `is_preferred`: Boolean

        """
        entity_relationship_assertions = self.get_or_create_element(
            _get_entity_relationship_assertions_element,
            EATSML + 'entity_relationship_assertions', self)
        entity_relationship = etree.SubElement(
            entity_relationship_assertions,
            EATSML + 'entity_relationship_assertion')
        if id is not None:
            entity_relationship.id = id
        if authority_record is not None:
            entity_relationship.authority_record = authority_record
        if related_entity is not None:
            entity_relationship.related_entity = related_entity
        if relationship_type is not None:
            entity_relationship.relationship_type = relationship_type
        entity_relationship.is_preferred = is_preferred
        return entity_relationship

    def create_note (self, id=None, authority_record=None,
                     note_text=None, is_internal=True,
                     is_preferred=False):
        """Create and return a new entity note assertion element.

        Creates an entity note assertions element if none such exists
        already.

        Arguments:

        - `id`: string ID of new element
        - `authority_record`: authority record element
        - `note_text`: string text of note
        - `is_internal`: Boolean
        - `is_preferred`: Boolean

        """
        note_assertions = self.get_or_create_element(
            _get_entity_notes_element, EATSML + 'entity_note_assertions',
            self)
        note_assertion = etree.SubElement(note_assertions,
                                          EATSML + 'entity_note_assertion')
        # Created the required children.
        etree.SubElement(note_assertion, EATSML + 'note')
        if id is not None:
            note_assertion.id = id
        if authority_record is not None:
            note_assertion.authority_record = authority_record
        if note_text is not None:
            note_assertion.note = note_text
        note_assertion.is_internal = is_internal
        note_assertion.is_preferred = is_preferred
        return note_assertion


class PropertyAssertionElementBase (EATSMLElementBase):

    """Superclass for property assertion elements, providing methods
    for resolving (and caching) assertion references."""

    def __get_authority_record (self):
        """Return the authority record element associated with this
        property assertion."""
        authority_record_id = self.get('authority_record')
        return self.get_element_by_id(authority_record_id)

    def __set_authority_record (self, authority_record):
        """Set the authority record element associated with this
        property assertion.

        Arguments:

        - `authority_record`: authority record element

        """
        self.set('authority_record', authority_record.id)

    authority_record = property(__get_authority_record, __set_authority_record)

    def __get_is_preferred (self):
        """Return the is_preferred attribute."""
        return self.get('is_preferred')

    def __set_is_preferred (self, is_preferred):
        """Set the is_preferred attribute.

        Arguments:

        - `is_preferred`: Boolean

        """
        self.set('is_preferred', str(is_preferred).lower())

    is_preferred = property(__get_is_preferred, __set_is_preferred)

    def get_dates (self):
        """Return a list of date elements for this property."""
        return _get_dates(self)

    def create_date (self):
        raise NotImplementedError


class ExistenceElementClass (PropertyAssertionElementBase):

    pass


class EntityTypeElementClass (PropertyAssertionElementBase):

    def __get_entity_type (self):
        """Return the entity type element associated with this
        assertion."""
        entity_type_id = self.get('type')
        return self.get_element_by_id(entity_type_id)

    def __set_entity_type (self, entity_type):
        """Set the entity type for this assertion.

        Arguments:

        - `entity_type`: entity type element

        """
        self.set('entity_type', entity_type.id)

    entity_type = property(__get_entity_type, __set_entity_type)

    def __unicode__ (self):
        name = ''
        if self.entity_type is not None:
            name = unicode(self.entity_type)
        return name


class NameElementClass (PropertyAssertionElementBase, UserDefaultableElement):

    def get_display_name (self):
        """Return the display name of this name.

        This may be drawn from the display_form element, or the
        assembled_form element. To get only the contents of
        display_form, use the display_form property.

        """
        form = self.convert_none_to_text(self.findtext(EATSML + 'display_form'))
        if not form:
            form = self.assembled_form
        return form

    def __get_display_form (self):
        """Return the contents of the display_form element."""
        return self.convert_none_to_text(self.findtext(EATSML + 'display_form'))

    def __set_display_form (self, name):
        """Set the display_form element's text content."""
        display_form_nodes = _get_display_form(self)
        if display_form_nodes:
            display_form = display_form_nodes[0]
        else:
            display_form = etree.SubElement(self, EATSML + 'display_form')
        display_form.text = unicode(name)

    display_form = property(__get_display_form, __set_display_form)

    def __get_type (self):
        """Return the name type element associated with this name."""
        name_part_type_id = self.get('type')
        return self.get_element_by_id(name_part_type_id)

    def __set_type (self, name_type):
        """Set the name type of this name to `name_type`.

        Arguments:

        - `name_type`: name type element

        """
        self.set('type', name_type.id)

    type = property(__get_type, __set_type)

    def __get_language (self):
        """Return the language element associated with this name."""
        language_id = self.get('language')
        return self.get_element_by_id(language_id)

    def __set_language (self, language):
        """Set the language element associated with this name.

        Arguments:

        - `language`: language element

        """
        self.set('language', language.id)

    language = property(__get_language, __set_language)

    def __get_script (self):
        """Return the script element associated with this name."""
        script_id = self.get('script')
        return self.get_element_by_id(script_id)

    def __set_script (self, script):
        """Set the script element associated with this name.

        Arguments:

        - `script`: script element

        """
        self.set('script', script.id)

    script = property(__get_script, __set_script)

    @property
    def assembled_form (self):
        """Return the assembled form of this name."""
        return self.convert_none_to_text(self.findtext(EATSML + 'assembled_form'))

    def get_name_part (self, name_part_type):
        """Return the name part of this name that is of type
        `name_part_type`.

        Arguments:

        - `name_part_type`: name part type element

        """
        if name_part_type is None:
            return None
        name_part_type_id = name_part_type.id
        nodeset = _get_name_part(self, name_part_type=name_part_type_id)
        return self.get_node_or_none(nodeset)

    def create_name_part (self, name_part_type, name_part_value):
        """Create a new name part for this name.

        Creates a name_parts element if none such already exists.

        Arguments:

        - `name_part_type`: name part type element
        - `name_part_value`: string of name part

        """
        name_parts_nodes = _get_name_parts_element(self)
        if name_parts_nodes:
            name_parts = name_parts_nodes[0]
        else:
            name_parts = etree.SubElement(self, EATSML + 'name_parts')
        name_part = etree.SubElement(name_parts, EATSML + 'name_part')
        name_part.type = name_part_type
        name_part.text = unicode(name_part_value)

    def create_name_relationship (self, related_name=None,
                                  relationship_type=None, is_preferred=False):
        name_relationships_nodes = _get_name_relationships_element(self)
        if name_relationships_nodes:
            name_relationships = name_relationships_nodes[0]
        else:
            entity = self.getparent().getparent()
            name_relationships = etree.SubElement(
                entity, EATSML + 'name_relationship_assertions')
        name_relationship = etree.SubElement(
            name_relationships, EATSML + 'name_relationship_assertion')
        if related_name is not None:
            name_relationship.related_name = related_name
        if relationship_type is not None:
            name_relationship.type = relationship_type
        name_relationship.is_preferred = is_preferred


class NamePartElementClass (EATSMLElementBase):

    def __get_type (self):
        """Return the name part type element associated with this name
        part."""
        name_part_type_id = self.get('type')
        return self.get_element_by_id(name_part_type_id)

    def __set_type (self, name_part_type):
        """Set the name part type of this name part to
        `name_part_type`.

        Arguments:

        - `name_part_type`: name part type element

        """
        self.set('type', name_part_type.id)

    type = property(__get_type, __set_type)


class NameRelationshipElementClass (PropertyAssertionElementBase):

    def __get_relationship_type (self):
        """Return the name relationship type element associated with
        this relationship."""
        name_relationship_type_id = self.get('type')
        return self.get_element_by_id(name_relationship_type_id)

    def __set_relationship_type (self, name_relationship_type):
        """Set the name relationship type of this relationship to
        `name_relationship_type`.

        Arguments:

        - `name_relationship_type`: name relationship type element

        """
        self.set('type', name_relationship_type.id)

    relationship_type = property(__get_relationship_type,
                                 __set_relationship_type)

    def __get_name (self):
        """Return the name element that is the base of this
        relationship."""
        name_id = self.get('name')
        return self.get_element_by_id(name_id)

    name = property(__get_name)
    
    def __get_related_name (self):
        """Return the name element that is related by this
        relationship."""
        related_name_id = self.get('related_name')
        return self.get_element_by_id(related_name_id)

    def __set_related_name (self, related_name):
        """Set the related name of this relationship.

        `related_name` must be associated with the same entity as
        self.
        
        Arguments:

        - `related_name`: name element

        """
        related_name_entity = related_name.getparent().getparent()
        if related_name_entity != self.getparent().getparent():
            # QAZ
            raise Exception
        if related_name == self:
            # QAZ
            raise Exception
        related_name_authority = related_name.authority_record.authority
        name_authority = self.authority_record.authority
        if related_name_authority != name_authority:
            # QAZ
            raise Exception
        self.set('related_name', related_name.id)

    related_name = property(__get_related_name, __set_related_name)

    
class EntityRelationshipElementClass (PropertyAssertionElementBase):

    def __get_relationship_type (self):
        """Return the entity relationship type element associated with
        this relationship."""
        entity_relationship_type_id = self.get('type')
        return self.get_element_by_id(entity_relationship_type_id)

    def __set_relationship_type (self, entity_relationship_type):
        """Set the entity relationship type of this relationship to
        `entity_relationship_type`.

        Arguments:

        - `entity_relationship_type`: entity relationship type element

        """
        self.set('type', entity_relationship_type.id)

    relationship_type = property(__get_relationship_type,
                                 __set_relationship_type)

    def get_entity (self):
        """Return the entity that has this relationship."""
        return self.getparent().getparent()

    def __get_related_entity (self):
        """Return the entity element that is related by this relationship."""
        related_entity_id = self.get('related_entity')
        return self.get_element_by_id(related_entity_id)

    def __set_related_entity (self, related_entity):
        """Set the related entity of this relationship to
        `related_entity`.

        Arguments:

        - `related_entity`: entity element

        """
        if related_entity == self:
            # QAZ
            raise Exception
        self.set('related_entity', related_entity.id)

    related_entity = property(__get_related_entity, __set_related_entity)

    def get_assembled_form (self, entity=False, related_entity=False):
        """Return a textual representation of the relationship. One or
        other of `entity` and `related_entity` may be True, in
        which case that part of the text will be 'this entity'.

        Arguments:

        - `entity`: Boolean
        - `related_entity`: Boolean

        """
        if entity:
            entity_text = 'This entity'
            related_entity_text = self.related_entity.get_default_name().get_display_name()
        else:
            entity_text = self.get_entity().get_default_name().get_display_name()
            related_entity_text = 'this entity'
        relationship_text = unicode(self.relationship_type)
        return '%s %s %s' % (entity_text, relationship_text,
                             related_entity_text)


class EntityNoteElementClass (PropertyAssertionElementBase):

    def __get_is_internal (self):
        """Return True if this note is internal."""
        return self.get('is_internal')

    def __set_is_internal (self, is_internal):
        """Set this note's is_internal attribute to the value of
        `is_internal`.

        Arguments:

        - `is_internal`: Boolean

        """
        self.set('is_internal', str(is_internal).lower())

    is_internal = property(__get_is_internal, __set_is_internal)

    def __get_note (self):
        """Return the text of this note."""
        return self.convert_none_to_text(self.findtext(EATSML + 'note'))

    def __set_note (self, text):
        """Set the text of this note.

        Assumes that the required note element is already present.

        Arguments:

        - `text`: string text of the note

        """
        note_element = self[0]
        note_element.text = text

    note = property(__get_note, __set_note)


class DateElementClass (EATSMLElementBase):

    @property
    def assembled_form (self):
        """Return the assembled form of the date."""
        return self.convert_none_to_text(self.findtext(EATSML + 'assembled_form'))


parser = etree.XMLParser()
parser.set_element_class_lookup(ElementLookup())
