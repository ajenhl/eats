from django.conf.urls.defaults import patterns, url

from eats.constants import AUTHORITY_TYPE_IRI


# Displaying.
urlpatterns = patterns(
    'eats.views.display',
    url(r'^(?P<entity_id>\d+)/$', 'display_entity', name='display-entity'),
    )

# Editing.
urlpatterns += patterns(
    'eats.views.edit',
    url(r'^edit/create_entity/$', 'create_entity', name='create-entity'),
    )

topic_data = {
    'authority': {'type_iri': AUTHORITY_TYPE_IRI, 'name': 'authority'},
    }

# Administration.
urlpatterns += patterns(
    'eats.views.admin',
    url(r'^administer/$', 'administration_panel', name='administration-panel'),
    url(r'^administer/create_topic_map/$', 'create_topic_map',
        name='create-topic-map'),
    url(r'^administer/authority/$', 'topic_list', topic_data['authority'],
        name='authority-list'),
    url(r'^administer/authority/add/$', 'topic_add', topic_data['authority'],
        name='authority-add'),
    url(r'^administer/authority/(?P<topic_id>\d+)/$', 'topic_change',
        topic_data['authority'], name='authority-change'),
    )
