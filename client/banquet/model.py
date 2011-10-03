"""Model module for the Banquet application."""

__docformat__ = 'restructuredtext'

import ConfigParser
import os.path
import webbrowser

import gtk
import gobject
from gtkmvc.model import Model
from lxml import etree

from constants import AUTO_DESELECT_CONFIG_OPTION, AUTO_EDIT_CONFIG_OPTION, \
    BANQUET_CONFIG_FILEPATH, CONTEXT_LENGTH_CONFIG_OPTION, \
    CONTEXT_TOOL_URL_CONFIG_OPTION, EATS_SERVER_CONFIG_SECTION, \
    EATS_SERVER_HTTP_PASSWORD_CONFIG_OPTION, \
    EATS_SERVER_HTTP_USERNAME_CONFIG_OPTION, \
    EATS_SERVER_PASSWORD_CONFIG_OPTION, EATS_SERVER_URL_CONFIG_OPTION, \
    EATS_SERVER_USERNAME_CONFIG_OPTION, FILE_LOAD_COMPLETE, \
    FILE_LOAD_INACTIVE, FILE_LOAD_INTERRUPTED, FILE_OBJECT_COLUMN, \
    IS_KEYED_COLUMN, IS_SELECTED_COLUMN, NAME_INSTANCE_CONTEXT_CHARS, \
    NAME_OBJECT_COLUMN, TEI_NSMAP, TEI_USES_SPECIFIC_NAME_ELEMENTS, \
    TOOLS_CONFIG_SECTION
from markup import Name, XMLFile, Key, NameInstance
from eatsml.dispatcher import Dispatcher

class MainModel (Model):

    exception = {}
    file_count = 0
    name_count = 0
    file_load_status = FILE_LOAD_INACTIVE
    __observables__ = ('exception', 'file_count', 'name_count', 'file_load_status')

    __get_name_context_doc = etree.parse('get-name-context.xsl')
    __get_name_context = etree.XSLT(__get_name_context_doc)
    __tidy_name_context_doc = etree.parse('tidy-name-context.xsl')
    __tidy_name_context = etree.XSLT(__tidy_name_context_doc)
    __convert_from_specific_name_elements_doc = etree.parse('convert_from_specific_name_elements.xsl')
    __convert_from_specific_name_elements = etree.XSLT(__convert_from_specific_name_elements_doc)
    __get_name_nodes = etree.XPath('//*[self::tei:name or self::tei:rs]',
                                   namespaces=TEI_NSMAP)
    __get_first_preceding_sibling = etree.XPath('preceding-sibling::*[1]')

    def __init__ (self):
        super(MainModel, self).__init__()
        self.__parser = etree.XMLParser(load_dtd=True)
        # TreeStore for files:
        #   XMLFile object
        self.filelist = gtk.ListStore(gobject.TYPE_PYOBJECT)
        # TreeStores for name markup:
        #   Boolean marker of whether an item is selected (for group operations)
        #   Row data object
        #   Boolean marker of whether an item is a key-type item
        self.name_markup_tree = gtk.TreeStore(
            gobject.TYPE_BOOLEAN, gobject.TYPE_PYOBJECT, gobject.TYPE_BOOLEAN)
        self.file_markup_tree = gtk.TreeStore(
            gobject.TYPE_BOOLEAN, gobject.TYPE_PYOBJECT, gobject.TYPE_BOOLEAN)
        self.key_markup_tree = gtk.TreeStore(
            gobject.TYPE_BOOLEAN, gobject.TYPE_PYOBJECT, gobject.TYPE_BOOLEAN)
        self.selection_markup_tree = gtk.TreeStore(
            gobject.TYPE_BOOLEAN, gobject.TYPE_PYOBJECT, gobject.TYPE_BOOLEAN)
        self.name_markup_tree.set_default_sort_func(None)
        self.file_markup_tree.set_default_sort_func(None)
        self.key_markup_tree.set_default_sort_func(None)
        self.selection_markup_tree.set_default_sort_func(None)
        # Dictionary of open files. Keys are file paths, values are
        # File objects.
        self.files = {}
        # Dictionary of names. Keys are name strings, values are Name
        # objects.
        self.__names = {}
        # Dictionary of name keys. Keys are name keys, values are Key
        # objects.
        self.__keys = {}
        # Count of files loaded in the current load.
        self.file_count = 0
        # Count of names loaded in the current load.
        self.name_count = 0
        # List of gtk.TreeIters for files loaded in the last
        # (interrupted) load.
        self.__loaded_file_iters = []
        # ListStore for authorities:
        #   Authority object
        #   Authority name
        self.authority_list = gtk.ListStore(gobject.TYPE_PYOBJECT, str)
        # ListStore for entity types:
        #   Entity type object
        #   Entity type name
        #   Authority object
        self.entity_type_list = gtk.ListStore(gobject.TYPE_PYOBJECT, str,
                                              gobject.TYPE_PYOBJECT)
        # ListStore for name types:
        #   Name type object
        #   Name type name
        #   Authority object
        self.name_type_list = gtk.ListStore(gobject.TYPE_PYOBJECT, str,
                                            gobject.TYPE_PYOBJECT)
        # ListStore for languages:
        #   Language object
        #   Language name
        #   Authority object
        self.language_list = gtk.ListStore(gobject.TYPE_PYOBJECT, str,
                                           gobject.TYPE_PYOBJECT)
        # ListStore for scripts:
        #   Script object
        #   Script name
        #   Authority object
        self.script_list = gtk.ListStore(gobject.TYPE_PYOBJECT, str,
                                         gobject.TYPE_PYOBJECT)
        # ListStore for lookup results:
        #   Entity result object
        #   Entity type
        #   Given name
        #   Family name
        self.resultlist = gtk.ListStore(gobject.TYPE_PYOBJECT, str, str, str)
        self.resultlist_sort = gtk.TreeModelSort(self.resultlist)
        self.result_count = 0
        self.config = self.__initialise_preferences()
        self.__dispatcher = None

    def __initialise_preferences (self):
        """Load the user preferences."""
        config = ConfigParser.RawConfigParser()
        config_filename = os.path.expanduser(BANQUET_CONFIG_FILEPATH)
        config.read(config_filename)
        self.__create_config_section(config, EATS_SERVER_CONFIG_SECTION)
        self.__create_config_section(config, TOOLS_CONFIG_SECTION)
        self.__create_config_option(config, EATS_SERVER_CONFIG_SECTION,
                                    EATS_SERVER_URL_CONFIG_OPTION, '')
        self.__create_config_option(config, EATS_SERVER_CONFIG_SECTION,
                                    EATS_SERVER_USERNAME_CONFIG_OPTION, '')
        self.__create_config_option(config, EATS_SERVER_CONFIG_SECTION,
                                    EATS_SERVER_PASSWORD_CONFIG_OPTION, '')
        self.__create_config_option(config, EATS_SERVER_CONFIG_SECTION,
                                    EATS_SERVER_HTTP_USERNAME_CONFIG_OPTION, '')
        self.__create_config_option(config, EATS_SERVER_CONFIG_SECTION,
                                    EATS_SERVER_HTTP_PASSWORD_CONFIG_OPTION, '')
        self.__create_config_option(config, TOOLS_CONFIG_SECTION,
                                    CONTEXT_TOOL_URL_CONFIG_OPTION, '')
        self.__create_config_option(config, TOOLS_CONFIG_SECTION,
                                    CONTEXT_LENGTH_CONFIG_OPTION,
                                    NAME_INSTANCE_CONTEXT_CHARS)
        self.__create_config_option(config, TOOLS_CONFIG_SECTION,
                                    AUTO_EDIT_CONFIG_OPTION, 'False')
        self.__create_config_option(config, TOOLS_CONFIG_SECTION,
                                    AUTO_DESELECT_CONFIG_OPTION, 'False')
        self.__create_config_option(config, TOOLS_CONFIG_SECTION,
                                    TEI_USES_SPECIFIC_NAME_ELEMENTS, 'False')
        return config

    def __create_config_section (self, config, section_name):
        """Create a section in the configuration with `section_name`
        if such a section does not already exist.

        Arguments:

        - `config`: ConfigParser.SafeConfigParser object
        - `section_name`: string

        """
        if not config.has_section(section_name):
            config.add_section(section_name)

    def __create_config_option (self, config, section_name, option_name, value):
        """Create an option in the configuration with `option_name` in
        section `section_name`.

        Arguments:

        - `config`: ConfigParser.SafeConfigParser object
        - `section_name`: string
        - `option_name`: string
        - `value`: string, int, float or Boolean default value

        """
        if not config.has_option(section_name, option_name):
            config.set(section_name, option_name, value)

    def __get_dispatcher (self):
        server_url = self.config.get(EATS_SERVER_CONFIG_SECTION,
                                     EATS_SERVER_URL_CONFIG_OPTION)
        username = self.config.get(EATS_SERVER_CONFIG_SECTION,
                                   EATS_SERVER_USERNAME_CONFIG_OPTION)
        password = self.config.get(EATS_SERVER_CONFIG_SECTION,
                                   EATS_SERVER_PASSWORD_CONFIG_OPTION)
        http_username = self.config.get(EATS_SERVER_CONFIG_SECTION,
                                        EATS_SERVER_HTTP_USERNAME_CONFIG_OPTION)
        http_password = self.config.get(EATS_SERVER_CONFIG_SECTION,
                                        EATS_SERVER_HTTP_PASSWORD_CONFIG_OPTION)
        if not http_username:
            http_username = http_password = None
        dispatcher = Dispatcher(server_url, username, password, http_username,
                                http_password)
        return dispatcher
        
    def set_lookup_base_data (self):
        """Set the base data for the lookup window - entity types,
        languages and scripts defined in the EATS server.

        Return True if no errors were encountered connecting to and
        retrieving data from the EATS server.

        """
        self.__dispatcher = self.__get_dispatcher()
        try:
            self.__dispatcher.login()
        except Exception, err:
            self.exception = {
                'text': 'Encountered the following error trying to log in to the EATS server',
                'exception': err}
            return False
        try:
            eatsml = self.__dispatcher.get_base_document()
        except Exception, err:
            self.exception = {
                'text': 'Encountered the following error retrieving base EATS data',
                'exception': err}
            return False
        self.authority_list.clear()
        self.entity_type_list.clear()
        self.language_list.clear()
        self.script_list.clear()
        for authority in eatsml.get_authorities():
            row_iter = self.authority_list.append([authority, authority.name])
            if authority.user_preferred:
                self.default_authority_iter = row_iter
                self.__default_authority = authority
            for entity_type in authority.get_entity_types():
                self.entity_type_list.append([entity_type, entity_type.name,
                                              authority])
            for name_type in authority.get_name_types():
                row_iter = self.name_type_list.append(
                    [name_type, name_type.name, authority])
            for language in authority.get_languages():
                row_iter = self.language_list.append([language, language.name,
                                                      authority])
                if language.user_preferred:
                    self.default_language_iter = row_iter
            for script in authority.get_scripts():
                row_iter = self.script_list.append([script, script.name,
                                                    authority])
                if script.user_preferred:
                    self.default_script_iter = row_iter
        self.__name_part_types = {}
        self.__name_part_types['terms_of_address'] = eatsml.get_name_part_type(
            'terms of address')
        self.__name_part_types['given_name'] = eatsml.get_name_part_type(
            'given')
        self.__name_part_types['family_name'] = eatsml.get_name_part_type(
            'family')
        return True
        
    def add_files (self, filenames):
        """Add filenames to filelist ListStore."""
        self.__loaded_file_iters = []
        self.file_load_status = FILE_LOAD_INACTIVE
        self.files_total = len(filenames)
        self.file_count = 0
        context_length = self.config.getint(TOOLS_CONFIG_SECTION,
                                            CONTEXT_LENGTH_CONFIG_OPTION)
        for filename in filenames:
            self.file_count += 1
            self.name_count = 0
            if filename not in self.files:
                if self.file_load_status == FILE_LOAD_INTERRUPTED:
                    yield False
                else:
                    yield True
                try:
                    xml_tree = self.__parse_file(filename)
                    interim_context_tree = self.__get_name_context(
                        xml_tree, context_length="%d" % (context_length))
                    context_tree = self.__tidy_name_context(
                        interim_context_tree)
                except Exception, err:
                    self.exception = {
                        'text': 'Could not add file %s:' % filename,
                        'exception': err}
                    continue
                xml_file = XMLFile(filename, xml_tree)
                self.files[filename] = xml_file
                file_iter = self.filelist.append([xml_file])
                xml_file.filelist_row_ref = self.__get_ref_from_iter(
                    self.filelist, file_iter)
                self.__loaded_file_iters.append(file_iter)
                name_nodes = self.__get_name_nodes(xml_tree)
                context_root = context_tree.getroot()
                self.names_total = len(name_nodes)
                # Add a top-level file item.
                self.__get_root_iter(xml_file, self.file_markup_tree)
                for i in range(len(name_nodes)):
                    # This check must come before adding a name, or
                    # else cancelling may/will leave behind a stray
                    # name.
                    if self.file_load_status == FILE_LOAD_INTERRUPTED:
                        yield False
                    name_node = name_nodes[i]
                    context_node = context_root[i]
                    self.__add_name_to_stores(xml_file, name_node,
                                              context_node)
                    yield True
                xml_file.is_modified = False
                file_path = self.filelist.get_path(file_iter)
                self.filelist.emit('row-changed', file_path, file_iter)
        self.file_load_status = FILE_LOAD_COMPLETE
        yield False

    def __parse_file (self, filename):
        """Return the lxml ElementTree generated from parsing
        `filename`."""
        tree = etree.parse(filename, self.__parser)
        tree = self.__convert_from_specific_name_elements(tree)
        return tree
        
    def __add_name_to_stores (self, xml_file, name_node, context_node):
        """Add name_node to the various gtk.TreeStores.

        Arguments:
        
        - `xml_file`: XMLFile object containing name_node
        - `name_node`: `lxml.etree.Element`
        - `context_node`: `lxml.etree.Element` of context for name

        """
        name_string = context_node.find('name').text
        normalised_name = self.__normalise_name(name_string)
        name = self.__names.setdefault(normalised_name, Name(name_string))
        # Get/add a name item to the file item.
        file_name_iter = self.__get_child_iter(xml_file, name,
                                               self.file_markup_tree)
        # Get/add a top-level name item.
        self.__get_root_iter(name, self.name_markup_tree)
        # Get/add a file item to the name item.
        name_file_iter = self.__get_child_iter(name, xml_file,
                                               self.name_markup_tree)
        # Get the preceding and following context.
        preceding = gobject.markup_escape_text(
            context_node.find('preceding').text or '')
        following = gobject.markup_escape_text(
            context_node.find('following').text or '')
        name_instance = NameInstance(name, name_node, xml_file, preceding,
                                     following)
        xml_file.add_name_instance(name_instance)
        name_key = name_instance.key_value
        if name_key is None:
            # Add a name instance item to the file/name item.
            file_instance_iter = self.file_markup_tree.append(
                file_name_iter, [False, name_instance, False])
            # Add a name instance item to the name/file item.
            name_instance_iter = self.name_markup_tree.append(
                name_file_iter, [False, name_instance, False])
            key_instance_iter = None
        else:
            file_instance_iter, name_instance_iter, key_instance_iter = self.__add_keyed_name_instance(name_instance, name, name_key, xml_file, file_name_iter, name_file_iter)
        name_instance.row_refs = (
            self.__get_ref_from_iter(self.file_markup_tree, file_instance_iter),
            self.__get_ref_from_iter(self.name_markup_tree, name_instance_iter),
            self.__get_ref_from_iter(self.key_markup_tree, key_instance_iter),
            None)
        self.name_count += 1.0

    def __normalise_name (self, name):
        """Return a normalised form of name."""
        return name.title()

    def __add_keyed_name_instance (self, name_instance, name, name_key,
                                   xml_file, file_name_iter, name_file_iter):
        # Get/add a keyed item to the file/name item.
        file_keyed_iter = self.__get_keyed_iter(file_name_iter, xml_file,
                                                name, self.file_markup_tree)
        # Get/add a keyed item to the name/file item.
        name_keyed_iter = self.__get_keyed_iter(
            name_file_iter, name, xml_file, self.name_markup_tree)
        key = self.__keys.setdefault(name_key, Key(name_key))
        # Get/add a top-level key item.
        self.__get_root_iter(key, self.key_markup_tree, True)
        # Get/add a file item to the key item.
        key_file_iter = self.__get_child_iter(key, xml_file,
                                              self.key_markup_tree, True)
        # Get/add a key item to the file/name item.
        file_key_iter = self.__get_key_iter(
            file_keyed_iter, name_key, xml_file, name,
            self.file_markup_tree)
        # Get/add a key item to the name/file item.
        name_key_iter = self.__get_key_iter(
            name_keyed_iter, name_key, name, xml_file,
            self.name_markup_tree)
        # Add a name instance item to the file/name/key item.
        file_instance_iter = self.file_markup_tree.append(
            file_key_iter, [False, name_instance, True])
        # Add a name instance item to the name/file/key item.
        name_instance_iter = self.name_markup_tree.append(
            name_key_iter, [False, name_instance, True])
        # Add a name instance item to the key/file item.
        key_instance_iter = self.key_markup_tree.append(
            key_file_iter, [False, name_instance, True])
        name_instance.key = key
        return file_instance_iter, name_instance_iter, key_instance_iter
    
    def get_iter_from_ref (self, tree_store, parent, child_key=None):
        """Return a `gtk.TreeIter` or None for parent (or child of parent).

        Arguments:

        - `tree_store`: `gtk.TreeStore`
        - `parent`: RowItem
        - `child_key`: RowItem or tuple of RowItem and (RowItem or string)

        """
        if child_key is None:
            row_ref = parent.row_ref
        else:
            row_ref = parent.get_child_row_ref(child_key)
        if row_ref is None:
            return None
        path = row_ref.get_path()
        if path is None:
            return None
        else:
            return tree_store.get_iter(path)

    def __get_ref_from_iter (self, tree_store, item_iter):
        """Return a `gtk.TreeRowReference` corresponding to
        `item_iter` within `tree_store`.

        Arguments:

        - `tree_store`: `gtk.TreeStore`
        - `item_iter`: `gtk.TreeIter`

        """
        ref = None
        if item_iter is not None:
            path = tree_store.get_path(item_iter)
            ref = gtk.TreeRowReference(tree_store, path)
        return ref

    def __get_root_iter (self, row_item, tree_store, is_keyed=False):
        """Return a `gtk.TreeIter` pointing to the root row for row_item
        in tree_store.

        The row is added if it doesn't already exist.

        Arguments:

        - `row_item`: RowItem
        - `tree_store`: `gtk.TreeStore`
        - `is_keyed`: Boolean value for if the row represents a keyed name

        """
        item_iter = self.get_iter_from_ref(tree_store, row_item)
        if item_iter is None:
            item_iter = tree_store.append(
                None, [False, row_item, is_keyed])
            row_item.row_ref = self.__get_ref_from_iter(tree_store, item_iter)
        return item_iter

    def __get_child_iter (self, parent, child, tree_store, is_keyed=False):
        """Return a gtk.TreeIter pointing to the row for child of
        parent in tree_store.

        The row is added if it doesn't already exist.

        Arguments:

        - `parent`: RowItem
        - `child`: RowItem
        - `tree_store`: `gtk.TreeStore`
        - `is_keyed`: Boolean value for if the row represents a keyed name

        """
        child_iter = self.get_iter_from_ref(tree_store, parent, child)
        if child_iter is None:
            parent_iter = self.get_iter_from_ref(tree_store, parent)
            child_iter = tree_store.append(
                parent_iter, [False, child, is_keyed])
            row_ref = self.__get_ref_from_iter(tree_store, child_iter)
            parent.add_child_row_ref(child, row_ref)
        return child_iter

    def __get_keyed_iter (self, parent_iter, root_item, parent_item,
                          tree_store):
        """Return a `gtk.TreeIter` pointing to the row for keyed name
        elements that is a child of the row pointed to by `parent_iter`,
        in tree_store.

        The row is added if it doesn't already exist.

        Arguments:

        - `parent_iter`: `gtk.TreeIter` pointing to the parent row
        - `root_item`: RowItem at the root of the tree
        - `parent_item`: RowItem of the parent
        - `tree_store`: `gtk.TreeStore`

        """
        keyed_iter = self.get_iter_from_ref(tree_store, root_item,
                                            (parent_item, 'key'))
        if keyed_iter is None:
            keyed_iter = tree_store.insert(
                parent_iter, 0, [False, 'Keyed names', True])
            root_item.add_child_row_ref(
                (parent_item, 'key'),
                self.__get_ref_from_iter(tree_store, keyed_iter))
        return keyed_iter

    def __get_key_iter (self, keyed_iter, key, root_item, parent_item,
                        tree_store):
        """Return a `gtk.TreeIter` pointing to the row for key within
        tree_store.

        The row is added if it doesn't already exist.

        Arguments:

        - `keyed_iter`: `gtk.TreeIter` of the parent row
        - `key`: Key object
        - `root_item`: RowItem of root item
        - `parent_item`: RowItem of root's child
        - `tree_store`: `gtk.TreeStore`

        """
        key_iter = self.get_iter_from_ref(tree_store, root_item,
                                          (parent_item, key))
        if key_iter is None:
            key_iter = tree_store.append(
                keyed_iter, [False, key, True])
            root_item.add_child_row_ref(
                (parent_item, key),
                self.__get_ref_from_iter(tree_store, key_iter))
        return key_iter

    def remove_loaded_files (self):
        """Remove the files loaded in the last (interrupted) load."""
        for file_iter in self.__loaded_file_iters:
            xml_file = self.get_file_from_iter(file_iter)
            self.remove_file(xml_file, file_iter)

    def get_file_from_iter (self, file_iter):
        """Return the XMLFile pointed to by `file_iter`.

        Arguments:

        - `file_iter`: `gtk.TreeIter` within the filelist `gtk.ListStore`

        """
        xml_file = self.filelist.get_value(file_iter,
                                           FILE_OBJECT_COLUMN)
        return xml_file

    def remove_file (self, xml_file, file_iter):
        """Remove the file `xml_file`.

        Arguments:
        
        - `xml_file`: XMLFile to be removed
        - `file_iter`: `gtk.TreeIter` pointing to the row in the
          filelist `gtk.ListStore` for `xml_file`

        """
        for name_instance in xml_file.name_instances[:]:
            # Use a copy of the list of NameInstances, due to the
            # deletion removing items from that list.
            self.__delete_name_instance(name_instance)
        del self.files[xml_file.filename]
        self.filelist.remove(file_iter)

    def __select_name_instance (self, name_instance):
        """Add `name_instance` to the selections `gtk.TreeStore`, and
        mark it as selected in the other markup `gtk.TreeStore`s.

        Arguments:

        - `name_instance`: `NameInstance` object

        """
        file_iter, name_iter, key_iter, selection_iter = \
            self.get_iters_for_name_instance(name_instance)
        if selection_iter is None:
            selection_iter = self.selection_markup_tree.append(
                None, (True, name_instance, False))
            row_refs = list(name_instance.row_refs)
            row_refs[3] = self.__get_ref_from_iter(self.selection_markup_tree,
                                                   selection_iter)
            name_instance.row_refs = tuple(row_refs)
            self.name_markup_tree.set_value(name_iter, IS_SELECTED_COLUMN, True)
            self.file_markup_tree.set_value(file_iter, IS_SELECTED_COLUMN, True)
            if key_iter is not None:
                self.key_markup_tree.set_value(key_iter, IS_SELECTED_COLUMN,
                                               True)
                
    def __deselect_name_instance (self, name_instance):
        """Remove `name_instance` from the selections `gtk.TreeStore`,
        and mark it as unselected in the other markup
        `gtk.TreeStore`s.

        Arguments:

        - `name_instance`: `NameInstance` object
        
        """
        file_iter, name_iter, key_iter, selection_iter = \
            self.get_iters_for_name_instance(name_instance)
        if selection_iter is not None:
            self.selection_markup_tree.remove(selection_iter)
            row_refs = list(name_instance.row_refs)
            row_refs[3] = None
            name_instance.row_refs = tuple(row_refs)
        self.__toggle_cell_reverse(self.file_markup_tree, file_iter)
        self.__toggle_cell_reverse(self.name_markup_tree, name_iter)
        if key_iter is not None:
            self.__toggle_cell_reverse(self.key_markup_tree, key_iter)
                
    def toggle_cell (self, model, parent_iter, value, toggle_keys=False):
        """Set the checkbox at parent_iter to value, and do the same for all
        of its descendant checkboxes.

        Only toggles keyed items if toggle_keys is True.

        Arguments:
        
        - `model`: `gtk.TreeModel` containing parent_iter
        - `parent_iter`: `gtk.TreeIter`
        - `value`: Boolean value to set checkbox to
        - `toggle_keys`: Boolean indicator of whether to toggle items
           that are marked as being keyed

        """
        if toggle_keys or not model.get_value(parent_iter, IS_KEYED_COLUMN):
            model.set_value(parent_iter, IS_SELECTED_COLUMN, value)
            for n in range(model.iter_n_children(parent_iter)):
                child_iter = model.iter_nth_child(parent_iter, n)
                self.toggle_cell(model, child_iter, value, toggle_keys)
            row_object = model.get_value(parent_iter, NAME_OBJECT_COLUMN)
            if isinstance(row_object, NameInstance):
                # Add or remove this NameInstance from the list of
                # selected instances.
                if value:
                    self.__select_name_instance(row_object)
                else:
                    self.__deselect_name_instance(row_object)

    def __toggle_cell_reverse (self, model, child_iter):
        """Set the checkbox at child_iter to False, and do the same
        for all of its ancestor checkboxes.

        Indeed, this is one-directional toggling.

        Arguments:

        - `model`: gtk.TreeModel` containing `child_iter`
        - `child_iter`: `gtk.TreeIter`

        """
        if child_iter is not None:
            is_selected = model.get_value(child_iter, IS_SELECTED_COLUMN)
            if is_selected:
                model.set_value(child_iter, IS_SELECTED_COLUMN, False)
            parent_iter = model.iter_parent(child_iter)
            self.__toggle_cell_reverse(model, parent_iter)

    def remove_name_markup (self, name_instance):
        """Remove name markup from name_instance.

        Arguments:

        - `name_instance`: NameInstance

        """
        try:
            self.__remove_name_markup(name_instance.element)
            self.__delete_name_instance(name_instance)
        except Exception, err:
            self.exception = {
                'text': 'Failed to remove name markup',
                'exception': err}

    def __delete_name_instance (self, name_instance):
        """Delete `name_instance`.

        Arguments:
        
        - `name_instance`: NameInstance object

        """
        self.__remove_name_instance_from_treestores(name_instance)
        name_instance.dissociate()
        row_ref = name_instance.file.filelist_row_ref
        self.__notify_filelist_changed(row_ref)
        del name_instance

    def __remove_name_instance_from_treestores (self, name_instance):
        """Remove `name_instance` from the markup gtk.TreeStores.

        Arguments:

        - `name_instance`: NameInstance

        """
        self.__deselect_name_instance(name_instance)
        file_iter, name_iter, key_iter, selection_iter = \
            self.get_iters_for_name_instance(name_instance)
        self.__remove_iter(self.file_markup_tree, file_iter)
        self.__remove_iter(self.name_markup_tree, name_iter)
        if key_iter is not None:
            self.__remove_iter(self.key_markup_tree, key_iter)
        name_instance.row_refs = (None, None, None, None)

    def get_iters_for_name_instance (self, name_instance):
        """Return a tuple of `gtk.TreeIter`s corresponding to the
        `gtk.TreeRowReference`s of `name_instance`.

        Arguments:

        - `name_instance`: `NameInstance` object

        """
        paths = []
        key_iter = selection_iter = None
        for row_ref in name_instance.row_refs:
            if row_ref is None:
                paths.append(None)
            else:
                paths.append(row_ref.get_path())
        file_iter = self.file_markup_tree.get_iter(paths[0])
        name_iter = self.name_markup_tree.get_iter(paths[1])
        if paths[2] is not None:
            key_iter = self.key_markup_tree.get_iter(paths[2])
        if paths[3] is not None:
            selection_iter = self.selection_markup_tree.get_iter(paths[3])
        return (file_iter, name_iter, key_iter, selection_iter)
        
    def __remove_name_markup (self, name):
        """Remove name markup from name element.

        That is, incorporate the content of the name element into the
        document, removing the element.

        """
        parent = name.getparent()
        # QAZ: If parent is None, then this is the root node, and
        # removing the markup here is going to result in an invalid
        # XML file.
        try:
            previous_sibling = self.__get_first_preceding_sibling(name)[0]
        except IndexError:
            previous_sibling = None
        # Handle the text of the name.
        if previous_sibling is not None:
            previous_sibling.tail = self.__concatenate_text(
                previous_sibling.tail, name.text)
        else:
            parent.text = self.__concatenate_text(parent.text, name.text)
        # Handle the tail of the name.
        if len(name):
            name[-1].tail = self.__concatenate_text(name[-1].tail, name.tail)
        elif previous_sibling is not None:
            previous_sibling.tail = self.__concatenate_text(previous_sibling.tail, name.tail)
        else:
            parent.text = self.__concatenate_text(parent.text, name.tail)
        # Handle the children of the name.
        name_index = parent.index(name)
        children = name[:]
        children.reverse()
        for child in children:
            parent.insert(name_index, child)
        # Remove the now empty name element.
        parent.remove(name)

    @staticmethod
    def __concatenate_text (base_text, added_text):
        """Return base_text concatenated with added_text, where each
        of the arguments may be None."""
        if base_text is None:
            return added_text
        if added_text is None:
            return base_text
        return base_text + added_text

    def __remove_iter (self, model, child_iter):
        """Remove `child_iter` from `model`, and recurse up to the parent
        if `child_iter` is the only child.

        Arguments:
        
        - `model`: `gtk.TreeStore` containing `child_iter`
        - `child_iter`: `gtk.TreeIter`

        """
        if child_iter is not None:
            parent_iter = model.iter_parent(child_iter)
            model.remove(child_iter)
            if parent_iter is not None and not \
                    model.iter_has_child(parent_iter):
                self.__remove_iter(model, parent_iter)

    def __notify_filelist_changed (self, row_ref):
        """Emit a row-changed signal for the row in filelist
        `gtk.ListStore` pointed to by row_ref, so that the updated
        count of NameInstances will be shown.

        Arguments:
        
        - `row_ref`: `gtk.TreeRowReference`

        """
        path = row_ref.get_path()
        iter = self.filelist.get_iter(path)
        self.filelist.emit('row-changed', path, iter)

    def save_files (self):
        """Save all open files."""
        for xml_file in self.files.values():
            self.save_file(xml_file)

    def save_file (self, xml_file):
        """Save `xml_file`.

        Arguments:
        
        - `xml_file`: XMLFile to be saved

        """
        try:
            saved = xml_file.save()
        except Exception, err:
            self.exception = {
                'text': 'Could not save file %s' % xml_file.filename,
                'exception': err}
        if saved:
            self.__notify_filelist_changed(xml_file.filelist_row_ref)

    def save_config (self):
        """Save the configuration."""
        filename = os.path.expanduser(BANQUET_CONFIG_FILEPATH)
        config_file = open(filename, 'w')
        self.config.write(config_file)

    def get_selected_name_instances (self, model, row_iter):
        """Return a list of selected NameInstance objects, unless
        `row_iter` points to an unchecked row, in which case return
        an empty list.

        Arguments:

        - `model`: `gtk.TreeModelFilter`
        - `row_item`: RowItem or NameInstance object

        """
        is_checked = model.get_value(row_iter, IS_SELECTED_COLUMN)
        if is_checked:
            return self.__get_selected_name_instances()
        return []

    def __get_selected_name_instances (self):
        """Return a list of selected `NameInstance` objects."""
        selections = []
        tree_iter = self.selection_markup_tree.get_iter_first()
        while tree_iter is not None:
            selections.append(self.selection_markup_tree.get_value(
                    tree_iter, NAME_OBJECT_COLUMN))
            tree_iter = self.selection_markup_tree.iter_next(tree_iter)
        return selections
    
    def get_entity_type (self, row_item):
        """Return the string entity type of row_item, or the unanimous
        entity_type, or else an empty string. Also return True if all
        of the entity types for the selected items are the same
        (ignoring empty entity types).

        Arguments:

        - `row_item`: RowItem or NameInstance

        """
        entity_types = set([instance.entity_type for instance in
                            self.__get_selected_name_instances() if
                            instance.entity_type is not None])
        entity_type = ''
        is_unanimous = False
        if isinstance(row_item, NameInstance):
            entity_type = row_item.entity_type or ''
        if len(entity_types) == 1:
            entity_type = entity_types.pop() or ''
            is_unanimous = True
        elif len(entity_types) == 0:
            is_unanimous = True
        return entity_type, is_unanimous

    def look_up_name (self, name):
        """Look up name in EATS.

        Arguments:

        - `name`: search string

        """
        self.resultlist.clear()
        try:
            eatsml = self.__dispatcher.look_up_name(name)
        except Exception, err:
            self.exception = {
                'text': 'Encountered the following error looking up name "%s"' \
                    % name,
                'exception': err}
            return
        entities = eatsml.get_entities()
        self.result_count = len(entities)
        if not entities:
            return
        for entity in entities:
            entity_types = []
            if len(entity_types):
                entity_type = unicode(entity_types[0])
            else:
                entity_type = ''
            name = entity.get_preferred_name()
            given_name = family_name = ''
            if name is not None:
                given_name = name.get_name_part(
                    self.__name_part_types['given_name'])
                family_name = name.get_name_part(
                    self.__name_part_types['family_name'])
            self.resultlist.append([entity, entity_type,
                                    given_name, family_name])

    def get_edit_url (self, entity):
        """Return the full URL for the edit page for entity.

        Arguments:

        - `entity`: `etree.Element` of the EATSML entity

        """
        url = self.__dispatcher.get_edit_url(entity)
        return url

    def get_context_urls (self, entity):
        """Return a list of full URLs for the context page for entity.

        The context uses an AuthorityRecord's ID.

        Arguments:

        - `entity`: `lxml.etree.Element` of the EATSML entity

        """
        context_url = self.config.get(TOOLS_CONFIG_SECTION,
                                      CONTEXT_TOOL_URL_CONFIG_OPTION)
        urls = []
        records = entity.get_default_authority_records()
        for record in records:
            url = context_url % record.system_id
            urls.append(url)
        return urls

    def select_all (self):
        """Select all `NameInstance` objects."""
        name_iter = self.name_markup_tree.get_iter_first()
        while name_iter is not None:
            self.toggle_cell(self.name_markup_tree, name_iter, True)
            name_iter = self.name_markup_tree.iter_next(name_iter)

    def deselect_all (self):
        """Deselect all currently selected `NameInstance` objects."""
        for name_instance in self.__get_selected_name_instances():
            self.__deselect_name_instance(name_instance)
    
    def key_selections (self, key, entity_type):
        """Add `key` and `entity_type` to the currently selected
        NameInstances.

        Arguments:

        - `key`: string
        - `entity_type`: entity type element

        """
        entity_type_value = entity_type.name
        # Iterate over a copy of the selected NameInstance objects,
        # since that list is being modified within the loop.
        for name_instance in self.__get_selected_name_instances():
            self.__deselect_name_instance(name_instance)
            name_instance.entity_type = entity_type_value
            if key != name_instance.key_value:
                self.__move_name_instance(name_instance, key)
        return True

    def get_key_from_entity (self, entity, data):
        """Return the key and entity type from `entity`.

        Arguments:

        - `entity`: `lxml.etree.Element` of the EATSML entity
        - `data`: dictionary of user-provided lookup data

        """
        key = entity.url
        entity_types = entity.get_preferred_entity_types(data['authority'])
        if entity_types:
            print entity_types
            entity_type = entity_types[0]
        else:
            entity_type = data['entity_type']
        return key, entity_type

    def __add_existence (self, entity, data):
        """Create an existence and entity type for `entity`, and
        return the system ID of the authority record associated with
        the new existence.

        Arguments:

        - `entity`: `lxml.etree.Element` of an EATSML entity
        - `data`: dictionary of user-provided lookup data

        """
        doc = self.__dispatcher.get_base_document_copy()
        new_entity = doc.create_entity(id=entity.id, eats_id=entity.eats_id)
        new_entity.create_existence(id='new_existence_assertion')
        new_entity.create_entity_type(id='new_entity_type_assertion',
                                      entity_type=data['entity_type'])
        message = 'Added %s existence and entity type to entity %s.' % \
            (data['authority'].name, entity.eats_id)
        try:
            url = self.__dispatcher.import_document(doc, message)
        except Exception, err:
            self.exception = {
                'text': 'Encountered the following error trying to create an existence and entity type for the entity:',
                'exception': err}
            return None
        try:
            eatsml = self.__dispatcher.get_processed_import(url)
        except Exception, err:
            self.exception = {
                'text': 'Encountered the following error trying to get the new details for the entity:',
                'exception': err}
            return None
        entity = eatsml.get_entities()[0]
        key, entity_type = self.get_key_from_entity(entity, data)
        return key, entity_type

    def __move_name_instance (self, name_instance, key):
        """Remove `name_instance` from the markup treeviews and add it
        again as keyed with `key`.

        Arguments:

        - `name_instance`: NameInstance object
        - `key`: string

        """
        self.__remove_name_instance_from_treestores(name_instance)
        name = name_instance.name
        xml_file = name_instance.file
        # Get/add a top-level name item.
        self.__get_root_iter(name, self.name_markup_tree)
        # Get/add a top-level file item.
        self.__get_root_iter(xml_file, self.file_markup_tree)
        file_name_iter = self.__get_child_iter(xml_file, name,
                                               self.file_markup_tree)
        name_file_iter = self.__get_child_iter(name, xml_file,
                                               self.name_markup_tree)
        file_instance_iter, name_instance_iter, key_instance_iter = \
            self.__add_keyed_name_instance(name_instance, name, key, xml_file,
                                           file_name_iter, name_file_iter)
        name_instance.row_refs = (
            self.__get_ref_from_iter(self.file_markup_tree, file_instance_iter),
            self.__get_ref_from_iter(self.name_markup_tree, name_instance_iter),
            self.__get_ref_from_iter(self.key_markup_tree, key_instance_iter),
            None)
        self.__notify_filelist_changed(xml_file.filelist_row_ref)

    def split_name (self, name):
        """Return name split into a dictionary of parts, keyed by
        "display", "terms", "given" and "family".

        Arguments:

        - `name`: string

        """
        name_parts = {'display': '', 'terms': '', 'given': '',
                      'family': ''}
        if not name:
            return name_parts
        parts = name.split(',')
        number_parts = len(parts)
        if number_parts == 1:
            parts = name.split()
            if len(parts) == 1:
                name_parts['family'] = parts[0]
            else:
                name_parts['given'] = ' '.join(parts[:-1])
                name_parts['family'] = parts[-1]
        elif number_parts == 2:
            name_parts['family'] = parts[0].strip()
            name_parts['given'] = parts[1].strip()
        else:
            name_parts['display'] = name.strip()
        return name_parts

    def create_new_entity (self, data):
        """Create a new entity in EATS, using the information in
        `data`. Return the system ID of the authority record
        associated with the new entity, or None if the creation
        failed.

        Arguments:

        - `data`: dictionary of entity data

        """
        doc = self.__dispatcher.get_base_document_copy()
        authority = data['authority']
        entity = doc.create_entity(xml_id='new_entity')
        entity.create_existence(xml_id='new_existence_assertion',
                                authority=authority)
        entity.create_entity_type(
            xml_id='new_entity_type_assertion', authority=authority,
            entity_type=data['entity_type'])
        name = entity.create_name(
            xml_id='new_name_assertion', authority=authority,
            name_type=data['name_type'], is_preferred=True)
        name.language = data['language']
        name.script = data['script']
        name.display_form = data['display_form']
        for name_part_type in ('terms_of_address', 'given_name', 'family_name'):
            if data[name_part_type]:
                name.create_name_part(self.__name_part_types[name_part_type],
                                      data[name_part_type])
        message_name = data['display_form']
        if not message_name:
            message_name = ' '.join([data['given_name'], data['family_name']]).strip()
        message = 'Created new entity "%s" from lookup.' % message_name
        try:
            url = self.__dispatcher.import_document(doc, message)
        except Exception, err:
            self.exception = {
                'text': 'Encountered the following error trying to create a new entity:',
                'exception': err}
            return None
        try:
            eatsml = self.__dispatcher.get_processed_import(url)
        except Exception, err:
            self.exception = {
                'text': 'Encountered the following error trying to get the details for the new entity. However, the new entity was created, so do not try creating it again!',
                'exception': err}
            return None
        entity = eatsml.get_entities()[0]
        key, entity_type = self.get_key_from_entity(entity, data)
        if self.config.getboolean(TOOLS_CONFIG_SECTION,
                                  AUTO_EDIT_CONFIG_OPTION):
            self.open_entity_edit(entity)
        return key, entity_type

    def open_entity_edit (self, entity):
        """Open the webpage for editing `entity`.

        Arguments:

        - `entity`: entity element

        """
        url = self.get_edit_url(entity)
        webbrowser.open(url)

    def open_entity_context (self, entity):
        """Open the webpage for `entity`'s context.

        Arguments:

        - `entity`: entity element

        """
        urls = self.get_context_urls(entity)
        for url in urls:
            webbrowser.open(url)
