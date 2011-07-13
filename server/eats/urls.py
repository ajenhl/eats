from django.conf.urls.defaults import patterns, url

from eats.constants import AUTHORITY_TYPE_IRI, CALENDAR_TYPE_IRI, DATE_PERIOD_TYPE_IRI, DATE_TYPE_TYPE_IRI, ENTITY_RELATIONSHIP_TYPE_TYPE_IRI, ENTITY_TYPE_TYPE_IRI, LANGUAGE_TYPE_IRI, NAME_TYPE_TYPE_IRI, SCRIPT_TYPE_IRI
from eats.models import Authority


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
topic_data = {
    'authority': {'type_iri': AUTHORITY_TYPE_IRI, 'name': 'authority'},
    'calendar': {'type_iri': CALENDAR_TYPE_IRI, 'name': 'calendar'},
    'date_period': {'type_iri': DATE_PERIOD_TYPE_IRI, 'name': 'date-period'},
    'date_type': {'type_iri': DATE_TYPE_TYPE_IRI, 'name': 'date-type'},
    'entity_relationship_type': {'type_iri': ENTITY_RELATIONSHIP_TYPE_TYPE_IRI,
                                 'name': 'entity-relationship-type'},
    'entity_type': {'type_iri': ENTITY_TYPE_TYPE_IRI, 'name': 'entity-type'},
    'language': {'type_iri': LANGUAGE_TYPE_IRI, 'name': 'language'},
    'name_type': {'type_iri': NAME_TYPE_TYPE_IRI, 'name': 'name-type'},
    'script': {'type_iri': SCRIPT_TYPE_IRI, 'name': 'script'},
    }

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
    url(r'^administer/calendar/$', 'topic_list', topic_data['calendar'],
        name='calendar-list'),
    url(r'^administer/calendar/add/$', 'topic_add', topic_data['calendar'],
        name='calendar-add'),
    url(r'^administer/calendar/(?P<topic_id>\d+)/$', 'topic_change',
        topic_data['calendar'], name='calendar-change'),
    url(r'^administer/date-period/$', 'topic_list', topic_data['date_period'],
        name='date-period-list'),
    url(r'^administer/date-period/add/$', 'topic_add',
        topic_data['date_period'], name='date-period-add'),
    url(r'^administer/date-period/(?P<topic_id>\d+)/$', 'topic_change',
        topic_data['date_period'], name='date-period-change'),
    url(r'^administer/date-type/$', 'topic_list', topic_data['date_type'],
        name='date-type-list'),
    url(r'^administer/date-type/add/$', 'topic_add', topic_data['date_type'],
        name='date-type-add'),
    url(r'^administer/date-type/(?P<topic_id>\d+)/$', 'topic_change',
        topic_data['date_type'], name='date-type-change'),
    url(r'^administer/entity-relationship-type/$', 'topic_list',
        topic_data['entity_relationship_type'],
        name='entity-relationship-type-list'),
    url(r'^administer/entity-relationship-type/add/$', 'topic_add',
        topic_data['entity_relationship_type'],
        name='entity-relationship-type-add'),
    url(r'^administer/entity-relationship-type/(?P<topic_id>\d+)/$',
        'topic_change', topic_data['entity_relationship_type'],
        name='entity-relationship-type-change'),
    url(r'^administer/entity-type/$', 'topic_list', topic_data['entity_type'],
        name='entity-type-list'),
    url(r'^administer/entity-type/add/$', 'topic_add',
        topic_data['entity_type'], name='entity-type-add'),
    url(r'^administer/entity-type/(?P<topic_id>\d+)/$', 'topic_change',
        topic_data['entity_type'], name='entity-type-change'),
    url(r'^administer/language/$', 'topic_list', topic_data['language'],
        name='language-list'),
    url(r'^administer/language/add/$', 'topic_add', topic_data['language'],
        name='language-add'),
    url(r'^administer/language/(?P<topic_id>\d+)/$', 'topic_change',
        topic_data['language'], name='language-change'),
    url(r'^administer/name-type/$', 'topic_list', topic_data['name_type'],
        name='name-type-list'),
    url(r'^administer/name-type/add/$', 'topic_add',
        topic_data['name_type'], name='name-type-add'),
    url(r'^administer/name-type/(?P<topic_id>\d+)/$', 'topic_change',
        topic_data['name_type'], name='name-type-change'),
    url(r'^administer/script/$', 'topic_list', topic_data['script'],
        name='script-list'),
    url(r'^administer/script/add/$', 'topic_add', topic_data['script'],
        name='script-add'),
    url(r'^administer/script/(?P<topic_id>\d+)/$', 'topic_change',
        topic_data['script'], name='script-change'),
    )
