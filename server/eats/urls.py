from django.conf.urls.defaults import patterns, url


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

# Administration.
urlpatterns += patterns(
    'eats.views.admin',
    url(r'^administer/$', 'administration_panel', name='administration-panel'),
    url(r'^administer/create_topic_map/$', 'create_topic_map',
        name='create-topic-map'),
    url(r'^administer/authority/$', 'authority_list', name='authority-list'),
    url(r'^administer/authority/add/$', 'authority_add', name='authority-add'),
    url(r'^administer/authority/(?P<authority_id>\d+)/$', 'authority_change',
        name='authority-change'),
    )
