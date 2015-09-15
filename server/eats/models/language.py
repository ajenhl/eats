from django.db import transaction

from tmapi.indices import ScopedIndex
from tmapi.models import Topic

from .infrastructure import Infrastructure
from .infrastructure_manager import InfrastructureManager
from .name_part_type import NamePartType


class LanguageManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_language_association_type
        return super(LanguageManager, self).filter_by_authority(
            authority, association_type)

    def get_by_code (self, code):
        for language in self.all():
            if code == language.get_code():
                return language
        else:
            raise self.model.DoesNotExist

    def get_queryset (self):
        return super(LanguageManager, self).get_queryset().filter(
            types=self.eats_topic_map.language_type)


class Language (Topic, Infrastructure):

    objects = LanguageManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    def get_code (self):
        name = self.get_names(self.eats_topic_map.language_code_type)[0]
        return name.get_value()

    @property
    def name_part_types (self):
        """Returns the list of name part types that are associated
        with this language.

        :rtype: list of `NamePartType`s

        """
        index = self.eats_topic_map.get_index(ScopedIndex)
        index.open()
        # QAZ: This might be bleeding the underlying Django database
        # model through too much.
        occurrences = index.get_occurrences(self).filter(type=self.eats_topic_map.name_part_type_order_in_language_type).order_by('value')
        return [occurrence.get_parent(proxy=NamePartType) for occurrence
                in occurrences]

    @name_part_types.setter
    def name_part_types (self, name_part_types):
        """Sets the name part types associated with this language.

        :param name_part_types: the name part types, in display order
        :type name_part_types: list of `NamePartType`s

        """
        index = self.eats_topic_map.get_index(ScopedIndex)
        index.open()
        existing = {}
        for occurrence in index.get_occurrences(self).filter(
            type=self.eats_topic_map.name_part_type_order_in_language_type):
            existing[occurrence.get_parent()] = occurrence
        for index, name_part_type in enumerate(name_part_types):
            if name_part_type in existing:
                existing[name_part_type].set_value(index)
                del existing[name_part_type]
            else:
                name_part_type.create_occurrence(
                    self.eats_topic_map.name_part_type_order_in_language_type,
                    index, scope=[self])
        for occurrence in list(existing.values()):
            occurrence.remove()

    @transaction.atomic
    def remove (self):
        """Deletes this language.

        Automatically deletes any occurrences linking this language to
        name part types. Otherwise, normal topic removal rules apply.

        """
        index = self.eats_topic_map.get_index(ScopedIndex)
        index.open()
        for occurrence in index.get_occurrences(self).filter(
                type=self.eats_topic_map.name_part_type_order_in_language_type):
            occurrence.remove()
        super(Language, self).remove()

    def set_code (self, code):
        if code == self.get_code():
            return
        try:
            self._default_manager.get_by_code(code)
            # QAZ: Raise a specific exception with error message.
            raise Exception
        except self.DoesNotExist:
            pass
        name = self.get_names(self.eats_topic_map.language_code_type)[0]
        name.set_value(code)
