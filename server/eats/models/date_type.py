from tmapi.models import Topic

from base_manager import BaseManager


class DateTypeManager (BaseManager):

    def get_by_identifier (self, identifier):
        return self.get(identifier__pk=identifier)
    
    def get_query_set (self):
        return super(DateTypeManager, self).get_query_set().filter(
            types=self.eats_topic_map.date_type)


class DateType (Topic):

    objects = DateTypeManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'
