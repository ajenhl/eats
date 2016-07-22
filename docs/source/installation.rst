Installation and Setup
======================

Prerequisites
-------------

EATS is a `Django`_ application, and depends on other Django
applications, `django-tmapi`_, `django-selectable`_,
`ddh_django_utils`_, and the Python XML library `lxml`_. It also uses
`django-webtest`_ for its view tests.

EATS works with Django versions 1.8 and later, and requires Python 3.4
or later.

Project settings
----------------

EATS uses Django's built-in sites framework as the source for the URLs
it associates with the entities it creates. Set the domain name
appropriately.

The URL for the `Topic Map`_ that underpins EATS must be set in the
Django project settings as EATS_TOPIC_MAP.

The number of search results per page can be specified as
EATS_RESULTS_PER_PAGE.

The number of extra forms to supply for each property assertion on
edit entity pages may be customised using the following settings:
EATS_EXTRA_EXISTENCE_FORMS, EATS_EXTRA_ENTITY_TYPE_FORMS,
EATS_EXTRA_NAME_FORMS, EATS_EXTRA_NAME_PART_FORMS,
EATS_EXTRA_ENTITY_RELATIONSHIP_FORMS, EATS_EXTRA_NOTE_FORMS, and
EATS_EXTRA_SUBJECT_IDENTIFIER_FORMS.

.. _Django: https://www.djangoproject.com/
.. _django-tmapi: https://github.com/ajenhl/django-tmapi
.. _django-selectable: https://github.com/mlavin/django-selectable
.. _ddh_django_utils: https://pypi.python.org/pypi/ddh_django_utils
.. _lxml: http://lxml.de/
.. _django-webtest: https://bitbucket.org/kmike/django-webtest/
.. _Topic Map: http://topicmaps.org/
