from tmapi.models import Topic

from infrastructure_manager import InfrastructureManager


class LanguageManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_language_association_type
        return super(LanguageManager, self).filter_by_authority(
            authority, association_type)
    
    def get_query_set (self):
        return super(LanguageManager, self).get_query_set().filter(
            types=self.eats_topic_map.language_type)


class Language (Topic):

    objects = LanguageManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'
