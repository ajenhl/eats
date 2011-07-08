from tmapi.models import Topic

from infrastructure_manager import InfrastructureManager


class CalendarManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_calendar_association_type
        return super(CalendarManager, self).filter_by_authority(
            authority, association_type)
    
    def get_query_set (self):
        return super(CalendarManager, self).get_query_set().filter(
            types=self.eats_topic_map.calendar_type)


class Calendar (Topic):

    objects = CalendarManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'
