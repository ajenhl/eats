Entity merging
==============

If two entities are found to be duplicates, they may be merged
together. This is preferable to simply deleting one, for two reasons:

1. If the entities (may) have both been referenced, then deleting one
   breaks those references.
2. Any information on the entity to be deleted that is not shared with
   the other entity must be manually added.

Merging one entity into another avoids both of these problems. The
URLs for the merged entity are associated with the other entity, and
all property assertions for that entity are merged in with those of
the other entity.

The merging of property assertions is simple. If the identical
information is present on both entities, and the property assertion is
not a name or entity relationship, the duplicate will be discarded;
otherwise, it is effectively copied over. This may mean (such as with
identical names) that there are duplicates that must be manually
deleted, but this is easily done in the editing interface.

Merging is a one way process that cannot be undone. To merge two
entities together, use the link at the bottom of the edit page for the
entity that will be merged *into*.
