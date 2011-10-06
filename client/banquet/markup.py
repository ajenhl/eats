"""Module containing classes for the markup objects."""

__docformat__ = 'restructuredtext'

import os

import gobject

from lxml import etree


class RowItem (object):

    """Class for representing objects that serve as row data in the
    various markup TreeStores."""

    def __init__ (self):
        self.__row_ref = None
        self.__child_row_refs = {}

    def __get_row_ref (self):
        """Return the gtk.TreeRowReference for this object."""
        return self.__row_ref

    def __set_row_ref (self, row_ref):
        """Set the `gtk.TreeRowReference` for this object.

        Arguments:

        - `row_ref`: `gtk.TreeRowReference`

        """
        self.__row_ref = row_ref

    row_ref = property(__get_row_ref, __set_row_ref)

    def get_child_row_ref (self, parent):
        """Return the `gtk.TreeRowReference` for this object where it
        is a child of `parent`.

        Arguments:

        - `parent`: `RowItem` object or tuple of `RowItem` and (`RowItem` or string)

        """
        return self.__child_row_refs.get(parent)

    def add_child_row_ref (self, parent, child_row_ref):
        """Set the child `gtk.TreeRowReference` for `parent`.

        Arguments:

        - `parent`:`RowItem` object or tuple of `RowItem` and (`RowItem` or string)
        - `child_row_ref`: `gtk.TreeRowReference`

        """
        self.__child_row_refs[parent] = child_row_ref


class Name (RowItem):

    """Class for representing a name (a particular sequence of
    characters within name markup).

    Objects of this class maintain a mapping of all NameInstances for
    the name, grouped by the XMLFile they are found in.

    """

    def __init__ (self, name):
        """Initialise the Name object.

        Arguments:

        - `name`: string of name

        """
        super(Name, self).__init__()
        self.__name = name
        self.__filter_name = name.lower()
        # Dictionary of NameInstances of this name, keyed by XMLFile.
        self.__unkeyed_instances = {}

    @property
    def name (self):
        """Return the string name."""
        return self.__name

    def add_name_instance (self, name_instance, xml_file):
        """Add `name_instance` to the list of unkeyed NameInstances for
        the name.

        Arguments:

        - `name_instance`: `NameInstance` object
        - `xml_file`: `XMLFile` containing `name_instance`

        """
        if xml_file not in self.__unkeyed_instances:
            self.__unkeyed_instances[xml_file] = []
        if name_instance in self.__unkeyed_instances[xml_file]:
            raise Exception('NameInstance already added to Name')
        else:
            self.__unkeyed_instances[xml_file].append(name_instance)

    def remove_name_instance (self, name_instance, xml_file):
        """Remove name_instance from the list of unkeyed NameInstances
        for the name within xml_file.

        Arguments:

        - `name_instance`: `NameInstance` object
        - `xml_file`: `XMLFile` containing `name_instance`

        """
        self.__unkeyed_instances[xml_file].remove(name_instance)
        if not self.__unkeyed_instances[xml_file]:
            del self.__unkeyed_instances[xml_file]

    def to_string (self, parent):
        """Return a string form of the name for display.

        Arguments:

        - `parent`: `RowItem` object that is the parent of the name in the display context

        """
        text = gobject.markup_escape_text(self.name)
        unkeyed_children = False
        count = 0
        count_string = ''
        if parent is None and len(self.__unkeyed_instances.keys()):
            unkeyed_children = True
            count = sum([len(instances) for instances in self.__unkeyed_instances.values()])
        elif isinstance(parent, XMLFile) and parent in self.__unkeyed_instances:
            unkeyed_children = True
            count = len(self.__unkeyed_instances[parent])
        if unkeyed_children:
            if count > 0:
                count_string = ' [%d]' % count
            text = '<b>%s%s</b>' % (text, count_string)
        return text

    def matches_filter (self, filter_text):
        """Return True if the name contains `filter_text`.

        Arguments:

        - `filter_text`: string of text to filter on

        """
        words = filter_text.split()
        for word in words:
            if word not in self.__filter_name:
                return False
        return True
    
    def __unicode__ (self):
        return self.name


class XMLFile (RowItem):

    """Class for representing an XML file."""

    __convert_to_specific_name_elements_doc = etree.parse('convert_to_specific_name_elements.xsl')
    __convert_to_specific_name_elements = etree.XSLT(__convert_to_specific_name_elements_doc)

    def __init__ (self, filename, xml_tree):
        """Initialise the XMLFile object.

        Arguments:

        - `filename`: string of full path of file
        - `xml_tree`: `lxml.etree.ElementTree` of file's content

        """
        super(XMLFile, self).__init__()
        self.__filename = filename
        self.__basename = os.path.basename(filename)
        self.__tree = xml_tree
        # List of NameInstance objects within this file.
        self.__name_instances = []
        self.__keyed_count = 0
        # gtk.TreeRowReference to the file's place in the filelist model.
        self.__filelist_row_ref = None
        self.__is_modified = False

    @property
    def filename (self):
        """Return the filename of the file."""
        return self.__filename

    @property
    def basename (self):
        """Return the basename of the file."""
        return self.__basename

    @property
    def tree (self):
        """Return the etree.ElementTree of the XML."""
        return self.__tree

    @property
    def name_instances (self):
        """Return a list of the NameInstance objects within the file."""
        return self.__name_instances

    def add_name_instance (self, name_instance):
        """Add name_instance to the list of NameInstances found in this file.

        Arguments:

        - `name_instance`: NameInstance object

        """
        if name_instance in self.__name_instances:
            raise Exception('name_instance has already been added to XMLFile')
        else:
            self.__name_instances.append(name_instance)
            if name_instance.key is not None:
                self.__keyed_count += 1

    def remove_name_instance (self, name_instance):
        """Remove name_instance from the list of NameInstances found
        in this file.

        Arguments:

        - `name_instance`: NameInstance object

        """
        self.__name_instances.remove(name_instance)
        if name_instance.key is not None:
            self.__keyed_count -= 1
        self.is_modified = True

    @property
    def unkeyed_count (self):
        """Return the count of unkeyed NameInstances within the file."""
        return len(self.__name_instances) - self.__keyed_count

    @property
    def keyed_count (self):
        """Return the count of keyed NameInstances within the file."""
        return self.__keyed_count

    @property
    def filelist_row_ref (self):
        """Return the gtk.TreeRowReference for the file in the
        filelist model."""
        return self.__filelist_row_ref

    @filelist_row_ref.setter
    def filelist_row_ref (self, row_ref):
        """Set the `gtk.TreeRowReference` for the file in the filelist model.

        Arguments:

        - `row_ref`: `gtk.TreeRowReference`

        """
        self.__filelist_row_ref = row_ref

    @property
    def is_modified (self):
        """Return Boolean of whether the file has been modified."""
        return self.__is_modified

    @is_modified.setter
    def is_modified (self, is_modified):
        """Set Boolean of whether the file has been modified.

        Arguments:

        - `is_modified`: Boolean

        """
        self.__is_modified = is_modified

    def save (self):
        """Save the XML document, returning True if the file needed to
        be saved, False otherwise."""
        if self.__is_modified:
            fh = open(self.filename, 'w')
            tree = self.__convert_to_specific_name_elements(self.tree)
            tree.write(fh, encoding='utf-8', xml_declaration=True)
            self.__is_modified = False
            return True
        return False
    
    def __unicode__ (self):
        return self.filename


class Key (RowItem):

    """Class for representing a name markup key."""

    def __init__ (self, key):
        """Initialise the Key object.

        Arguments:

        - `key`: string key value

        """
        super(Key, self).__init__()
        self.__key = key

    @property
    def key (self):
        """Return the key value."""
        return self.__key

    def __unicode__ (self):
        return self.key


class NameInstance (object):

    """Class for representing a particular piece of name markup within
    an XML document."""

    def __init__ (self, name, element, xml_file, preceding, following):
        """Initialise the NameInstance object.

        Arguments:

        - `name`: `Name` object of which this is an instance (in a non-OO sense)
        - `element`: `etree.Element` of the name instance
        - `xml_file`: `XMLFile` object containing the name instance
        - `preceding`: string context preceding name
        - `following`: string context following name

        """
        self.__name = name
        self.__element = element
        self.__file = xml_file
        self.__key = None
        self.__entity_type = None
        self.__context = self.__get_name_context(preceding, following)
        self.__row_refs = ()
        self.name.add_name_instance(self, self.file)

    @property
    def name (self):
        """Return the Name object for the instance."""
        return self.__name

    @property
    def element (self):
        """Return the XML element of the instance."""
        return self.__element

    @property
    def file (self):
        """Return the XMLFile object that contains the instance."""
        return self.__file

    @property
    def context (self):
        """Return the textual context of the instance."""
        return self.__context

    @property
    def key (self):
        """Return the Key object that represents the key value of the
        instance, or None if it is not keyed."""
        return self.__key

    @key.setter
    def key (self, key):
        """Set the Key object that represents the key value of the
        instance."""
        if self.__key is None and key is not None:
            self.name.remove_name_instance(self, self.file)
        self.element.set('key', key.key)
        # Remove and re-add the name instance to its containing
        # XMLFile. This has the effect of sorting out keyed/unkeyed,
        # and marking the file as modified. Set the key after removing
        # the instance but before adding so that the count of keyed
        # instances is handled correctly.
        self.file.remove_name_instance(self)
        self.__key = key
        self.file.add_name_instance(self)
        
    def __get_key_value (self):
        """Return the key attribute value of the instance."""
        return self.element.get('key')

    def __set_key_value (self, key_value):
        """Set the key attribute value of the instance.

        Arguments:

        - `key_value`: string

        """
        self.element.set('key', key_value)

    key_value = property(__get_key_value, __set_key_value)

    @property
    def entity_type (self):
        """Return the entity type attribute value of the instance."""
        return self.element.get('type')

    @entity_type.setter
    def entity_type (self, entity_type):
        """Set the entity type attribute value of the instance."""
        if entity_type is None:
            self.element.attrib.pop('type', None)
        else:
            self.element.set('type', entity_type)

    @property
    def row_refs (self):
        """Return the tuple of gtk.TreeRowReferences for the instance."""
        return self.__row_refs

    @row_refs.setter
    def row_refs (self, row_refs):
        """Set the list of gtk.TreeRowReferences for the instance.

        Arguments:

        - `row_refs`: list of `gtk.TreeRowReferences` for file, name, and key
                      `gtk.TreeStores`

        """
        self.__row_refs = row_refs

    def __get_name_context (self, preceding, following):
        """Return textual context of the name element.

        Arguments:

        - `preceding`: string context preceding name
        - `following`: string context following name

        """
        full_context = '%s<b>%s</b>%s' % \
            (preceding, gobject.markup_escape_text(self.__name.name),
             following)
        return full_context

    def dissociate (self):
        """Remove the instance from associations with its XMLFile and
        Name."""
        xml_file = self.file
        xml_file.remove_name_instance(self)
        if self.key is None:
            self.name.remove_name_instance(self, xml_file)

    def __unicode__ (self):
        entity_type = self.entity_type or 'no type'
        return '[<i>%s</i>] %s' % (entity_type, self.context)
