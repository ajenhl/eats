Client programs
===============

EATS comes with a couple of client programs designed to add entity
references to TEI XML markup.


Banquet
-------

Banquet is a tool for performing bulk keying of name markup in TEI XML
documents. Its user interface presents all of the textual content of
name elements in groups, allowing the user to perform a single lookup
against an EATS instance and add an entity identifier to all of the
selected elements.

Banquet is a Python 2 project, and requires PyGTK and lxml.



oXygen lookup plugin
--------------------

The lookup client is a plugin for the oXygen XML editor that allows a
user to select some text, perform a lookup against an EATS instance
using that text, and add in appropriate TEI XML markup reference the
selected entity. It handles creating new name markup as well as
modifying existing name markup.
