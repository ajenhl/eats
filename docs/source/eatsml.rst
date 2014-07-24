EATSML: Importing and Exporting
===============================

EATS uses an XML format called EATSML for serialisation of its
data. Existing data can be exported from EATS, and new data imported
into EATS using it.


Export
------

There are several different exports available, depending on what data
is wanted:

* Base export, that exports the infrastructural data (authorities,
  languages, name types, etc) but no entities. Typically the
  infrastructural data exported is limited to that relating to the
  authorities the user is an editor for.

  This is available at ``/export/eatsml/base/``.

* Entity export, that exports the entities, along with the
  infrastructural data that is referenced by those entities.

  This is available at ``/export/eatsml/entities/``.

* Full export, that exports all infrastructure data and all entities.

  This is available at ``/export/eatsml/full/``.

The EATSML of an export specifies the identifier of a piece of data in
the EATS database, in the ``eats_id`` attribute. This is needed when
performing an import that adds new data that reference existing
information, such as the authority for a new existence property
assertion.


Import
------

The import of an EATSML document is available at ``/import/``.

When importing EATSML that has been exported from a different EATS
system, the ``eats_id`` attributes must be either removed (if the
identified data does not exist in the new system), or changed to match
the identifiers used in the new system. Otherwise the import will fail
because it cannot find the referenced data - or worse, succeed but
associate the imported information with the wrong data that just
happens to share the same id!

After making an import, the imported EATSML can be viewed either in
the form it was imported, or with the appropriate ``eats_id``
attributes added.

The import process automatically prunes the EATSML of any material
that is neither to be added, nor referenced by data that is to be
added. Therefore, the EATSML that is displayed for an import may not
exactly match the EATSML that was actually sent to the server. This is
done to make it easier to see what is added in an import.
