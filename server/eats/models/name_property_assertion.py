from tmapi.models import Association

from base_manager import BaseManager
from name import Name
from name_cache import NameCache
from property_assertion import PropertyAssertion


class NamePropertyAssertionManager (BaseManager):

    def filter_by_entity (self, entity):
        return self.filter(roles__type=self.eats_topic_map.entity_role_type,
                           roles__player=entity)

    def get_preferred (self, entity, authority, language, script):
        """Returns the name for `entity` that best matches
        `authority`, `language`, and `script`.

        The name that best fits first the script (completely
        unreadable names are bad), then the authority, then the
        language, is returned. If there are multiple matches, the
        first name that is set as preferred is returned.

        :param entity: the entity that bears the name
        :type entity: `Entity`
        :param authority: preferred authority to assert the name
        :type authority: `Authority`
        :param language: preferred language of the name
        :type language: `Language`
        :param script: preferred script of the name
        :type script: `Script`
        :rtype: `NamePropertyAssertion` or None
        
        """
        entity_names = NameCache.objects.filter(entity=entity)
        if not entity_names.count():
            raise self.model.DoesNotExist
        if script is not None:
            script_names = entity_names.filter(script=script)
            if not script_names.count():
                script_names = entity_names
        else:
            script_names = entity_names
        if authority is not None:
            authority_names = script_names.filter(authority=authority)
            if not authority_names.count():
                authority_names = script_names
        else:
            authority_names = script_names
        if language is not None:
            language_names = authority_names.filter(language=language)
            if not language_names.count():
                language_names = authority_names
        else:
            language_names = authority_names
        names = language_names.filter(is_preferred=True)
        if not names.count():
            names = language_names
        try:
            return names[0].assertion
        except IndexError:
            raise self.model.DoesNotExist
    
    def get_query_set (self):
        assertion_type = self.eats_topic_map.name_assertion_type
        qs = super(NamePropertyAssertionManager, self).get_query_set()
        return qs.filter(type=assertion_type)


class NamePropertyAssertion (Association, PropertyAssertion):

    objects = NamePropertyAssertionManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def name (self):
        """Returns the name being asserted."""
        if not hasattr(self, '_name'):
            property_role = self.get_roles(
                self.eats_topic_map.property_role_type)[0]
            self._name = property_role.get_player(proxy=Name)
        return self._name

    def remove (self):
        """Deletes this property assertion."""
        self.name.remove()
        super(NamePropertyAssertion, self).remove()
        
    def set_players (self, entity, name):
        """Sets the entity and name involved in this property assertion.

        :param entity: the entity
        :type entity: `Entity`
        :param name: the name
        :type name: `Name`

        """
        if hasattr(self, '_entity') or hasattr(self, '_name'):
            raise Exception(
                'set_players may be called only once for a property assertion')
        self.create_role(self.eats_topic_map.property_role_type, name)
        self._name = name
        self.create_role(self.eats_topic_map.entity_role_type, entity)
        self._entity = entity
        name._entity = entity
        
    def update (self, name_type, language, script, display_form, is_preferred):
        """Updates this property assertion, and its associated name.

        :param name_type: type of the name
        :type name_type: `Topic`
        :param language: language of the name
        :type language: `Topic`
        :param script: script of the name
        :type script: `Topic`
        :param display_form: display form of the name
        :type display_form: unicode string
        :param is_preferred: if the name is a preferred form
        :type is_preferred: `Boolean`

        """
        self.authority.validate_components(language=language, script=script,
                                           name_type=name_type)
        self.name.update(name_type, language, script, display_form)
        self.is_preferred = is_preferred
