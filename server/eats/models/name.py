from operator import attrgetter

from tmapi.models import Topic

from .name_cache import NameCache
from .name_element import NameElement
from .name_index import NameIndex
from .name_part import NamePart
from .name_type import NameType

from .base_manager import BaseManager
from eats.lib.name_form import create_name_forms


class NameManager (BaseManager):

    def get_queryset (self):
        return super(NameManager, self).get_queryset().filter(
            types=self.eats_topic_map.name_type)


class Name (Topic, NameElement):

    objects = NameManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    def _add_name_cache (self):
        """Adds this name to the name cache."""
        form = self.assembled_form
        if form:
            assertion = self.assertion
            cached_name = NameCache(
                entity=self.entity, assertion=assertion, name=self,
                form=form, language=self.language, script=self.script,
                authority=self.assertion.authority,
                is_preferred=assertion.is_preferred)
            cached_name.save()

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
            if part:
                indexed_form = NameIndex(entity=self.entity, name=self,
                                         form=part)
                indexed_form.save()

    def _assemble_name_parts (self):
        data = self.get_name_parts()
        form = []
        for name_part_type in self.language.name_part_types:
            form.extend([name_part.display_form for name_part in
                         data.get(name_part_type, [])])
        return self.script.separator.join(form)

    @property
    def assembled_form (self):
        return self.display_form or self._assemble_name_parts()

    @property
    def assertion (self):
        if not hasattr(self, '_assertion'):
            from .name_property_assertion import NamePropertyAssertion
            property_role = self.get_roles_played(
                self.eats_topic_map.property_role_type)[0]
            self._assertion = property_role.get_parent(
                proxy=NamePropertyAssertion)
        return self._assertion

    def create_name_part (self, name_part_type, language, script, display_form,
                          order):
        """Creates a name part associated with this name.

        :param name_part_type: type of the name part
        :type name_part_type: `NamePartType`
        :param language: language of the name part
        :type language: `Language` or None
        :param script: script of the name part
        :type script: `Script` or None
        :param display_form: form of the name part
        :type display_form: `str`
        :param order: order of name part
        :type order: integer
        :rtype: `NamePart`

        """
        # QAZ: This needs to check that the parameters are all
        # associated with the name's authority, by calling
        # self.assertion.authority.validate_components(). name_parts
        # should also be updated through an update method, which calls
        # private individual functions, so that validation can easily
        # take place there also.
        association_type = self.eats_topic_map.name_has_name_part_association_type
        name_role_type = self.eats_topic_map.name_role_type
        association = self.eats_topic_map.create_association(association_type)
        association.create_role(name_role_type, self)
        name_part = self.eats_topic_map.create_topic(proxy=NamePart)
        name_part.add_type(self.eats_topic_map.name_part_type)
        association.create_role(self.eats_topic_map.name_part_role_type,
                                name_part)
        name_part.create_name(display_form, name_part_type)
        language_association = self.eats_topic_map.create_association(
            self.eats_topic_map.is_in_language_type)
        language_association.create_role(
            self.eats_topic_map.name_part_role_type, name_part)
        language_association.create_role(self.eats_topic_map.language_role_type,
                                         language)
        name_part.create_occurrence(self.eats_topic_map.name_part_order_type,
                                    order)
        script_association = self.eats_topic_map.create_association(
            self.eats_topic_map.is_in_script_type)
        script_association.create_role(self.eats_topic_map.name_part_role_type,
                                       name_part)
        script_association.create_role(self.eats_topic_map.script_role_type,
                                       script)
        name_part.update_name_index()
        self.update_name_cache()
        return name_part

    def _delete_name_cache (self):
        """Deletes the cache for this name."""
        try:
            self.cached_name.delete()
        except NameCache.DoesNotExist:
            pass

    def _delete_name_index_forms (self):
        """Deletes the indexed forms of this name."""
        self.indexed_name_forms.filter(name_part__isnull=True).delete()

    @property
    def entity (self):
        """Returns the entity to which this name belongs.

        :rtype: `Entity`

        """
        if not hasattr(self, '_entity'):
            from .entity import Entity
            entity_role = self.assertion.get_roles(
                self.eats_topic_map.entity_role_type)[0]
            self._entity = entity_role.get_player(proxy=Entity)
        return self._entity

    def get_name_parts (self):
        """Returns the name parts associated with this name as a
        dictionary, keyed by name part type.

        :rtype: dictionary

        """
        name_parts = NamePart.objects.filter_by_name(self)
        data = {}
        for name_part in name_parts:
            name_part_type = name_part.name_part_type
            type_data = data.setdefault(name_part_type, [])
            type_data.append(name_part)
        # Sort the name parts into their specified order within type.
        for name_parts in list(data.values()):
            name_parts.sort(key=attrgetter('order'))
        return data

    @property
    def _language_role (self):
        """Returns the language role for this name.

        :rtype: `Role`

        """
        # QAZ: possible index errors.
        name_role = self.get_roles_played(
            self.eats_topic_map.name_role_type,
            self.eats_topic_map.is_in_language_type)[0]
        language_role = name_role.get_parent().get_roles(
            self.eats_topic_map.language_role_type)[0]
        return language_role

    @property
    def name_type (self):
        """Returns the name type of this name.

        :rtype: `NameType`

        """
        return self._get_name().get_type(proxy=NameType)

    @name_type.setter
    def name_type (self, name_type):
        """Sets the name type of this name.

        :param name_type: type of name
        :type name_type: `NameType`

        """
        self._get_name().set_type(name_type)

    def remove (self):
        for name_part in NamePart.objects.filter_by_name(self):
            name_part.remove()
        for role in self.get_roles_played():
            association = role.get_parent()
            association.remove()
        super(Name, self).remove()

    @property
    def _script_role (self):
        """Returns the script role of this name.

        :rtype: `Role`

        """
        # QAZ: possible index errors.
        name_role = self.get_roles_played(
            self.eats_topic_map.name_role_type,
            self.eats_topic_map.is_in_script_type)[0]
        script_role = name_role.get_parent().get_roles(
            self.eats_topic_map.script_role_type)[0]
        return script_role

    def update (self, name_type, language, script, display_form):
        self.name_type = name_type
        self.language = language
        self.script = script
        self.display_form = display_form
        self.update_name_cache()
        self.update_name_index()

    def update_name_cache (self):
        """Updates the name cache for this name."""
        self._delete_name_cache()
        self._add_name_cache()
