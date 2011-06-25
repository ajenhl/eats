from tmapi.models import Topic

from base_manager import BaseManager


class CalendarManager (BaseManager):

    def get_by_identifier (self, identifier):
        return self.get(identifier__pk=identifier)
    
    def get_query_set (self):
        return super(CalendarManager, self).get_query_set().filter(
            types=self.eats_topic_map.calendar_type)


class Calendar (Topic):

    objects = CalendarManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'
