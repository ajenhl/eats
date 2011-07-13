from django.conf.urls.defaults import patterns, url

from eats.models import Authority, Calendar, DatePeriod, DateType, EntityRelationshipType, EntityType, Language, NameType, Script


# Displaying.
urlpatterns = patterns(
    'eats.views.display',
    url(r'^entity/(?P<entity_id>\d+)/$', 'entity_view', name='entity-view'),
    )

# Editing.
urlpatterns += patterns(
    'eats.views.edit',
    url(r'^edit/entity/add/$', 'entity_add', name='entity-add'),
    url(r'^edit/entity/(?P<entity_id>\d+)/$', 'entity_change',
        name='entity-change'),
    url(r'^edit/entity/(?P<entity_id>\d+)/(?P<assertion_id>\d+)/date/add/$',
        'date_add', name='date-add'),
    url(r'^edit/entity/(?P<entity_id>\d+)/(?P<assertion_id>\d+)/date/(?P<date_id>\d+)/$', 'date_change', name='date-change'),
    )

authority_data = {'model': Authority}
calendar_data = {'model': Calendar}
date_period_data = {'model': DatePeriod}
date_type_data = {'model': DateType}
entity_relationship_type_data = {'model': EntityRelationshipType}
entity_type_data = {'model': EntityType}
language_data = {'model': Language}
name_type_data = {'model': NameType}
script_data = {'model': Script}

# Administration.
urlpatterns += patterns(
    'eats.views.admin',
    url(r'^administer/$', 'administration_panel', name='administration-panel'),
    url(r'^administer/create_topic_map/$', 'create_topic_map',
        name='create-topic-map'),
    url(r'^administer/authority/$', 'topic_list', authority_data,
        name='authority-list'),
    url(r'^administer/authority/add/$', 'topic_add', authority_data,
        name='authority-add'),
    url(r'^administer/authority/(?P<topic_id>\d+)/$', 'topic_change',
        authority_data, name='authority-change'),
    url(r'^administer/calendar/$', 'topic_list', calendar_data,
        name='calendar-list'),
    url(r'^administer/calendar/add/$', 'topic_add', calendar_data,
        name='calendar-add'),
    url(r'^administer/calendar/(?P<topic_id>\d+)/$', 'topic_change',
        calendar_data, name='calendar-change'),
    url(r'^administer/date-period/$', 'topic_list', date_period_data,
        name='date-period-list'),
    url(r'^administer/date-period/add/$', 'topic_add',
        date_period_data, name='date-period-add'),
    url(r'^administer/date-period/(?P<topic_id>\d+)/$', 'topic_change',
        date_period_data, name='date-period-change'),
    url(r'^administer/date-type/$', 'topic_list', date_type_data,
        name='date-type-list'),
    url(r'^administer/date-type/add/$', 'topic_add', date_type_data,
        name='date-type-add'),
    url(r'^administer/date-type/(?P<topic_id>\d+)/$', 'topic_change',
        date_type_data, name='date-type-change'),
    url(r'^administer/entity-relationship-type/$', 'topic_list',
        entity_relationship_type_data,
        name='entity-relationship-type-list'),
    url(r'^administer/entity-relationship-type/add/$', 'topic_add',
        entity_relationship_type_data,
        name='entity-relationship-type-add'),
    url(r'^administer/entity-relationship-type/(?P<topic_id>\d+)/$',
        'topic_change', entity_relationship_type_data,
        name='entity-relationship-type-change'),
    url(r'^administer/entity-type/$', 'topic_list', entity_type_data,
        name='entity-type-list'),
    url(r'^administer/entity-type/add/$', 'topic_add',
        entity_type_data, name='entity-type-add'),
    url(r'^administer/entity-type/(?P<topic_id>\d+)/$', 'topic_change',
        entity_type_data, name='entity-type-change'),
    url(r'^administer/language/$', 'topic_list', language_data,
        name='language-list'),
    url(r'^administer/language/add/$', 'topic_add', language_data,
        name='language-add'),
    url(r'^administer/language/(?P<topic_id>\d+)/$', 'topic_change',
        language_data, name='language-change'),
    url(r'^administer/name-type/$', 'topic_list', name_type_data,
        name='name-type-list'),
    url(r'^administer/name-type/add/$', 'topic_add',
        name_type_data, name='name-type-add'),
    url(r'^administer/name-type/(?P<topic_id>\d+)/$', 'topic_change',
        name_type_data, name='name-type-change'),
    url(r'^administer/script/$', 'topic_list', script_data,
        name='script-list'),
    url(r'^administer/script/add/$', 'topic_add', script_data,
        name='script-add'),
    url(r'^administer/script/(?P<topic_id>\d+)/$', 'topic_change',
        script_data, name='script-change'),
    )
