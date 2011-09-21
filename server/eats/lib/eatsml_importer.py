from lxml import etree

from eats.lib.eatsml_handler import EATSMLHandler


class EATSMLImporter (EATSMLHandler):

    """An importer of EATSML documents into the EATS system.

    Importing EATSML allows only for adding material to an EATS topic
    map, not deleting or modifying existing material. Subject to the
    permissions of the user performing the import, the following may
    be created:

       * infrastructure elements (authorities, languages, calendars,
         etc)
       * entities
       * property assertions (for both new and existing entities)
       * dates (for new property assertions only)

    """

    def __init__ (self, topic_map):
        super(EATSMLImporter, self).__init__(topic_map)

    def import_xml (self, eatsml, user):
        """Imports EATSML document into EATS.

        Returns an XML tree of the original document annotated with
        ids.
        
        :param eatsml: XML of EATSML to import
        :type eatsml: `str`
        :param user: user performing the import
        :type user: `EATSUser`
        :rtype: `ElementTree`

        """
        # QAZ: check the authorities listed in the EATSML against the
        # user's editable authorities - abort the import if the former
        # isn't a subset of the latter. Except in the case of an
        # administrator.
        import_tree = etree.XML(eatsml)
        self._validate(import_tree)

