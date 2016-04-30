from django.conf.urls import patterns, url

from eats.models import Authority, Calendar, DatePeriod, DateType, EntityRelationshipType, EntityType, Language, NamePartType, NameType, Script


# Displaying.
urlpatterns = patterns(
    'eats.views.display',
    url(r'^$', 'home', name='eats-home'),
    url(r'^entity/(?P<entity_id>\d+)/$', 'entity_view', name='eats-entity-view'),
    url(r'^entity/(?P<entity_id>\d+)/eatsml/', 'entity_eatsml_view',
        name='eats-entity-eatsml-view'),
    url(r'^search/$', 'search', name='eats-search'),
    url(r'^search/eatsml/$', 'search_eatsml', name='eats-search-eatsml'),
    url(r'^statistics/$', 'statistics', name='eats-statistics'),
    )

# Editing.
urlpatterns += patterns(
    'eats.views.edit',
    url(r'^entity/add/$', 'entity_add', name='eats-entity-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/$', 'entity_change',
        name='eats-entity-change'),
    url(r'^entity/(?P<entity_id>\d+)/delete/$', 'entity_delete',
        name='eats-entity-delete'),
    url(r'^entity/(?P<entity_id>\d+)/merge/$', 'entity_merge',
        name='eats-entity-merge'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/add/$',
        'date_add', name='eats-date-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/(?P<date_id>\d+)/$', 'date_change', name='eats-date-change'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/note/add/$',
        'pa_note_add', name='eats-pa-note-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/note/(?P<note_id>\d+)/$', 'pa_note_change', name='eats-pa-note-change'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/(?P<date_id>\d+)/note/add/$', 'date_note_add', name='eats-date-note-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/(?P<date_id>\d+)/note/(?P<note_id>\d+)/$', 'date_note_change', name='eats-date-note-change'),
    url(r'^export/eatsml/base/$', 'export_eatsml_base',
        name='eats-export-eatsml-base'),
    url(r'^export/eatsml/entities/$', 'export_eatsml_entities',
        name='eats-export-eatsml-entities'),
    url(r'^export/eatsml/entities/entity_type/(?P<entity_type_id>\d+)/$',
        'export_eatsml_entities_by_entity_type',
        name='eats-export-eatsml-entities-by-entity-type'),
    url(r'^export/eatsml/full/$', 'export_eatsml_full',
        name='eats-export_eatsml_full'),
    url(r'^import/$', 'import_eatsml', name='eats-import-eatsml'),
    url(r'^import/(?P<import_id>\d+)/$', 'display_eatsml_import',
        name='eats-display-eatsml-import'),
    url(r'^import/(?P<import_id>\d+)/raw/$', 'display_eatsml_import_raw',
        name='eats-display-eatsml-import-raw'),
    url(r'^import/(?P<import_id>\d+)/annotated/$',
        'display_eatsml_import_annotated',
        name='eats-display-eatsml-import-annotated'),
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
    url(r'^administer/$', 'administration_panel',
        name='eats-administration-panel'),
    url(r'^administer/create_topic_map/$', 'create_topic_map',
        name='eats-create-topic-map'),
    url(r'^administer/authority/$', 'topic_list', authority_data,
        name='eats-authority-list'),
    url(r'^administer/authority/add/$', 'topic_add', authority_data,
        name='eats-authority-add'),
    url(r'^administer/authority/(?P<topic_id>\d+)/$', 'topic_change',
        authority_data, name='eats-authority-change'),
    url(r'^administer/calendar/$', 'topic_list', calendar_data,
        name='eats-calendar-list'),
    url(r'^administer/calendar/add/$', 'topic_add', calendar_data,
        name='eats-calendar-add'),
    url(r'^administer/calendar/(?P<topic_id>\d+)/$', 'topic_change',
        calendar_data, name='eats-calendar-change'),
    url(r'^administer/date-period/$', 'topic_list', date_period_data,
        name='eats-dateperiod-list'),
    url(r'^administer/date-period/add/$', 'topic_add',
        date_period_data, name='eats-dateperiod-add'),
    url(r'^administer/date-period/(?P<topic_id>\d+)/$', 'topic_change',
        date_period_data, name='eats-dateperiod-change'),
    url(r'^administer/date-type/$', 'topic_list', date_type_data,
        name='eats-datetype-list'),
    url(r'^administer/date-type/add/$', 'topic_add', date_type_data,
        name='eats-datetype-add'),
    url(r'^administer/date-type/(?P<topic_id>\d+)/$', 'topic_change',
        date_type_data, name='eats-datetype-change'),
    url(r'^administer/entity-relationship-type/$', 'topic_list',
        entity_relationship_type_data, name='eats-entityrelationshiptype-list'),
    url(r'^administer/entity-relationship-type/add/$', 'topic_add',
        entity_relationship_type_data, name='eats-entityrelationshiptype-add'),
    url(r'^administer/entity-relationship-type/(?P<topic_id>\d+)/$',
        'topic_change', entity_relationship_type_data,
        name='eats-entityrelationshiptype-change'),
    url(r'^administer/entity-type/$', 'topic_list', entity_type_data,
        name='eats-entitytype-list'),
    url(r'^administer/entity-type/add/$', 'topic_add',
        entity_type_data, name='eats-entitytype-add'),
    url(r'^administer/entity-type/(?P<topic_id>\d+)/$', 'topic_change',
        entity_type_data, name='eats-entitytype-change'),
    url(r'^administer/language/$', 'topic_list', language_data,
        name='eats-language-list'),
    url(r'^administer/language/add/$', 'topic_add', language_data,
        name='eats-language-add'),
    url(r'^administer/language/(?P<topic_id>\d+)/$', 'topic_change',
        language_data, name='eats-language-change'),
    url(r'^administer/name-part-type/$', 'topic_list', name_part_type_data,
        name='eats-nameparttype-list'),
    url(r'^administer/name-part-type/add/$', 'topic_add',
        name_part_type_data, name='eats-nameparttype-add'),
    url(r'^administer/name-part-type/(?P<topic_id>\d+)/$', 'topic_change',
        name_part_type_data, name='eats-nameparttype-change'),
    url(r'^administer/name-type/$', 'topic_list', name_type_data,
        name='eats-nametype-list'),
    url(r'^administer/name-type/add/$', 'topic_add',
        name_type_data, name='eats-nametype-add'),
    url(r'^administer/name-type/(?P<topic_id>\d+)/$', 'topic_change',
        name_type_data, name='eats-nametype-change'),
    url(r'^administer/script/$', 'topic_list', script_data,
        name='eats-script-list'),
    url(r'^administer/script/add/$', 'topic_add', script_data,
        name='eats-script-add'),
    url(r'^administer/script/(?P<topic_id>\d+)/$', 'topic_change',
        script_data, name='eats-script-change'),
    url(r'^administer/user/$', 'user_list', name='eats-user-list'),
    url(r'^administer/user/(?P<eats_user_id>\d+)/$', 'user_change',
        name='eats-user-change'),
    url(r'^administer/user/activate/$', 'user_activate',
        name='eats-user-activate'),
    )
