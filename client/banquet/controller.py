"""Controller module for the Banquet GUI."""

__docformat__ = 'restructuredtext'

from textwrap import TextWrapper

import gobject
import gtk
import pango

from gtkmvc import Controller

from constants import AUTHORITY_OBJECT_COLUMN, AUTO_DESELECT_CONFIG_OPTION, \
    AUTO_EDIT_CONFIG_OPTION, CONTEXT_LENGTH_CONFIG_OPTION, \
    CONTEXT_TOOL_URL_CONFIG_OPTION, EATS_SEARCH_RESULTS, \
    EATS_SERVER_CONFIG_SECTION, EATS_SERVER_CONNECTED, \
    EATS_SERVER_CONNECTED_MESSAGE, EATS_SERVER_DISCONNECTED, \
    EATS_SERVER_DISCONNECTED_MESSAGE, EATS_SERVER_HTTP_PASSWORD_CONFIG_OPTION, \
    EATS_SERVER_HTTP_USERNAME_CONFIG_OPTION, EATS_SERVER_PASSWORD_CONFIG_OPTION, \
    EATS_SERVER_URL_CONFIG_OPTION, EATS_SERVER_USERNAME_CONFIG_OPTION, \
    ENTITY_OBJECT_COLUMN, ENTITY_TYPE_AUTHORITY_OBJECT_COLUMN, \
    ENTITY_TYPE_COLUMN, ENTITY_TYPE_NAME_COLUMN, ENTITY_TYPE_OBJECT_COLUMN, \
    FAMILY_NAME_COLUMN, FILE_LOAD_COMPLETE, FILE_LOAD_INTERRUPTED, \
    FILE_OBJECT_COLUMN, GIVEN_NAME_COLUMN, IS_KEYED_COLUMN, \
    LANGUAGE_OBJECT_COLUMN, MARKUP_NOTEBOOK_FILE_PAGE, \
    MARKUP_NOTEBOOK_KEY_PAGE, MARKUP_NOTEBOOK_NAME_PAGE, \
    MARKUP_NOTEBOOK_SELECTION_PAGE, NAME_OBJECT_COLUMN, \
    NAME_TYPE_AUTHORITY_OBJECT_COLUMN, NAME_TYPE_OBJECT_COLUMN, \
    SCRIPT_OBJECT_COLUMN, TOOLS_CONFIG_SECTION
from markup import Name, NameInstance, XMLFile

class MainController (Controller):

    def __init__ (self, model, view):
        super(MainController, self).__init__(model, view)
        self.__progress_bar_file_count = 0
        self.__progress_bar_name_count = 0
        self.__treeviews = {}
        self.__notebook_pages = {}
        self.__connected = False
        return

    def register_view (self, view):
        self.__setup_filelist_treeview()
        self.__setup_lookup_views()
        self.__setup_filters()
        self.__setup_name_treeview()
        self.__setup_file_treeview()
        self.__setup_key_treeview()
        self.__setup_selection_treeview()
        self.__treeviews = {
            self.view['name_treeview']: self.name_markup_filter,
            self.view['file_treeview']: self.file_markup_filter,
            self.view['key_treeview']: self.key_markup_filter}
        self.__notebook_pages = {
            MARKUP_NOTEBOOK_NAME_PAGE: self.view['name_treeview'],
            MARKUP_NOTEBOOK_FILE_PAGE: self.view['file_treeview'],
            MARKUP_NOTEBOOK_KEY_PAGE: self.view['key_treeview'],
            MARKUP_NOTEBOOK_SELECTION_PAGE: self.view['selection_treeview'],
            }
        self.__set_file_filters()
        self.__populate_preferences()
        self.__connect_to_server()

    def __setup_filelist_treeview (self):
        tv = self.view['filelist_treeview']
        tv.set_model(self.model.filelist)
        cell = gtk.CellRendererText()
        col = gtk.TreeViewColumn('Files [unkeyed / keyed]', cell)
        col.set_cell_data_func(cell, self.__render_file_object)
        tv.append_column(col)

    def __setup_lookup_views (self):
        """Tie the various lookup views to their models."""
        self.__setup_lookup_combobox(self.view['authority_combobox'],
                                     self.model.authority_list)
        self.__setup_entity_type_combobox()
        self.__setup_name_type_combobox()
        self.__setup_lookup_combobox(self.view['language_combobox'],
                                     self.model.language_list)
        self.__setup_lookup_combobox(self.view['script_combobox'],
                                     self.model.script_list)
        self.__setup_lookup_result_treeview()

    def __setup_entity_type_combobox (self):
        self.entity_type_filter = self.model.entity_type_list.filter_new()
        self.entity_type_filter.set_visible_func(self.__filter_entity_types)
        self.__setup_lookup_combobox(self.view['entity_type_combobox'],
                                     self.entity_type_filter)

    def __setup_name_type_combobox (self):
        self.name_type_filter = self.model.name_type_list.filter_new()
        self.name_type_filter.set_visible_func(self.__filter_name_types)
        self.__setup_lookup_combobox(self.view['name_type_combobox'],
                                     self.name_type_filter)
        
    def __setup_lookup_combobox (self, view, model):
        """Connect combobox view to model.

        Arguments:

        - `view`: `gtk.ComboBox`
        - `model`: `gtk.ListStore`

        """
        cell = gtk.CellRendererText()
        view.pack_start(cell)
        view.add_attribute(cell, 'text', 1)
        view.set_model(model)

    def __filter_entity_types (self, model, iter):
        """Set the visibility for the row in the entity_type_list
        `model` pointed to by `iter`. Return True if visible.

        Arguments:

        - `model`: gtk.TreeStore
        - `iter`: gtk.TreeIter

        """
        row_authority = model.get_value(
            iter, ENTITY_TYPE_AUTHORITY_OBJECT_COLUMN)
        return self.__filter_by_authority(row_authority)

    def __filter_name_types (self, model, iter):
        """Set the visibility for the row in the name_type_list
        `model` pointed to by `iter`. Return True if visible.

        Arguments:

        - `model`: gtk.TreeStore
        - `iter`: gtk.TreeIter

        """
        row_authority = model.get_value(
            iter, NAME_TYPE_AUTHORITY_OBJECT_COLUMN)
        return self.__filter_by_authority(row_authority)

    def __filter_by_authority (self, type_authority):
        """Return True if `type_authority` is the same as the
        currently selected authority.

        Arguments:

        - `type_authority`: authority element

        """
        visibility = False
        authority_iter = self.view['authority_combobox'].get_active_iter()
        if authority_iter is None:
            authority = None
        else:
            authority = self.model.authority_list.get_value(
                authority_iter, AUTHORITY_OBJECT_COLUMN)
        if authority == type_authority:
            visibility = True
        return visibility
        
    def __setup_lookup_result_treeview (self):
        tv = self.view['lookup_treeview']
        tv.set_model(self.model.resultlist_sort)
        # Column containing main details.
        cell = gtk.CellRendererText()
        cell.set_property('wrap-width', 250)
        cell.set_property('wrap-mode', pango.WRAP_WORD)
        cell.set_property('yalign', 0)
        col = gtk.TreeViewColumn('Entity details', cell)
        col.set_expand(True)
        col.set_property('resizable', True)
        col.set_cell_data_func(cell, self.__render_result_object)
        tv.append_column(col)
        # Column displaying entity type.
        cell = gtk.CellRendererText()
        cell.set_property('yalign', 0)
        col = gtk.TreeViewColumn('Entity type', cell)
        col.set_cell_data_func(cell, self.__render_result_type)
        col.set_property('resizable', True)
        col.set_sort_column_id(ENTITY_TYPE_COLUMN)
        tv.append_column(col)
        # Column displaying given name.
        cell = gtk.CellRendererText()
        cell.set_property('yalign', 0)
        col = gtk.TreeViewColumn('Given name', cell,
                                 markup=GIVEN_NAME_COLUMN)
        col.set_property('resizable', True)
        col.set_sort_column_id(GIVEN_NAME_COLUMN)
        tv.append_column(col)
        # Column displaying family name.
        cell = gtk.CellRendererText()
        cell.set_property('yalign', 0)
        col = gtk.TreeViewColumn('Family name', cell,
                                 markup=FAMILY_NAME_COLUMN)
        col.set_property('resizable', True)
        col.set_sort_column_id(FAMILY_NAME_COLUMN)
        tv.append_column(col)
        selection = tv.get_selection()
        selection.connect('changed', self.on_result_list_selection_changed)

    def __setup_filters (self):
        """Create the `gtk.TreeModelFilter` objects for filtering the
        name markup models."""
        self.name_markup_filter = self.model.name_markup_tree.filter_new()
        self.name_markup_filter.set_visible_func(self.__filter_markup_tree)
        self.file_markup_filter = self.model.file_markup_tree.filter_new()
        self.file_markup_filter.set_visible_func(self.__filter_markup_tree)
        self.key_markup_filter = self.model.key_markup_tree.filter_new()
        self.key_markup_filter.set_visible_func(self.__filter_markup_tree)
        self.selection_markup_filter = self.model.selection_markup_tree.filter_new()
        self.selection_markup_filter.set_visible_func(self.__filter_markup_tree)
        
    def __setup_name_treeview (self):
        """Configure the gtk.TreeView showing name markup with name
        strings as the top level items."""
        treeview = self.view['name_treeview']
        treeview.set_model(self.name_markup_filter)
        self.__setup_markup_treeview(treeview)

    def __setup_file_treeview (self):
        """Configure the gtk.TreeView showing name markup with
        filenames as the top level items."""
        treeview = self.view['file_treeview']
        treeview.set_model(self.file_markup_filter)
        self.__setup_markup_treeview(treeview)

    def __setup_key_treeview (self):
        """Configure the gtk.TreeView showing name markup with name
        keys as the top level items."""
        treeview = self.view['key_treeview']
        treeview.set_model(self.key_markup_filter)
        self.__setup_markup_treeview(treeview)

    def __setup_selection_treeview (self):
        """Configure the `gtk.TreeView` showing all selected
        NameInstance objects."""
        treeview = self.view['selection_treeview']
        treeview.set_model(self.selection_markup_filter)
        self.__setup_markup_treeview(treeview)
        
    def __setup_markup_treeview (self, treeview):
        name_cell = gtk.CellRendererText()
        name_col = gtk.TreeViewColumn('Data', name_cell)
        name_col.set_expand(True)
        name_col.set_resizable(True)
        name_col.set_cell_data_func(name_cell, self.__render_row_object)
        name_cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        treeview.append_column(name_col)
        select_cell = gtk.CellRendererToggle()
        select_cell.connect('toggled', self.on_select_cell_toggled, treeview)
        select_col = gtk.TreeViewColumn('Selected', select_cell, active=0)
        treeview.append_column(select_col)
        selection = treeview.get_selection()
        selection.connect('changed', self.on_selection_changed)
        treeview.connect_after('size-allocate', self.on_treeview_size_allocated, name_col, name_cell)

    def __render_file_object (self, column, cell, model, iter):
        xml_file = model.get_value(iter, FILE_OBJECT_COLUMN)
        text = '%s [%d / %d]' % \
            (xml_file.basename, xml_file.unkeyed_count, xml_file.keyed_count)
        if xml_file.is_modified:
            text = '<i>%s</i>' % text
        if xml_file.unkeyed_count:
            text = '<b>%s</b>' % text
        cell.set_property('markup', text)

    def __render_row_object (self, column, cell, model, iter):
        """Function for rendering a markup treeview cell."""
        row_object = model.get_value(iter, NAME_OBJECT_COLUMN)
        if isinstance(row_object, Name):
            parent_iter = model.iter_parent(iter)
            parent = None
            if parent_iter is not None:
                parent = model.get_value(parent_iter, NAME_OBJECT_COLUMN)
            text = row_object.to_string(parent)
        else:
            text = unicode(row_object)
        cell.set_property('markup', text)

    def __render_result_object (self, column, cell, model, iter):
        """Function for rendering a lookup result."""
        entity = model.get_value(iter, ENTITY_OBJECT_COLUMN)
        preferred_name = entity.get_preferred_name()
        text = '<b>%s</b>' % gobject.markup_escape_text(
            preferred_name.assembled_form)
        entity_url = ''
        text = '%s\n    <i>%s</i>' % (text,
                                      gobject.markup_escape_text(entity_url))
        dates = [date.assembled_form for date in entity.get_existence_dates()]
        date_text = '\n    '.join(dates)
        if date_text:
            text = '%s\n    %s' % (text, gobject.markup_escape_text(date_text))
        cell.set_property('markup', text)

    def __render_result_type (self, column, cell, model, iter):
        """Function for rendering a lookup result entity type."""
        entity_type = model.get_value(iter, ENTITY_TYPE_COLUMN)
        colour = None
        if entity_type == 'place':
            colour = '#daeccd'
        elif entity_type == 'ship':
            colour = '#c6cefd'
        elif entity_type == 'work':
            colour = '#ffcfe7'
        elif entity_type == 'organisation':
            colour = '#fdf7c6'
        elif entity_type == 'person':
            colour = '#e5d4d8'
        cell.set_property('markup', entity_type)
        if colour is None:
            cell.set_property('background-set', False)
        else:
            cell.set_property('background', colour)

    def __filter_markup_tree (self, model, iter):
        """Set the visibility for the row in `model` pointed to by
        `iter`. Return True if visible.

        Arguments:

        - `model`: `gtk.TreeStore`
        - `iter`: `gtk.TreeIter`

        """
        visibility = True
        filter_text = self.view['filter_entry'].get_text().lower()
        if filter_text:
            row_object = model.get_value(iter, NAME_OBJECT_COLUMN)
            if isinstance(row_object, Name):
                filter_text = gobject.markup_escape_text(filter_text)
                visibility = row_object.matches_filter(filter_text)
        return visibility        
        
    def __set_file_filters (self):
        """Add file filters to the open file dialog, since only XML
        files are relevant."""
        xml_file_filter = gtk.FileFilter()
        xml_file_filter.add_mime_type('application/xml')
        xml_file_filter.set_name('XML files')
        # Have an 'all files' filter in case the XML filter does not
        # catch all XML files.
        all_file_filter = gtk.FileFilter()
        all_file_filter.set_name('All files')
        all_file_filter.add_pattern('*')
        self.view['file_open_dialog'].add_filter(all_file_filter)
        self.view['file_open_dialog'].add_filter(xml_file_filter)
        self.view['file_open_dialog'].set_filter(xml_file_filter)

    def __populate_preferences (self):
        """Set the values in the preferences dialogue from the
        configuration file values."""
        config = self.model.config
        server_url = config.get(EATS_SERVER_CONFIG_SECTION,
                                EATS_SERVER_URL_CONFIG_OPTION)
        self.view['server_url_entry'].set_text(server_url)
        username = config.get(EATS_SERVER_CONFIG_SECTION,
                              EATS_SERVER_USERNAME_CONFIG_OPTION)
        self.view['username_entry'].set_text(username)
        password = config.get(EATS_SERVER_CONFIG_SECTION,
                              EATS_SERVER_PASSWORD_CONFIG_OPTION)
        self.view['password_entry'].set_text(password)
        http_username = config.get(EATS_SERVER_CONFIG_SECTION,
                                   EATS_SERVER_HTTP_USERNAME_CONFIG_OPTION)
        self.view['http_username_entry'].set_text(http_username)
        http_password = config.get(EATS_SERVER_CONFIG_SECTION,
                                   EATS_SERVER_HTTP_PASSWORD_CONFIG_OPTION)
        self.view['http_password_entry'].set_text(http_password)
        context_url = config.get(TOOLS_CONFIG_SECTION,
                                 CONTEXT_TOOL_URL_CONFIG_OPTION)
        self.view['context_url_entry'].set_text(context_url)
        context_length = config.getint(TOOLS_CONFIG_SECTION,
                                       CONTEXT_LENGTH_CONFIG_OPTION)
        self.view['context_length_spinbutton'].set_value(context_length)
        auto_edit = config.getboolean(TOOLS_CONFIG_SECTION,
                                      AUTO_EDIT_CONFIG_OPTION)
        self.view['auto_edit_checkbutton'].set_active(auto_edit)
        auto_deselect = config.getboolean(TOOLS_CONFIG_SECTION,
                                          AUTO_DESELECT_CONFIG_OPTION)
        self.view['auto_deselect_checkbutton'].set_active(auto_deselect)

    def __connect_to_server (self):
        """Try connecting to the EATS server."""
        if self.model.set_lookup_base_data():
            self.__set_connected_status()
        else:
            self.__set_disconnected_status()
        self.view['login_to_server_button'].set_sensitive(not(self.__connected))

    def __set_connected_status (self):
        """Set the statusbar message to indicate that the EATS server
        has been successfully connected to."""
        context_id = self.view['statusbar'].get_context_id(
            EATS_SERVER_CONNECTED)
        self.view['statusbar'].pop(context_id)
        self.view['statusbar'].push(context_id, EATS_SERVER_CONNECTED_MESSAGE)
        self.__connected = True

    def __set_disconnected_status (self):
        """Set the statusbar message to indicate that the EATS server
        has not been successfully connected to."""
        context_id = self.view['statusbar'].get_context_id(
            EATS_SERVER_DISCONNECTED)
        self.view['statusbar'].pop(context_id)
        self.view['statusbar'].push(context_id,
                                    EATS_SERVER_DISCONNECTED_MESSAGE)
        self.__connected = False

    def __set_result_status (self):
        """Set the lookup statusbar message to indicate how many
        results were returned by the last search."""
        context_id = self.view['lookup_statusbar'].get_context_id(
            EATS_SEARCH_RESULTS)
        self.view['lookup_statusbar'].pop(context_id)
        count = self.model.result_count
        if count == 1:
            message = '1 matching entity was found.'
        else:
            message = '%d matching entities were found.' % count
        self.view['lookup_statusbar'].push(context_id, message)
    
        
    #############################################
    #
    # Observable properties.
    #

    def property_exception_value_change (self, model, old, new):
        """The model has raised an exception that must be displayed in
        the view."""
        if new:
            if new.has_key('secondary_text'):
                secondary_text = new['secondary_text']
            else:
                secondary_text = unicode(new['exception'])
            self.__show_error_dialog(new['text'], secondary_text)

    def property_file_count_value_change (self, model, old, new):
        """The model has loaded a file, so the progress bar label
        needs to be updated."""
        self.view['progress_bar_label'].set_label(
            'Processing file %d of %d' % (new, self.model.files_total))

    def property_name_count_value_change (self, model, old, new):
        """The model has loaded a name from a file, so the progress
        bar needs to be updated."""
        if self.model.names_total == 0:
            fraction = 0
        else:
            fraction = new / self.model.names_total
        self.view['progress_bar'].set_fraction(fraction)
        self.view['progress_bar'].set_text(
            '%d of %d names' % (new, self.model.names_total))

    def property_file_load_status_value_change (self, model, old, new):
        """The model's file loading status has changed, so the
        progress bar dialog may need altering."""
        if new == FILE_LOAD_COMPLETE:
            self.view['progress_dialog'].hide()
            self.__thaw_treeviews()
        elif new == FILE_LOAD_INTERRUPTED:
            self.view['progress_dialog'].hide()
            self.model.remove_loaded_files()
            self.__thaw_treeviews()


    #############################################
    #
    # Signal handlers.
    #

    def on_main_window_delete_event (self, *args):
        for xml_file in self.model.files.values():
            modified_files = xml_file.is_modified
            if modified_files:
                response = self.view['confirm_quit_dialog'].run()
                if response == gtk.RESPONSE_OK:
                    # Save the files.
                    self.model.save_files()
                    self.model.save_config()
                    gtk.main_quit()
                elif response == gtk.RESPONSE_NO:
                    # Quit without saving.
                    self.model.save_config()
                    gtk.main_quit()
                else:
                    # Don't quit at all.
                    self.view['confirm_quit_dialog'].hide()
                    return True
        self.model.save_config()
        gtk.main_quit()

    def on_quit_menu_item_activate (self, *args):
        self.on_main_window_delete_event()

    def on_about_menu_item_activate (self, *args):
        self.view['about_dialog'].show()

    def on_about_dialog_response (self, dialog, response_id, *args):
        if response_id == gtk.RESPONSE_CANCEL:
            dialog.hide()

    def on_about_dialog_delete_event (self, widget, *args):
        widget.hide()
        return True

    def on_open_menu_item_activate (self, *args):
        self.view['file_open_dialog'].show()

    def on_file_open_dialog_delete_event (self, *args):
        self.on_file_open_dialog_cancel_button_clicked()
        return True

    def on_file_open_dialog_open_button_clicked (self, *args):
        filenames = self.view['file_open_dialog'].get_filenames()
        for treeview in self.__treeviews.keys():
            self.__freeze_treeview(treeview)
        self.view['progress_dialog'].show()
        task = self.model.add_files(filenames)
        gobject.idle_add(task.next)
        self.view['file_open_dialog'].hide()
        self.view['file_open_dialog'].unselect_all()

    def on_file_open_dialog_file_activated (self, *args):
        self.on_file_open_dialog_open_button_clicked()
        
    def on_file_open_dialog_cancel_button_clicked (self, *args):
        self.view['file_open_dialog'].hide()
        self.view['file_open_dialog'].unselect_all()

    def on_progress_dialog_cancel_button_clicked (self, *args):
        self.model.file_load_status = FILE_LOAD_INTERRUPTED

    def on_lookup_window_cancel_button_clicked (self, *args):
        if self.model.config.getboolean(TOOLS_CONFIG_SECTION,
                                        AUTO_DESELECT_CONFIG_OPTION):
            self.model.deselect_all()
        self.__close_lookup_window()

    def on_lookup_window_delete_event (self, *args):
        self.on_lookup_window_cancel_button_clicked()
        return True

    def on_lookup_window_search_button_clicked (self, *args):
        display_name = self.view['display_name_entry'].get_text()
        given_name, family_name, terms_of_address = ('', '', '')
        if self.view['given_name_entry'].get_property('sensitive'):
            given_name = self.view['given_name_entry'].get_text()
            family_name = self.view['family_name_entry'].get_text()
            terms_of_address = self.view['terms_of_address_entry'].get_text()
        search_string = ' '.join((display_name, given_name, family_name,
                                  terms_of_address))
        if search_string:
            self.model.look_up_name(search_string.strip())
            self.__set_result_status()

    def on_lookup_treeview_query_tooltip (self, treeview, x, y, keyboard_mode,
                                          tooltip):
        path_data = treeview.get_path_at_pos(x, y)
        model = treeview.get_model()
        if path_data is None:
            return False
        iter = model.get_iter(path_data[0])
        entity = model.get_value(iter, ENTITY_OBJECT_COLUMN)
        texts = []
        name_text = self.__get_entity_name_text(entity)
        if name_text:
            texts.append('<b>Other names:</b>\n    %s' %
                         gobject.markup_escape_text(name_text))
        note_text = self.__get_entity_note_text(entity)
        if note_text:
            texts.append('<b>Notes:</b>\n    %s' %
                         gobject.markup_escape_text(note_text))
        relationship_text = self.__get_entity_relationship_text(entity)
        if relationship_text:
            texts.append('<b>Relationships:</b>\n    %s' %
                         gobject.markup_escape_text(relationship_text))
        text = '\n\n'.join(texts)
        if text:
            tooltip.set_markup(text)
            return True
        return False

    def on_lookup_treeview_row_activated (self, treeview, path, *args):
        """Use the activated entity to key the selected NameInstances."""
        model = treeview.get_model()
        iter = model.get_iter(path)
        entity = model.get_value(iter, ENTITY_OBJECT_COLUMN)
        data = {}
        data['authority'] = self.__get_combobox_value(
            self.view['authority_combobox'], AUTHORITY_OBJECT_COLUMN)
        data['entity_type'] = self.__get_combobox_value(
            self.view['entity_type_combobox'], ENTITY_TYPE_OBJECT_COLUMN)
        key, entity_type = self.model.get_key_from_entity(entity, data)
        if key is not None:
            if self.__current_entity_type and \
                    self.__current_entity_type != entity_type.name:
                response = self.view['confirm_change_entity_type_dialog'].run()
                self.view['confirm_change_entity_type_dialog'].hide()
                if response != gtk.RESPONSE_YES:
                    return True
            self.model.key_selections(key, entity_type)
            self.__close_lookup_window()
        return True
    
    def on_error_dialog_response (self, dialog, *args):
        dialog.hide()

    def on_error_dialog_delete_event (self, widget, *args):
        widget.hide()
        return True

    def on_warning_dialog_response (self, dialog, *args):
        dialog.hide()

    def on_warning_dialog_delete_event (self, widget, *args):
        widget.hide()
        return True

    def on_filelist_treeview_button_press_event (self, treeview, event):
        """Open the popup menu for a file listed in the filelist
        `gtk.TreeView`."""
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            path_info = treeview.get_path_at_pos(x, y)
            if path_info is not None:
                path, col, cell_x, cell_y = path_info
                file_iter = self.model.filelist.get_iter(path)
                xml_file = self.model.filelist.get_value(
                    file_iter, FILE_OBJECT_COLUMN)
                if xml_file.is_modified:
                    self.view['filelist_save_menu_item'].set_sensitive(True)
                else:
                    self.view['filelist_save_menu_item'].set_sensitive(False)
                treeview.grab_focus()
                treeview.set_cursor(path, col, 0)
                self.view['filelist_popup_menu'].popup(None, None, None,
                                                       event.button, time)
            return True

    def on_filelist_save_menu_item_activate (self, *args):
        selection = self.view['filelist_treeview'].get_selection()
        model, file_iter = selection.get_selected()
        xml_file = model.get_value(file_iter, FILE_OBJECT_COLUMN)
        self.model.save_file(xml_file)
        
    def on_filelist_remove_menu_item_activate (self, *args):
        selection = self.view['filelist_treeview'].get_selection()
        file_iter = selection.get_selected()[1]
        if file_iter:
            xml_file = self.model.get_file_from_iter(file_iter)
            if xml_file.is_modified:
                # Prompt for confirmation of removal, since the file
                # has been modified.
                response_id = self.view['confirm_remove_dialog'].run()
                self.view['confirm_remove_dialog'].hide()
                if response_id == gtk.RESPONSE_YES:
                    self.model.remove_file(xml_file, file_iter)
            else:
                self.model.remove_file(xml_file, file_iter)
        return False

    def on_markup_notebook_switch_page (self, notebook, page, page_num, *args):
        """Set the toolbar buttons' state depending on the selection
        in the switched to page."""
        treeview = self.__notebook_pages[page_num]
        selection = treeview.get_selection()
        self.on_selection_changed(selection)
        return False

    def on_treeview_size_allocated (self, treeview, allocation, column, cell):
        """Change the wrapping for the `cell` in `column` in
        `treeview` to match the new `allocation`."""
        other_cols = (col for col in treeview.get_columns() if col != column)
        new_width = allocation.width - sum(col.get_width() for col in other_cols) * 2
        new_width -= treeview.style_get_property('horizontal-separator') * 2
        if cell.get_property('wrap_width') == new_width or new_width <= 0:
            return
        cell.set_property('wrap_width', new_width)
        store = treeview.get_model()
        if store is None:
            # Resizing the treeview while the first file is being
            # loaded results in store being None.
            return
        iter = store.get_iter_first()
        while iter is not None:
            store.row_changed(store.get_path(iter), iter)
            iter = store.iter_next(iter)
        treeview.set_size_request(0, -1)

    def on_markup_treeview_row_activated (self, treeview, path, column, *args):
        """Expand the activated row."""
        if treeview.row_expanded(path):
            treeview.collapse_row(path)
        else:
            treeview.expand_row(path, False)

    def on_name_treeview_row_expanded (self, treeview, iter, path, *args):
        """Expand the specified row, and its children save those which
        handle keyed names."""
        model = treeview.get_model()
        for i in range(model.iter_n_children(iter)):
            child_iter = model.iter_nth_child(iter, i)
            if not model.get(child_iter, IS_KEYED_COLUMN)[0]:
                path = model.get_path(child_iter)
                treeview.expand_row(path, False)
        return False

    def on_select_cell_toggled (self, cell, path, treeview):
        filter = treeview.get_model()
        filter_iter = filter.get_iter(path)
        is_keyed = filter.get_value(filter_iter, IS_KEYED_COLUMN)
        model = filter.get_model()
        model_iter = filter.convert_iter_to_child_iter(filter_iter)
        self.model.toggle_cell(model, model_iter, not(cell.get_active()),
                               is_keyed)
        return False

    def on_selection_changed (self, selection):
        filter, selected_iter = selection.get_selected()
        self.__set_editing_sensitivity(selected_iter)
        if selected_iter is not None:
            model = filter.get_model()
            # Do not synchronise selections if we are dealing with a
            # selection change in a model that is not the one being
            # viewed (ie, one caused by a selection change in the
            # viewed model).
            page_num = self.view['markup_notebook'].get_current_page()
            treeview = self.__notebook_pages[page_num]
            current_page_model = treeview.get_model().get_model()
            if model == current_page_model:
                model_iter = filter.convert_iter_to_child_iter(selected_iter)
                self.__synchronise_selections(model, model_iter)
        return False
        
    def on_remove_markup_menu_item_activate (self, *args):
        """Remove the name markup from the selected name."""
        self.__remove_markup()

    def on_remove_markup_toolbutton_clicked (self, *args):
        """Remove the name markup from the selected name."""
        self.__remove_markup()

    def on_lookup_name_menu_item_activate (self, *args):
        """Look up the selected name."""
        self.__lookup_name()

    def on_lookup_name_toolbutton_clicked (self, *args):
        """Look up the selected name."""
        self.__lookup_name()

    def on_lookup_window_create_button_clicked (self, *args):
        self.__create_new_entity()
        
    def on_save_menu_item_activate (self, *args):
        """Save all of the currently open files."""
        self.model.save_files()

    def on_filter_entry_changed (self, widget):
        self.name_markup_filter.refilter()
        self.file_markup_filter.refilter()
        self.key_markup_filter.refilter()

    def on_filter_entry_icon_press (self, widget, *args):
        self.view['filter_entry'].set_text('')        

    def on_authority_combobox_changed (self, combobox):
        self.entity_type_filter.refilter()
        self.name_type_filter.refilter()

    def on_entity_type_combobox_changed (self, combobox):
        entity_type = self.__get_combobox_value(combobox,
                                                ENTITY_TYPE_NAME_COLUMN)
        if entity_type is None:
            return False
        current_display_name = self.view['display_name_entry'].get_text()
        if entity_type == 'person':
            self.__set_name_part_entries(current_display_name)
        elif self.view['given_name_entry'].get_property('sensitive'):
            # The previous entity_type selected was "person", so
            # disable sensitivity and reassemble the name from the
            # parts, if there is no display name.
            self.view['terms_of_address_entry'].set_property('sensitive', False)
            self.view['given_name_entry'].set_property('sensitive', False)
            self.view['family_name_entry'].set_property('sensitive', False)
            if not current_display_name:
                display_name = self.__get_name_from_parts()
                self.view['display_name_entry'].set_text(display_name)
            self.view['terms_of_address_entry'].set_text('')
            self.view['given_name_entry'].set_text('')
            self.view['family_name_entry'].set_text('')

    def on_result_list_selection_changed (self, selection):
        model, selected_iter = selection.get_selected()
        sensitivity = True
        if selected_iter is None:
            sensitivity = False
        self.view['edit_toolbutton'].set_sensitive(sensitivity)
        self.view['context_toolbutton'].set_sensitive(sensitivity)

    def on_edit_toolbutton_clicked (self, *args):
        """Open a web browser to edit the selected entity in EATS."""
        entity = self.__get_selected_entity()
        self.model.open_entity_edit(entity.url)

    def on_context_toolbutton_clicked (self, *args):
        """Open a web browser to see the context of the selected
        entity."""
        entity = self.__get_selected_entity()
        self.model.open_entity_context(entity)

    def on_select_all_menu_item_activate (self, *args):
        """Select all `NameInstance` objects."""
        self.model.select_all()

    def on_deselect_all_menu_item_activate (self, *args):
        """Deselect all selected `NameInstance` objects."""
        self.model.deselect_all()

    def on_preferences_menu_item_activate (self, *args):
        self.view['preferences_dialog'].show()
            
    def on_preferences_dialog_delete_event (self, *args):
        self.view['preferences_dialog'].hide()
        return True
            
    def on_preferences_dialog_close_button_clicked (self, *args):
        self.view['preferences_dialog'].hide()

    def on_server_url_entry_changed (self, widget, *args):
        self.model.config.set(EATS_SERVER_CONFIG_SECTION,
                              EATS_SERVER_URL_CONFIG_OPTION,
                              widget.get_text())
        self.view['login_to_server_button'].set_sensitive(True)

    def on_username_entry_changed (self, widget, *args):
        self.model.config.set(EATS_SERVER_CONFIG_SECTION,
                              EATS_SERVER_USERNAME_CONFIG_OPTION,
                              widget.get_text())
        self.view['login_to_server_button'].set_sensitive(True)

    def on_password_entry_changed (self, widget, *args):
        self.model.config.set(EATS_SERVER_CONFIG_SECTION,
                              EATS_SERVER_PASSWORD_CONFIG_OPTION,
                              widget.get_text())
        self.view['login_to_server_button'].set_sensitive(True)

    def on_http_username_entry_changed (self, widget, *args):
        self.model.config.set(EATS_SERVER_CONFIG_SECTION,
                              EATS_SERVER_HTTP_USERNAME_CONFIG_OPTION,
                              widget.get_text())
        self.view['login_to_server_button'].set_sensitive(True)
        
    def on_http_password_entry_changed (self, widget, *args):
        self.model.config.set(EATS_SERVER_CONFIG_SECTION,
                              EATS_SERVER_HTTP_PASSWORD_CONFIG_OPTION,
                              widget.get_text())
        self.view['login_to_server_button'].set_sensitive(True)

    def on_login_to_server_button_clicked (self, button, *args):
        self.__connect_to_server()
        if self.__connected:
            button.set_sensitive(False)

    def on_context_url_entry_changed (self, widget, *args):
        # Since % is a special character in ConfigParser files, escape
        # it.
        text = widget.get_text()
        self.model.config.set(TOOLS_CONFIG_SECTION,
                              CONTEXT_TOOL_URL_CONFIG_OPTION, text)

    def on_context_length_spinbutton_value_changed (self, widget, *args):
        length = widget.get_value_as_int()
        self.model.config.set(TOOLS_CONFIG_SECTION,
                              CONTEXT_LENGTH_CONFIG_OPTION, length)

    def on_auto_edit_checkbutton_toggled (self, button, *args):
        self.model.config.set(TOOLS_CONFIG_SECTION, AUTO_EDIT_CONFIG_OPTION,
                              str(button.get_active()))

    def on_auto_deselect_checkbutton_toggled (self, button, *args):
        self.model.config.set(TOOLS_CONFIG_SECTION, AUTO_DESELECT_CONFIG_OPTION,
                              str(button.get_active()))


    #############################################
    #
    # General methods
    #

    def __show_error_dialog (self, primary_text, secondary_text):
        """Show an error dialog with the specified message.

        Arguments:

        - `primary_text`: string
        - `secondary_text`: string

        """
        self.__show_message_dialog(self.view['error_dialog'], primary_text,
                                   secondary_text)

    def __show_warning_dialog (self, primary_text, secondary_text):
        """Show a warning dialog with the specified message.

        Arguments:

        - `primary_text`: string
        - `secondary_text`: string

        """
        self.__show_message_dialog(self.view['warning_dialog'], primary_text,
                                   secondary_text)

    def __show_message_dialog (self, message_dialog, primary_text,
                               secondary_text):
        """Show `message_dialog` after setting its primary and
        secondary text.

        Arguments:

        - `message_dialog`: `gtk.MessageDialog`
        - `primary_text`: string
        - `secondary_text`: string

        """
        message_dialog.set_markup('<big><b>%s</b></big>' % primary_text)
        message_dialog.format_secondary_text(secondary_text)
        message_dialog.show()

    def __freeze_treeview (self, treeview):
        """Freeze treeview prior to adding many rows to it.

        Arguments:

        - `treeview`: `gtk.TreeView`

        """
        treeview.freeze_child_notify()
        treeview.set_model(None)

    def __thaw_treeviews (self):
        """Thaw the name markup treeviews."""
        for treeview, model in self.__treeviews.items():
            self.__thaw_treeview(treeview, model)
        
    def __thaw_treeview (self, treeview, model):
        """Thaw `treeview` after adding many rows to it.

        Arguments:

        `treeview`: `gtk.TreeView`
        `model`: `gtk.TreeModel`

        """
        treeview.set_model(model)
        treeview.thaw_child_notify()

    def __update_progress_bar (self):
        """Update the file opening progress bar."""
        self.view['progress_bar_label'].set_label(
            '%d of %d files' % (self.__progress_bar_file_count,
                                self.model.file_total))
        self.__progress_bar_name_count += 1.0
        if self.model.name_total == 0:
            fraction = 0
        else:
            fraction = self.__progress_bar_name_count / self.model.name_total
        self.view['progress_bar'].set_fraction(fraction)
        self.view['progress_bar'].set_text('%d of %d names' %
                                           (self.__progress_bar_name_count,
                                            self.model.name_total))

    def __reset_progress_bar (self):
        """Reset the counts on the progress bar."""
        self.__progress_bar_file_count = 0
        self.__progress_bar_name_count = 0

    def __set_editing_sensitivity (self, iter, sensitivity=None):
        """Set the sensitivity of the toolbar and menu items depending
        on whether `iter` is valid or not. If `sensitivity` is supplied,
        this value is used regardless of the `iter`.

        If the EATS server has not been successfully connected to, the
        lookup items will not be sensitive regardless of anything
        else.

        Arguments:

        - `iter`: `gtk.TreeIter`
        - `sensitivity`: Boolean sensitivity

        """
        if sensitivity is None:
            sensitivity = True
            if iter is None or (self.view['lookup_window'].flags() &
                                gtk.VISIBLE):
                sensitivity = False
        lookup_sensitivity = sensitivity
        if not self.__connected:
            lookup_sensitivity = False
        self.view['lookup_name_menu_item'].set_sensitive(lookup_sensitivity)
        self.view['remove_markup_menu_item'].set_sensitive(sensitivity)
        self.view['lookup_name_toolbutton'].set_sensitive(lookup_sensitivity)
        self.view['remove_markup_toolbutton'].set_sensitive(sensitivity)

    def __synchronise_selections (self, model, selected_iter):
        """Synchronise the selections in the name markup models to the
        `selected_iter`, where possible.

        Arguments:

        - `model`: `gtk.TreeStore` containing `selected_iter`
        - `selected_iter`: `gtk.TreeIter` pointing to the selected row

        """
        row_object = model.get_value(selected_iter,
                                     NAME_OBJECT_COLUMN)
        if isinstance(row_object, NameInstance):
            file_iter, name_iter, key_iter, selection_iter = \
                self.model.get_iters_for_name_instance(row_object)
            if model != self.model.file_markup_tree:
                self.__set_related_selection(
                    self.model.file_markup_tree, file_iter,
                    self.view['file_treeview'], self.file_markup_filter)
            if model != self.model.name_markup_tree:
                self.__set_related_selection(
                    self.model.name_markup_tree, name_iter,
                    self.view['name_treeview'], self.name_markup_filter)
            if key_iter is not None and model != self.model.key_markup_tree:
                self.__set_related_selection(
                    self.model.key_markup_tree, key_iter,
                    self.view['key_treeview'], self.key_markup_filter)
            if selection_iter is not None and model != self.model.selection_markup_tree:
                self.__set_related_selection(
                    self.model.selection_markup_tree, selection_iter,
                    self.view['selection_treeview'],
                    self.selection_markup_filter)
        elif model == self.model.name_markup_tree and \
                isinstance(row_object, XMLFile):
            parent_object = self.__get_parent_row_object(model, selected_iter)
            iter = self.model.get_iter_from_ref(self.model.file_markup_tree,
                                                row_object, parent_object)
            self.__set_related_selection(
                self.model.file_markup_tree, iter, self.view['file_treeview'],
                self.file_markup_filter)
        elif model == self.model.file_markup_tree and \
                isinstance(row_object, Name):
            parent_object = self.__get_parent_row_object(model, selected_iter)
            iter = self.model.get_iter_from_ref(self.model.name_markup_tree,
                                                row_object, parent_object)
            self.__set_related_selection(
                self.model.name_markup_tree, iter, self.view['name_treeview'],
                self.name_markup_filter)

    def __get_parent_row_object (self, model, child_iter):
        """Return the RowItem for the parent of `child_iter` in `model`.

        Arguments:

        - `model`: `gtk.TreeStore`
        - `child_iter`: `gtk.TreeIter`

        """
        parent_iter = model.iter_parent(child_iter)
        parent_object = model.get_value(parent_iter,
                                        NAME_OBJECT_COLUMN)
        return parent_object        
            
    def __set_related_selection (self, model, model_iter, treeview, filter):
        """Set the selection in treeview to the row pointed to by iter.

        Arguments:
        
        - `model`: `gtk.TreeStore` that will be selected from
        - `model_iter`: `gtk.TreeIter` of selected row
        - `treeview`: `gtk.TreeView` that will hold the new selection
        - `filter`: `gtk.TreeModelFilter` for `model`

        """
        path = model.get_path(model_iter)
        treeview.expand_to_path(path)
        selection = treeview.get_selection()
        filter_iter = filter.convert_child_iter_to_iter(model_iter)
        selection.select_iter(filter_iter)
        treeview.set_cursor(path)
        treeview.scroll_to_cell(path, None, True, 0.5)

    def __remove_markup (self):
        """Remove name markup from the current selection."""
        model, selected_iter = self.__get_current_selection()
        name_instances = self.model.get_selected_name_instances(
            model, selected_iter)
        # Use a copy of name_instances, since we are modifying it
        # within the loop.
        for name_instance in name_instances[:]:
            self.model.remove_name_markup(name_instance)

    def __lookup_name (self):
        """Look up the currently selected name."""
        model, selected_iter = self.__get_current_selection()
        selected_name_instance = model.get_value(selected_iter,
                                                 NAME_OBJECT_COLUMN)
        name_instances = self.model.get_selected_name_instances(
            model, selected_iter)
        # If there are no NameInstances, the operation is pointless,
        # so don't continue.
        if not name_instances:
            self.__show_error_dialog('The current selection is not checked.',
                                     '')
            return
        # Disable the editing commands while the dialog is open.
        self.__set_editing_sensitivity(None, False)
        # Set the default authority.
        self.view['authority_combobox'].set_active_iter(
            self.model.default_authority_iter)
        # Update the list of valid entity and name types based on the
        # default authority.
        self.name_type_filter.refilter()
        self.entity_type_filter.refilter()
        # Set the defaults for the other comboboxes.
        self.view['language_combobox'].set_active_iter(
            self.model.default_language_iter)
        self.view['script_combobox'].set_active_iter(
            self.model.default_script_iter)
        self.view['name_type_combobox'].set_active(0)
        entity_type, is_unanimous = self.model.get_entity_type(
            selected_name_instance)
        self.__current_entity_type = entity_type
        if not is_unanimous:
            self.__show_warning_dialog(
                'You have selected name instances with differing types.', '')
        name_string = name_instances[0].name.name
        name_string = name_string.replace("'", u'\N{RIGHT SINGLE QUOTATION MARK}')
        # Try to select the entity type in the list that matches the
        # selected instance's entity type.
        if entity_type:
            self.entity_type_filter.foreach(self.__select_matching_entity_type,
                                            entity_type)
        # Clear any existing lookup results.
        self.model.resultlist.clear()
        # Populate the name fields in the lookup dialog.
        if entity_type == 'person':
            self.__set_name_part_entries(name_string)
        else:
            self.view['display_name_entry'].set_text(name_string)
        # Set the focus to the find button.
        self.view['lookup_window_search_button'].grab_focus()
        context_id = self.view['lookup_statusbar'].get_context_id(
            EATS_SEARCH_RESULTS)
        self.view['lookup_statusbar'].pop(context_id)
        self.view['lookup_window'].show()

    def __get_current_selection (self):
        """Return the model and iter for the currently viewed selection."""
        page_num = self.view['markup_notebook'].get_current_page()
        treeview = self.__notebook_pages[page_num]
        model = treeview.get_model()
        selection = treeview.get_selection()
        selected_iter = selection.get_selected()[1]
        return model, selected_iter

    def __set_name_part_entries (self, name):
        """Set the name part entry fields as appropriate for `name`.

        Arguments:
        
        - `name`: string

        """
        # Make the person-specific entry boxes sensitive, and try
        # to populate them with the appropriate parts of the name.
        self.view['terms_of_address_entry'].set_property('sensitive', True)
        self.view['given_name_entry'].set_property('sensitive', True)
        self.view['family_name_entry'].set_property('sensitive', True)
        name_parts = self.model.split_name(name)
        self.view['display_name_entry'].set_text(name_parts['display'])
        self.view['terms_of_address_entry'].set_text(name_parts['terms'])
        self.view['given_name_entry'].set_text(name_parts['given'])
        self.view['family_name_entry'].set_text(name_parts['family'])

    def __get_name_from_parts (self):
        """Return a string of a name compiled from name parts."""
        terms_of_address = self.view['terms_of_address_entry'].get_text()
        given_name = self.view['given_name_entry'].get_text()
        family_name = self.view['family_name_entry'].get_text()
        parts = [part for part in (terms_of_address, given_name, family_name)
                 if part]
        name = ' '.join(parts)
        return name.strip()
        
    def __select_matching_entity_type (self, model, path, iter, entity_type):
        """Select the item in model at path in the entity type
        combobox if it matches entity_type.

        Arguments:

        - `model`: `gtk.TreeModelFilter`
        - `path`: path to current row
        - `iter`: `gtk.TreeIter` pointing to `path`
        - `entity_type`: string entity type to match to

        """
        if model.get_value(iter, ENTITY_TYPE_NAME_COLUMN) == entity_type:
            self.view['entity_type_combobox'].set_active_iter(iter)
            return True
        return False

    def __close_lookup_window (self):
        """Close the lookup name window."""
        self.view['lookup_window'].hide()
        # Reset the name fields.
        self.view['display_name_entry'].set_text('')
        self.view['given_name_entry'].set_text('')
        self.view['family_name_entry'].set_text('')
        self.view['terms_of_address_entry'].set_text('')
        self.view['entity_type_combobox'].set_active(-1)
        # Re-enable the editing commands, if appropriate.
        model, selected_iter = self.__get_current_selection()
        self.__set_editing_sensitivity(selected_iter)

    def __get_selected_entity (self):
        """Return the currently selected entity from the lookup
        results."""
        selection = self.view['lookup_treeview'].get_selection()
        model, iter = selection.get_selected()
        entity = model.get_value(iter, ENTITY_OBJECT_COLUMN)
        return entity

    def __get_entity_name_text (self, entity):
        """Return a string of the text form `entity`'s non-default names.

        Arguments:

        - `entity`: EATSML entity

        """
        name_text = ''
        names = entity.get_names()
        if len(names) > 1:
            preferred_name = entity.get_preferred_name()
            name_text = '\n    '.join([name.assembled_form for name
                                       in names if name != preferred_name])
        return name_text

    def __get_entity_note_text (self, entity):
        """Return a string of `entity`'s notes.

        Arguments:

        - `entity`: EATSML entity

        """
        note_text = ''
        notes = entity.get_notes()
        if notes:
            wrapper = TextWrapper(initial_indent='    ',
                                  subsequent_indent='    ', width=50)
            note_texts = [wrapper.fill(note.text) for note in notes]
            note_text = '\n\n'.join(note_texts)
        return note_text            

    def __get_entity_relationship_text (self, entity):
        """Return a string of the text form of `entity`'s relationships.

        Arguments:

        - `entity`: EATSML entity

        """
        relationship_text = ''
        relationships = entity.get_relationships()
        relationship_texts = [relationship.get_assembled_form()
                              for relationship in relationships]
        if relationship_texts:
            relationship_text = '\n    '.join(relationship_texts)
        return relationship_text

    def __create_new_entity (self):
        """Create a new entity from the details in the lookup form
        fields."""
        data = self.__get_lookup_data()
        # Check that all of the necessary data is supplied.
        missing_data = []
        for data_type in ('entity_type', 'language', 'script', 'authority',
                          'name', 'name_type'):
            if data[data_type] is None:
                missing_data.append(data_type.replace('_', ' '))
        if missing_data:
            self.__show_error_dialog(
                'Missing %s:' % ', '.join(missing_data),
                'In order to create a new entity, a full set of information must be provided.')
            return
        key, entity_type = self.model.create_new_entity(data)
        if key is not None:
            self.model.key_selections(key, entity_type)
            self.__close_lookup_window()

    def __get_lookup_data (self):
        """Return a dictionary of user-supplied data in the lookup
        interface."""
        data = {}
        data['entity_type'] = self.__get_combobox_value(
            self.view['entity_type_combobox'], ENTITY_TYPE_OBJECT_COLUMN)
        data['language'] = self.__get_combobox_value(
            self.view['language_combobox'], LANGUAGE_OBJECT_COLUMN)
        data['script'] = self.__get_combobox_value(
            self.view['script_combobox'], SCRIPT_OBJECT_COLUMN)
        data['authority'] = self.__get_combobox_value(
            self.view['authority_combobox'], AUTHORITY_OBJECT_COLUMN)
        data['name_type'] = self.__get_combobox_value(
            self.view['name_type_combobox'], NAME_TYPE_OBJECT_COLUMN)
        data['display_form'] = self.view['display_name_entry'].get_text()
        data['terms_of_address'] = self.view['terms_of_address_entry'].get_text()
        data['given_name'] = self.view['given_name_entry'].get_text()
        data['family_name'] = self.view['family_name_entry'].get_text()
        data['name'] = None
        if data['display_form'] or data['terms_of_address'] or \
                data['given_name'] or data['family_name']:
            data['name'] = ''
        return data

    def __get_combobox_value (self, combobox, column):
        """Return the value in `column` taken from the selected row in
        `combobox`'s model.

        Arguments:

        - `combobox`: gtk.ComboBox
        - `column`: integer column index

        """
        active_iter = combobox.get_active_iter()
        if active_iter is None:
            return None
        model = combobox.get_model()
        return model.get_value(active_iter, column)
