from django.conf.urls import patterns, url

from eats.models import Authority, Calendar, DatePeriod, DateType, EntityRelationshipType, EntityType, Language, NamePartType, NameType, Script


# Displaying.
urlpatterns = patterns(
    'eats.views.display',
    url(r'^$', 'home', name='home'),
    url(r'^entity/(?P<entity_id>\d+)/$', 'entity_view', name='entity-view'),
    url(r'^entity/(?P<entity_id>\d+)/eatsml/', 'entity_eatsml_view',
        name='entity-eatsml-view'),
    url(r'^search/$', 'search', name='search'),
    url(r'^search/eatsml/$', 'search_eatsml', name='search-eatsml'),
    url(r'^statistics/$', 'statistics', name='statistics'),
    )

# Editing.
urlpatterns += patterns(
    'eats.views.edit',
    url(r'^entity/add/$', 'entity_add', name='entity-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/$', 'entity_change',
        name='entity-change'),
    url(r'^entity/(?P<entity_id>\d+)/delete/$', 'entity_delete',
        name='entity-delete'),
    url(r'^entity/(?P<entity_id>\d+)/merge/$', 'entity_merge',
        name='entity-merge'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/add/$',
        'date_add', name='date-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/(?P<date_id>\d+)/$', 'date_change', name='date-change'),
    url(r'^export/eatsml/base/$', 'export_eatsml_base',
        name='export-eatsml-base'),
    url(r'^export/eatsml/entities/$', 'export_eatsml_entities',
        name='export-eatsml-entities'),
    url(r'^export/eatsml/entities/entity_type/(?P<entity_type_id>\d+)/$',
        'export_eatsml_entities_by_entity_type',
        name='export-eatsml-entities-by-entity-type'),
    url(r'^export/eatsml/full/$', 'export_eatsml_full',
        name='export_eatsml_full'),
    url(r'^import/$', 'import_eatsml', name='import-eatsml'),
    url(r'^import/(?P<import_id>\d+)/$', 'display_eatsml_import',
        name='display-eatsml-import'),
    url(r'^import/(?P<import_id>\d+)/raw/$', 'display_eatsml_import_raw',
        name='display-eatsml-import-raw'),
    url(r'^import/(?P<import_id>\d+)/annotated/$',
        'display_eatsml_import_annotated',
        name='display-eatsml-import-annotated'),
    )

authority_data = {'model': Authority}
calendar_data = {'model': Calendar}
date_period_data = {'model': DatePeriod}
date_type_data = {'model': DateType}
entity_relationship_type_data = {'model': EntityRelationshipType}
entity_type_data = {'model': EntityType}
language_data = {'model': Language}
name_part_type_data = {'model': NamePartType}
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
        name='dateperiod-list'),
    url(r'^administer/date-period/add/$', 'topic_add',
        date_period_data, name='dateperiod-add'),
    url(r'^administer/date-period/(?P<topic_id>\d+)/$', 'topic_change',
        date_period_data, name='dateperiod-change'),
    url(r'^administer/date-type/$', 'topic_list', date_type_data,
        name='datetype-list'),
    url(r'^administer/date-type/add/$', 'topic_add', date_type_data,
        name='datetype-add'),
    url(r'^administer/date-type/(?P<topic_id>\d+)/$', 'topic_change',
        date_type_data, name='datetype-change'),
    url(r'^administer/entity-relationship-type/$', 'topic_list',
        entity_relationship_type_data, name='entityrelationshiptype-list'),
    url(r'^administer/entity-relationship-type/add/$', 'topic_add',
        entity_relationship_type_data, name='entityrelationshiptype-add'),
    url(r'^administer/entity-relationship-type/(?P<topic_id>\d+)/$',
        'topic_change', entity_relationship_type_data,
        name='entityrelationshiptype-change'),
    url(r'^administer/entity-type/$', 'topic_list', entity_type_data,
        name='entitytype-list'),
    url(r'^administer/entity-type/add/$', 'topic_add',
        entity_type_data, name='entitytype-add'),
    url(r'^administer/entity-type/(?P<topic_id>\d+)/$', 'topic_change',
        entity_type_data, name='entitytype-change'),
    url(r'^administer/language/$', 'topic_list', language_data,
        name='language-list'),
    url(r'^administer/language/add/$', 'topic_add', language_data,
        name='language-add'),
    url(r'^administer/language/(?P<topic_id>\d+)/$', 'topic_change',
        language_data, name='language-change'),
    url(r'^administer/name-part-type/$', 'topic_list', name_part_type_data,
        name='nameparttype-list'),
    url(r'^administer/name-part-type/add/$', 'topic_add',
        name_part_type_data, name='nameparttype-add'),
    url(r'^administer/name-part-type/(?P<topic_id>\d+)/$', 'topic_change',
        name_part_type_data, name='nameparttype-change'),
    url(r'^administer/name-type/$', 'topic_list', name_type_data,
        name='nametype-list'),
    url(r'^administer/name-type/add/$', 'topic_add',
        name_type_data, name='nametype-add'),
    url(r'^administer/name-type/(?P<topic_id>\d+)/$', 'topic_change',
        name_type_data, name='nametype-change'),
    url(r'^administer/script/$', 'topic_list', script_data,
        name='script-list'),
    url(r'^administer/script/add/$', 'topic_add', script_data,
        name='script-add'),
    url(r'^administer/script/(?P<topic_id>\d+)/$', 'topic_change',
        script_data, name='script-change'),
    url(r'^administer/user/$', 'user_list', name='user-list'),
    url(r'^administer/user/(?P<eats_user_id>\d+)/$', 'user_change',
        name='user-change'),
    url(r'^administer/user/activate/$', 'user_activate', name='user-activate'),
    )
