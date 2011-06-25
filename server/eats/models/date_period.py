from tmapi.models import Topic

from base_manager import BaseManager


class DatePeriodManager (BaseManager):

    def get_by_identifier (self, identifier):
        return self.get(identifier__pk=identifier)
    
    def get_query_set (self):
        return super(DatePeriodManager, self).get_query_set().filter(
            types=self.eats_topic_map.date_period_type)


class DatePeriod (Topic):

    objects = DatePeriodManager()
    
    class Meta:
        proxy = True
        app_label = 'eats'
