from tmapi.models import Topic

from .infrastructure import Infrastructure
from .infrastructure_manager import InfrastructureManager


class DatePeriodManager (InfrastructureManager):

    def filter_by_authority (self, authority):
        association_type = self.eats_topic_map.authority_has_date_period_association_type
        return super(DatePeriodManager, self).filter_by_authority(
            authority, association_type)

    def get_queryset (self):
        return super(DatePeriodManager, self).get_queryset().filter(
            types=self.eats_topic_map.date_period_type)


class DatePeriod (Topic, Infrastructure):

    objects = DatePeriodManager()

    class Meta:
        proxy = True
        app_label = 'eats'
