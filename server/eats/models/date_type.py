from tmapi.models import Topic

from infrastructure_manager import InfrastructureManager


class DateTypeManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_date_type_association_type
        return super(DateTypeManager, self).filter_by_authority(
            authority, association_type)
    
    def get_query_set (self):
        return super(DateTypeManager, self).get_query_set().filter(
            types=self.eats_topic_map.date_type_type)


class DateType (Topic):

    objects = DateTypeManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'
