from .language import Language
from .script import Script


class NameElement (object):

    """Provides common methods for `Name` and `NamePart` objects."""

    @property
    def display_form (self):
        """Returns the display form of this name.

        :rtype: `str`

        """
        return self._get_name().get_value()

    @display_form.setter
    def display_form (self, value):
        """Sets the display form of this name.

        Note that changing the value via this method does not update
        the name index.

        :param value: value of the name
        :type value: `str`

        """
        self._get_name().set_value(value)

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from .eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map

    def _get_name (self):
        """Returns the TMAPI `Name` associated with this name
        entity."""
        # QAZ: convert a possible IndexError into a more
        # useful/descriptive exception.
        return self.get_names()[0]

    @property
    def language (self):
        """Returns the language of this name.

        :rtype: `Language`

        """
        return self._language_role.get_player(proxy=Language)

    @language.setter
    def language (self, language):
        """Sets the language of this name.

        Note that changing the language via this method does not
        update the name index.

        :param language: language of the name
        :type language: `Language`

        """
        self._language_role.set_player(language)

    @property
    def _language_role (self):
        """Returns the language role for this name.

        :rtype: `Role`

        """
        raise NotImplemented

    @property
    def script (self):
        """Returns the script of this name.

        :rtype: `Script`

        """
        return self._script_role.get_player(proxy=Script)

    @script.setter
    def script (self, script):
        """Sets the script of this name.

        Note that changing the script via this method does not update
        the name index.

        :param script: script of the name
        :type script: `Script`

        """
        self._script_role.set_player(script)

    @property
    def _script_role (self):
        """Returns the script role of this name.

        :rtype: `Role`

        """
        raise NotImplementedError

    def update_name_index (self):
        """Updates the name index forms for this name."""
        self._delete_name_index_forms()
        self._add_name_index()
