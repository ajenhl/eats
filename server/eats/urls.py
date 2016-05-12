from django.conf.urls import url

from eats.models import Authority, Calendar, DatePeriod, DateType, EntityRelationshipType, EntityType, Language, NamePartType, NameType, Script
from .views import admin, display, edit


# Displaying.
urlpatterns = [
    url(r'^$', display.home, name='eats-home'),
    url(r'^entity/(?P<entity_id>\d+)/$', display.entity_view, name='eats-entity-view'),
    url(r'^entity/(?P<entity_id>\d+)/eatsml/', display.entity_eatsml_view,
        name='eats-entity-eatsml-view'),
    url(r'^search/$', display.search, name='eats-search'),
    url(r'^search/eatsml/$', display.search_eatsml, name='eats-search-eatsml'),
    url(r'^statistics/$', display.statistics, name='eats-statistics'),
]

# Editing.
urlpatterns += [
    url(r'^entity/add/$', edit.entity_add, name='eats-entity-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/$', edit.entity_change,
        name='eats-entity-change'),
    url(r'^entity/(?P<entity_id>\d+)/delete/$', edit.entity_delete,
        name='eats-entity-delete'),
    url(r'^entity/(?P<entity_id>\d+)/merge/$', edit.entity_merge,
        name='eats-entity-merge'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/add/$',
        edit.date_add, name='eats-date-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/(?P<date_id>\d+)/$', edit.date_change, name='eats-date-change'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/note/add/$',
        edit.pa_note_add, name='eats-pa-note-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/note/(?P<note_id>\d+)/$', edit.pa_note_change, name='eats-pa-note-change'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/(?P<date_id>\d+)/note/add/$', edit.date_note_add, name='eats-date-note-add'),
    url(r'^entity/(?P<entity_id>\d+)/edit/(?P<assertion_id>\d+)/date/(?P<date_id>\d+)/note/(?P<note_id>\d+)/$', edit.date_note_change, name='eats-date-note-change'),
    url(r'^export/eatsml/base/$', edit.export_eatsml_base,
        name='eats-export-eatsml-base'),
    url(r'^export/eatsml/entities/$', edit.export_eatsml_entities,
        name='eats-export-eatsml-entities'),
    url(r'^export/eatsml/entities/entity_type/(?P<entity_type_id>\d+)/$',
        edit.export_eatsml_entities_by_entity_type,
        name='eats-export-eatsml-entities-by-entity-type'),
    url(r'^export/eatsml/full/$', edit.export_eatsml_full,
        name='eats-export_eatsml_full'),
    url(r'^import/$', edit.import_eatsml, name='eats-import-eatsml'),
    url(r'^import/(?P<import_id>\d+)/$', edit.display_eatsml_import,
        name='eats-display-eatsml-import'),
    url(r'^import/(?P<import_id>\d+)/raw/$', edit.display_eatsml_import_raw,
        name='eats-display-eatsml-import-raw'),
    url(r'^import/(?P<import_id>\d+)/annotated/$',
        edit.display_eatsml_import_annotated,
        name='eats-display-eatsml-import-annotated'),
]

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
urlpatterns += [
    url(r'^administer/$', admin.administration_panel,
        name='eats-administration-panel'),
    url(r'^administer/create_topic_map/$', admin.create_topic_map,
        name='eats-create-topic-map'),
    url(r'^administer/authority/$', admin.topic_list, authority_data,
        name='eats-authority-list'),
    url(r'^administer/authority/add/$', admin.topic_add, authority_data,
        name='eats-authority-add'),
    url(r'^administer/authority/(?P<topic_id>\d+)/$', admin.topic_change,
        authority_data, name='eats-authority-change'),
    url(r'^administer/calendar/$', admin.topic_list, calendar_data,
        name='eats-calendar-list'),
    url(r'^administer/calendar/add/$', admin.topic_add, calendar_data,
        name='eats-calendar-add'),
    url(r'^administer/calendar/(?P<topic_id>\d+)/$', admin.topic_change,
        calendar_data, name='eats-calendar-change'),
    url(r'^administer/date-period/$', admin.topic_list, date_period_data,
        name='eats-dateperiod-list'),
    url(r'^administer/date-period/add/$', admin.topic_add,
        date_period_data, name='eats-dateperiod-add'),
    url(r'^administer/date-period/(?P<topic_id>\d+)/$', admin.topic_change,
        date_period_data, name='eats-dateperiod-change'),
    url(r'^administer/date-type/$', admin.topic_list, date_type_data,
        name='eats-datetype-list'),
    url(r'^administer/date-type/add/$', admin.topic_add, date_type_data,
        name='eats-datetype-add'),
    url(r'^administer/date-type/(?P<topic_id>\d+)/$', admin.topic_change,
        date_type_data, name='eats-datetype-change'),
    url(r'^administer/entity-relationship-type/$', admin.topic_list,
        entity_relationship_type_data, name='eats-entityrelationshiptype-list'),
    url(r'^administer/entity-relationship-type/add/$', admin.topic_add,
        entity_relationship_type_data, name='eats-entityrelationshiptype-add'),
    url(r'^administer/entity-relationship-type/(?P<topic_id>\d+)/$',
        admin.topic_change, entity_relationship_type_data,
        name='eats-entityrelationshiptype-change'),
    url(r'^administer/entity-type/$', admin.topic_list, entity_type_data,
        name='eats-entitytype-list'),
    url(r'^administer/entity-type/add/$', admin.topic_add,
        entity_type_data, name='eats-entitytype-add'),
    url(r'^administer/entity-type/(?P<topic_id>\d+)/$', admin.topic_change,
        entity_type_data, name='eats-entitytype-change'),
    url(r'^administer/language/$', admin.topic_list, language_data,
        name='eats-language-list'),
    url(r'^administer/language/add/$', admin.topic_add, language_data,
        name='eats-language-add'),
    url(r'^administer/language/(?P<topic_id>\d+)/$', admin.topic_change,
        language_data, name='eats-language-change'),
    url(r'^administer/name-part-type/$', admin.topic_list, name_part_type_data,
        name='eats-nameparttype-list'),
    url(r'^administer/name-part-type/add/$', admin.topic_add,
        name_part_type_data, name='eats-nameparttype-add'),
    url(r'^administer/name-part-type/(?P<topic_id>\d+)/$', admin.topic_change,
        name_part_type_data, name='eats-nameparttype-change'),
    url(r'^administer/name-type/$', admin.topic_list, name_type_data,
        name='eats-nametype-list'),
    url(r'^administer/name-type/add/$', admin.topic_add,
        name_type_data, name='eats-nametype-add'),
    url(r'^administer/name-type/(?P<topic_id>\d+)/$', admin.topic_change,
        name_type_data, name='eats-nametype-change'),
    url(r'^administer/script/$', admin.topic_list, script_data,
        name='eats-script-list'),
    url(r'^administer/script/add/$', admin.topic_add, script_data,
        name='eats-script-add'),
    url(r'^administer/script/(?P<topic_id>\d+)/$', admin.topic_change,
        script_data, name='eats-script-change'),
    url(r'^administer/user/$', admin.user_list, name='eats-user-list'),
    url(r'^administer/user/(?P<eats_user_id>\d+)/$', admin.user_change,
        name='eats-user-change'),
    url(r'^administer/user/activate/$', admin.user_activate,
        name='eats-user-activate'),
]
