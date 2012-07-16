Installation and Setup
======================

Prerequisites
-------------

EATS is a `Django`_ application designed for version 1.3. Django has a
very helpful `installation guide`_.

EATS depends on two other Django applications, `django-tmapi`_ and
`django-selectable`_, and the Python XML library `lxml`_. It also uses
`django_webtest`_ for its view tests.

.. _Django: https://www.djangoproject.com/
.. _installation guide: https://docs.djangoproject.com/en/1.3/topics/install/
.. _django-tmapi: http://trac.assembla.com/django-tmapi/
.. _django-selectable: https://bitbucket.org/mlavin/django-selectable
.. _lxml: http://lxml.de/
.. _django_webtest: https://bitbucket.org/kmike/django-webtest/

Project settings
----------------

EATS uses Django's built-in sites framework as the source for the URLs
it associates with the entities it creates. Set the domain name
appropriately.
