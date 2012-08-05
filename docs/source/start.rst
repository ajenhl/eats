Getting Started
===============

Administration
--------------

After installing and setting up EATS, there are four steps to getting
everything in place to create entities. These are all done via the
administration interface at ``/administer/`` (this is `not` the Django
admin interface).

* Create the Topic Map that will hold your EATS data.

* Add whatever languages, scripts, name types, entity types, etc, that
  you wish to use.

* Add one or more authorities, and specify which language, scripts,
  etc, are available to them.

* Create EATS users (these are existing Django users), and if they are
  to be able to create and edit entities, add them to each authority
  for which they are to be an editor.


Creating and editing entities
-----------------------------

To add new entities, either use the form at ``/entity/add/`` or use
one of the client tools to generate them from the names in a source
text. An entity may be viewed at ``/entity/<id>/`` and edited at
``/entity/<id>/edit/``.
