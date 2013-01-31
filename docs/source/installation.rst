Installation and Setup
======================

Prerequisites
-------------

EATS is a `Django`_ application, and depends on two other Django
applications, `django-tmapi`_ and `django-selectable`_, and the Python
XML library `lxml`_. It also uses `django-webtest`_ for its view
tests.

EATS works with Django versions 1.4 and later (the only issue with
Django 1.3 is with pagination, and requires a single line change in
``views/display.py``).

Project settings
----------------

EATS uses Django's built-in sites framework as the source for the URLs
it associates with the entities it creates. Set the domain name
appropriately.

The URL for the `Topic Map`_ that underpins EATS must be set in the
Django project settings as EATS_TOPIC_MAP.

.. _Django: https://www.djangoproject.com/
.. _django-tmapi: https://github.com/ajenhl/django-tmapi
.. _django-selectable: https://bitbucket.org/mlavin/django-selectable
.. _lxml: http://lxml.de/
.. _django-webtest: https://bitbucket.org/kmike/django-webtest/
.. _Topic Map: http://topicmaps.org/
