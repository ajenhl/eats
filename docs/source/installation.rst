Installation and Setup
======================

Prerequisites
-------------

EATS is a `Django`_ application, and depends on two other Django
applications, `django-tmapi`_ and `django-selectable`_, and the Python
XML library `lxml`_. It also uses `django-webtest`_ for its view
tests.

EATS works with Django versions 1.3 and later.

.. _Django: https://www.djangoproject.com/
.. _django-tmapi: http://trac.assembla.com/django-tmapi/
.. _django-selectable: https://bitbucket.org/mlavin/django-selectable
.. _lxml: http://lxml.de/
.. _django-webtest: https://bitbucket.org/kmike/django-webtest/

Project settings
----------------

EATS uses Django's built-in sites framework as the source for the URLs
it associates with the entities it creates. Set the domain name
appropriately.
