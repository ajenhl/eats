from tmapi.models import Topic

from .base_manager import BaseManager
from .name_element import NameElement
from .name_index import NameIndex
from .name_part_type import NamePartType

from eats.lib.name_form import create_name_forms


class NamePartManager (BaseManager):

    def filter_by_name (self, name):
        association_type = self.eats_topic_map.name_has_name_part_association_type
        name_role_type = self.eats_topic_map.name_role_type
        name_part_role_type = self.eats_topic_map.name_part_role_type
        return self.filter(
            roles__type=name_part_role_type,
            roles__association__type=association_type,
            roles__association__roles__type=name_role_type,
            roles__association__roles__player=name)

    def get_queryset (self):
        return super(NamePartManager, self).get_queryset().filter(
            types=self.eats_topic_map.name_part_type)


class NamePart (Topic, NameElement):

    objects = NamePartManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    def _add_name_index (self):
        """Adds the forms of this name to the name index."""
        parts = []
        language_code = self.language.get_code()
        script_code = self.script.get_code()
        name_forms = create_name_forms(self.display_form, language_code,
                                       script_code)
        for name in name_forms:
            parts.extend(name.split())
        for part in set(parts):
            indexed_form = NameIndex(entity=self.name.entity, name=self.name,
                                     name_part=self, form=part)
            indexed_form.save()

    def _delete_name_index_forms (self):
        """Deletes the indexed forms of this name."""
        self.indexed_name_part_forms.all().delete()

    @property
    def _language_role (self):
        """Returns the language role for this name.

        :rtype: `Role`

        """
        # QAZ: possible index errors.
        name_role = self.get_roles_played(
            self.eats_topic_map.name_part_role_type,
            self.eats_topic_map.is_in_language_type)[0]
        language_role = name_role.get_parent().get_roles(
            self.eats_topic_map.language_role_type)[0]
        return language_role

    @property
    def name (self):
        """Returns the name that this is a name part of.

        :rtype: `Name`

        """
        if not hasattr(self, '_name'):
            from .name import Name
            name_part_role = self.get_roles_played(
                self.eats_topic_map.name_part_role_type,
                self.eats_topic_map.name_has_name_part_association_type)[0]
            association = name_part_role.get_parent()
            name_role = association.get_roles(
                self.eats_topic_map.name_role_type)[0]
            self._name = name_role.get_player(proxy=Name)
        return self._name

    @property
    def name_part_type (self):
        """Returns the name part type of this name.

        :rtype: `NamePartType`

        """
        return self._get_name().get_type(proxy=NamePartType)

    @name_part_type.setter
    def name_part_type (self, name_part_type):
        """Sets the name part type of this name part.

        :param name_part_type: type of name part
        :type name_type: `NamePartType`

        """
        self._get_name().set_type(name_part_type)

    @property
    def order (self):
        """Returns the order of this name part.

        :rtype: integer

        """
        return self._order_occurrence.get_value()

    @order.setter
    def order (self, order):
        """Sets the order of this name part.

        :param order: order
        :type order: integer

        """
        self._order_occurrence.set_value(order)

    @property
    def _order_occurrence (self):
        """Returns the order occurrence for this name part.

        :rtype: `Occurrence`

        """
        occurrence_type = self.eats_topic_map.name_part_order_type
        try:
            occurrence = self.get_occurrences(occurrence_type)[0]
        except IndexError:
            occurrence = self.create_occurrence(occurrence_type, 1)
        return occurrence

    def remove (self):
        # self.name will raise an exception if it has not been called
        # before this method and after the association is deleted, so
        # get a local reference to the name.
        name = self.name
        for role in self.get_roles_played():
            association = role.get_parent()
            association.remove()
        name.update_name_cache()
        super(NamePart, self).remove()

    @property
    def _script_role (self):
        """Returns the script role of this name.

        :rtype: `Role`

        """
        # QAZ: possible index errors.
        name_role = self.get_roles_played(
            self.eats_topic_map.name_part_role_type,
            self.eats_topic_map.is_in_script_type)[0]
        script_role = name_role.get_parent().get_roles(
            self.eats_topic_map.script_role_type)[0]
        return script_role
