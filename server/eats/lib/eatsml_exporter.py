from lxml import etree


# Namespace constants.
XML_NAMESPACE = 'http://www.w3.org/XML/1998/namespace'
XML = '{%s}' % (XML_NAMESPACE)
EATS_NAMESPACE = 'http://eats.artefact.org.nz/ns/eatsml/'
EATS = '{%s}' % (EATS_NAMESPACE)
NSMAP = {None: EATS_NAMESPACE}


class EATSMLExporter (object):

    def __init__ (self):
        self._infrastructure_required = {
            'authority': set(),
            }

    def export_entities (self, entities):
        """Returns an XML tree of `entities` exported into EATSML.

        :param entities: entities to be exported
        :type entities: `list` or `QuerySet` of `Entity`s
        :rtype: `ElementTree`

        """
        root = etree.Element(EATS + 'collection', nsmap=NSMAP)
        entities_element = etree.SubElement(root, EATS + 'entities')
        for entity in entities:
            self._export_entity(entity, entities_element)
        # Export any required infrastructure elements.
        self._export_infrastructure(root)
        return root.getroottree()

    def _export_entity (self, entity, parent):
        """Export `entity`.

        :param entity: entity to export
        :type entity: `Entity`
        :param parent: XML element that will contain the exported entity
        :type parent: `Element`

        """
        entity_element = etree.SubElement(parent, EATS + 'entity')
        entity_element.set(XML + 'id', 'entity-%d' % entity.get_id())
        self._export_existences(entity, entity_element)

    def _export_existences (self, entity, parent):
        """Export the existences of `entity`.

        :param entity: entity whose exstences will be exported
        :type entity: `Entity`
        :param parent: XML element that will contain the exported existences
        :type parent: `Element`

        """
        existences = entity.get_existences()
        if existences:
            existences_element = etree.SubElement(parent, EATS + 'existences')
        for existence in existences:
            self._export_existence(existence, existences_element)

    def _export_existence (self, existence, parent):
        """Export `existence`.

        :param existence: existence to be exported
        :type existence: `ExistencePropertyAssertion`
        :param parent: XML element that will contain the exported existence
        :type parent: `Element`

        """
        existence_element = etree.SubElement(parent, EATS + 'existence')
        authority = existence.authority
        existence_element.set('authority', 'authority-%d' % authority.get_id())
        self._infrastructure_required['authority'].add(authority)

    def _export_infrastructure (self, parent):
        """Exports required infrastructure elements, appending them to
        `parent`.

        :param parent: XML element that will contain the export infrastructure
        :type parent: `Element`

        """
        authorities = self._infrastructure_required['authority']
        self._export_authorities(authorities, parent)
        # If there is an entities element that has already been
        # created, move it to after the infrastructure elements.
        if parent[0].tag == EATS + 'entities':
            parent.append(parent[0])

    def _export_authorities (self, authorities, parent):
        """Exports `authorities`, appending them to `parent`.

        :param authorities: authorities to export
        :type authorities: `set` of `Authority`s
        :param parent: XML element that will contain the exported authorities
        :type parent: `Element`

        """
        if authorities:
            authorities_element = etree.SubElement(parent, EATS + 'authorities')
        for authority in authorities:
            self._export_authority(authority, authorities_element)

    def _export_authority (self, authority, parent):
        """Exports `authority`, appending it to `parent`.

        :param authority: authority to export
        :type authority: `Authority`
        :param parent: XML element that will contain the exported authority
        :type parent: `Element`

        """
        authority_element = etree.SubElement(parent, EATS + 'authority')
        authority_element.set(XML + 'id', 'authority-%d' % authority.get_id())
        name_element = etree.SubElement(authority_element, EATS + 'name')
        name_element.text = authority.get_admin_name()
