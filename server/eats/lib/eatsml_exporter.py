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
            'entity_relationship_type': set(),
            'entity_type': set(),
            'language': set(),
            'name_part_type': set(),
            'name_type': set(),
            'script': set(),
            }
        self._entities_required = set()

    def export_entities (self, entities):
        """Returns an XML tree of `entities` exported into EATSML.

        :param entities: entities to export
        :type entities: `list` or `QuerySet` of `Entity`s
        :rtype: `ElementTree`

        """
        root = etree.Element(EATS + 'collection', nsmap=NSMAP)
        entities_element = etree.SubElement(root, EATS + 'entities')
        for entity in entities:
            self._export_entity(entity, entities_element)
        # Export any additional entities that might need to be
        # exported (due to being referenced from another entity).
        for entity in self._entities_required:
            if entity not in entities:
                self._export_entity(entity, entities_element, True)
        # Export any required infrastructure elements.
        self._export_infrastructure(root)
        return root.getroottree()

    def _export_entity (self, entity, parent, extra=False):
        """Exports `entity`.

        :param entity: entity to export
        :type entity: `Entity`
        :param parent: XML element that will contain the exported entity
        :type parent: `Element`
        :param extra: if True, `entity` is only referenced by another entity
        :type extra: `bool`

        """
        entity_element = etree.SubElement(parent, EATS + 'entity')
        entity_element.set(XML + 'id', 'entity-%d' % entity.get_id())
        self._export_existence_property_assertions(entity, entity_element)
        self._export_entity_type_property_assertions(entity, entity_element)
        self._export_name_property_assertions(entity, entity_element)
        if extra:
            entity_element.set('related_entity', 'true')
        else:
            # Only export relationships for primary entities (those
            # specifically requested to be exported); otherwise there
            # is the possibility of recursion.
            self._export_entity_relationship_property_assertions(
                entity, entity_element)
        self._export_note_property_assertions(entity, entity_element)
        self._export_subject_identifier_property_assertions(
            entity, entity_element)

    def _export_entity_relationship_property_assertions (self, entity, parent):
        """Exports the entity relationships of `entity`.

        :param entity: entity whose entity relationships will be exported
        :type entity: `Entity`
        :param parent: XML element that will contain the exported entity types
        :type parent: `Element`

        """
        entity_relationships = entity.get_entity_relationships()
        if entity_relationships:
            entity_relationships_element = etree.SubElement(
                parent, EATS + 'entity_relationships')
        for entity_relationship in entity_relationships:
            self._export_entity_relationship_property_assertion(
                entity_relationship, entity, entity_relationships_element)

    def _export_entity_relationship_property_assertion (self, assertion,
                                                        entity, parent):
        """Exports the entity relationship `assertion`.

        :param assertion: entity relationship to export
        :type assertion: `EntityRelationshipPropertyAssertion`
        :param entity: entity whose assertion this is
        :type entity: `Entity`
        :param parent: XML element that will contain the exported
          entity relationships
        :type parent: `Element`

        """        
        entity_relationship_element = etree.SubElement(
            parent, EATS + 'entity_relationship')
        authority = assertion.authority
        entity_relationship_element.set('authority', 'authority-%d' %
                                        authority.get_id())
        relationship_type = assertion.entity_relationship_type
        entity_relationship_element.set('entity_relationship_type',
                                        'entity_relationship_type-%d' %
                                        relationship_type.get_id())
        domain_entity = assertion.domain_entity
        range_entity = assertion.range_entity
        entity_relationship_element.set('domain_entity', 'entity-%d' %
                                        domain_entity.get_id())
        entity_relationship_element.set('range_entity', 'entity-%d' %
                                        range_entity.get_id())
        self._infrastructure_required['authority'].add(authority)
        self._infrastructure_required['entity_relationship_type'].add(
            relationship_type)
        if domain_entity == entity:
            self._entities_required.add(range_entity)
        else:
            self._entities_required.add(domain_entity)
        
    def _export_entity_type_property_assertions (self, entity, parent):
        """Exports the entity types of `entity`.

        :param entity: entity whose entity types will be exported
        :type entity: `Entity`
        :param parent: XML element that will contain the exported entity types
        :type parent: `Element`

        """
        entity_types = entity.get_entity_types()
        if entity_types:
            entity_types_element = etree.SubElement(parent,
                                                    EATS + 'entity_types')
        for entity_type in entity_types:
            self._export_entity_type_property_assertion(entity_type,
                                                        entity_types_element)

    def _export_entity_type_property_assertion (self, assertion, parent):
        """Exports the entity type `assertion`.

        :param assertopm: entity type property assertion to export
        :type assertion: `EntityTypePropertyAssertion`
        :param parent: XML element that will contain the exported entity type
        :type parent: `Element`

        """
        entity_type_element = etree.SubElement(parent, EATS + 'entity_type')
        authority = assertion.authority
        entity_type = assertion.entity_type
        entity_type_element.set('authority', 'authority-%d' %
                                authority.get_id())
        entity_type_element.set('entity_type', 'entity_type-%d' %
                                entity_type.get_id())
        self._infrastructure_required['authority'].add(authority)
        self._infrastructure_required['entity_type'].add(entity_type)

    def _export_existence_property_assertions (self, entity, parent):
        """Exports the existences of `entity`.

        :param entity: entity whose exstences will be exported
        :type entity: `Entity`
        :param parent: XML element that will contain the exported existences
        :type parent: `Element`

        """
        existences = entity.get_existences()
        if existences:
            existences_element = etree.SubElement(parent, EATS + 'existences')
        for existence in existences:
            self._export_existence_property_assertion(existence,
                                                      existences_element)

    def _export_existence_property_assertion (self, existence, parent):
        """Exports `existence`.

        :param existence: existence to export
        :type existence: `ExistencePropertyAssertion`
        :param parent: XML element that will contain the exported existence
        :type parent: `Element`

        """
        existence_element = etree.SubElement(parent, EATS + 'existence')
        authority = existence.authority
        existence_element.set('authority', 'authority-%d' % authority.get_id())
        self._infrastructure_required['authority'].add(authority)

    def _export_name_property_assertions (self, entity, parent):
        """Exports the names of `entity`.

        :param entity: entity whose names will be exported
        :type entity: `Entity`
        :param parent: XML element that will contain the exported names
        :type parent: `Element`

        """
        names = entity.get_eats_names()
        if names:
            names_element = etree.SubElement(parent, EATS + 'names')
        for name in names:
            self._export_name_property_assertion(name, names_element)

    def _export_name_property_assertion (self, assertion, parent):
        """Exports the name in `assertion`.

        :param assertion: name to export
        :type assertion: `NamePropertyAssertion`
        :param parent: XML element that will contain the exported name
        :type parent: `Element`

        """
        name_element = etree.SubElement(parent, EATS + 'name')
        authority = assertion.authority
        name = assertion.name
        name_type = name.name_type
        language = name.language
        script = name.script
        name_element.set('authority', 'authority-%d' % authority.get_id())
        name_element.set('language', 'language-%d' % language.get_id())
        name_element.set('name_type', 'name_type-%d' % name_type.get_id())
        name_element.set('script', 'script-%d' % script.get_id())
        self._infrastructure_required['authority'].add(authority)
        self._infrastructure_required['language'].add(language)
        self._infrastructure_required['script'].add(script)
        self._infrastructure_required['name_type'].add(name_type)
        display_form_element = etree.SubElement(name_element,
                                                EATS + 'display_form')
        display_form_element.text = name.display_form
        name_parts = name.get_name_parts()
        if name_parts:
            name_parts_element = etree.SubElement(name_element,
                                                  EATS + 'name_parts')
        for name_part_type, name_parts in name_parts.items():
            name_part_type_id = name_part_type.get_id()
            self._infrastructure_required['name_part_type'].add(name_part_type)
            for name_part in name_parts:
                self._export_name_part(name_part_type_id, name_part,
                                       name_parts_element)
        assembled_form_element = etree.SubElement(name_element,
                                                  EATS + 'assembled_form')
        assembled_form_element.text = name.assembled_form

    def _export_name_part (self, name_part_type_id, name_part, parent):
        """Exports `name_part`.

        :param name_part_type_id: the id of the name part type
        :type name_part_type: `int`
        :param name_parts: the name part to export
        :type name_parts: `NamePart`
        :param parent: XML element that will contain the exported name part
        :type parent: `Element`

        """
        name_part_element = etree.SubElement(parent, EATS + 'name_part')
        language = name_part.language
        script = name_part.script
        self._infrastructure_required['language'].add(language)
        self._infrastructure_required['script'].add(script)
        name_part_element.set('name_part_type', 'name_part_type-%d' %
                              name_part_type_id)
        name_part_element.set('language', 'language-%d' % language.get_id())
        name_part_element.set('script', 'script-%d' % script.get_id())
        name_part_element.text = name_part.display_form

    def _export_note_property_assertions (self, entity, parent):
        """Exports the notes of `entity`.

        :param entity: entity whose notes will be exported
        :type entity: `Entity`
        :param parent: XML element that will contain the exported notes
        :type parent: `Element`

        """
        notes = entity.get_notes()
        if notes:
            notes_element = etree.SubElement(parent, EATS + 'notes')
        for note in notes:
            self._export_note_property_assertion(note, notes_element)

    def _export_note_property_assertion (self, assertion, parent):
        """Exports the note `assertion`.

        :param assertion: note to export
        :type assertion: `NotePropertyAssertion`
        :param parent: XML element that will contain the exported note
        :type parent: `Element`

        """
        authority = assertion.authority
        note_element = etree.SubElement(parent, EATS + 'note')
        note_element.set('authority', 'authority-%d' % authority.get_id())
        note_element.text = assertion.note
        self._infrastructure_required['authority'].add(authority)

    def _export_subject_identifier_property_assertions (self, entity, parent):
        """Exports the subject identifiers of `entity`.

        :param entity: entity whose subject identifiers will be exported
        :type entity: `Entity`
        :param parent: XML element that will contain the exported
          subject identifiers
        :type parent: `Element`

        """
        subject_identifiers = entity.get_subject_identifiers()
        if subject_identifiers:
            subject_identifiers_element = etree.SubElement(
                parent, EATS + 'subject_identifiers')
        for subject_identifier in subject_identifiers:
            self._export_subject_identifier_property_assertion(
                subject_identifier, subject_identifiers_element)

    def _export_subject_identifier_property_assertion (self, assertion, parent):
        """Exports the subject identifier `assertion`.

        :param assertion: subject identifier to export
        :type assertion: `SubjectIdentifierPropertyAssertion`
        :param parent: XML element that will contain the exported
          subject identifier
        :type parent: `Element`

        """
        subject_identifier_element = etree.SubElement(
            parent, EATS + 'subject_identifier')
        authority = assertion.authority
        subject_identifier_element.set('authority', 'authority-%d' %
                                       authority.get_id())
        subject_identifier_element.text = assertion.subject_identifier
        self._infrastructure_required['authority'].add(authority)

    def _export_infrastructure (self, parent):
        """Exports required infrastructure elements, appending them to
        `parent`.

        :param parent: XML element that will contain the export infrastructure
        :type parent: `Element`

        """
        authorities = self._infrastructure_required['authority']
        self._export_authorities(authorities, parent)
        entity_types = self._infrastructure_required['entity_type']
        self._export_entity_types(entity_types, parent)
        languages = self._infrastructure_required['language']
        self._export_languages(languages, parent)
        scripts = self._infrastructure_required['script']
        self._export_scripts(scripts, parent)
        name_types = self._infrastructure_required['name_type']
        self._export_name_types(name_types, parent)
        name_part_types = self._infrastructure_required['name_part_type']
        self._export_name_part_types(name_part_types, parent)
        entity_relationship_types = self._infrastructure_required['entity_relationship_type']
        self._export_entity_relationship_types(entity_relationship_types,
                                               parent)
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
        self._export_authority_infrastructure('entity_type', 'entity_types',
                                              'entity_type', authority_element)
        self._export_authority_infrastructure('language', 'languages',
                                              'language', authority_element)
        self._export_authority_infrastructure('name_type', 'name_types',
                                              'name_type', authority_element)
        self._export_authority_infrastructure(
            'name_part_type', 'name_part_types', 'name_part_type',
            authority_element)
        self._export_authority_infrastructure('script', 'scripts', 'script',
                                              authority_element)
        self._export_authority_infrastructure(
            'entity_relationship_type', 'entity_relationship_types',
            'entity_relationship_type', authority_element)

    def _export_authority_infrastructure (self, infrastructure_element_name,
                                          container_element_name, element_name,
                                          parent):
        """Exports ...

        :param infrastructure_element_name: name of the infrastructure
          element to export
        :type infrastructure_element_name: `str`
        :param container_element_name: name of the element to contain
          the exported infrastructure elements
        :type container_element_name: `str`
        :param element_name: name of the element for each infrastructure element
        :type element_name: `str`
        :param parent: XML element that will contain the exported elements
        :type parent: `Element`

        """
        items = self._infrastructure_required[infrastructure_element_name]
        if items:
            container_element = etree.SubElement(parent, EATS +
                                                 container_element_name)
        for item in items:
            element = etree.SubElement(container_element, EATS +
                                       element_name)
            element.set('ref', '%s-%d' % (infrastructure_element_name,
                                          item.get_id()))

    def _export_entity_relationship_types (self, relationship_types, parent):
        """Exports `relationship_types`, appending them to `parent`.

        :param relationship_types: entity relationship types to export
        :type relationshp_types: `set` of `EntityRelationshipType`s
        :param parent: XML element that will contain the exported
          entity relationship types
        :type parent: `Element`

        """
        if relationship_types:
            relationship_types_element = etree.SubElement(
                parent, EATS + 'entity_relationship_types')
        for relationship_type in relationship_types:
            self._export_entity_relationship_type(relationship_type,
                                                  relationship_types_element)

    def _export_entity_relationship_type (self, relationship_type, parent):
        """Exports `relationship_type`, appending it to `parent`.

        :param relationship_type: entity relationship type to export
        :type relationship_type: `EntityRelationshipType`
        :param parent: XML elementa that will contain the exported
          entity relationship type
        :type parent: `Element`

        """
        relationship_type_element = etree.SubElement(
            parent, EATS + 'entity_relationship_type')
        relationship_type_element.set(XML + 'id', 'entity_relationship_type-%d'
                                      % relationship_type.get_id())
        name_element = etree.SubElement(relationship_type_element,
                                        EATS + 'name')
        name_element.text = relationship_type.get_admin_forward_name()
        reverse_name_element = etree.SubElement(relationship_type_element,
                                                EATS + 'reverse_name')
        reverse_name_element.text = relationship_type.get_admin_reverse_name()
            
    def _export_entity_types (self, entity_types, parent):
        """Exports `entity_types`, appending them to `parent`.

        :param entity_types: entity types to export
        :type entity_types: `set` of `EntityType`s
        :param parent: XML element that will contain the exported entity types
        :type parent: `Element`

        """
        if entity_types:
            entity_types_element = etree.SubElement(parent,
                                                    EATS + 'entity_types')
        for entity_type in entity_types:
            self._export_entity_type(entity_type, entity_types_element)

    def _export_entity_type (self, entity_type, parent):
        """Exports `entity_type`, appending it to `parent`.

        :param entity_type: entity type to export
        :type entity_type: `EntityType`
        :param parent: XML element that will contain the exported entity type
        :type parent: `Element`

        """
        entity_type_element = etree.SubElement(parent, EATS + 'entity_type')
        entity_type_element.set(XML + 'id', 'entity_type-%d' %
                                entity_type.get_id())
        name_element = etree.SubElement(entity_type_element, EATS + 'name')
        name_element.text = entity_type.get_admin_name()

    def _export_languages (self, languages, parent):
        """Exports `languages`, appending them to `parent`.

        :param languages: languages to export
        :type languages: `set` of `Language`s
        :param parent: XML element that will contain the exported languages
        :type parent: `Element`

        """
        if languages:
            languages_element = etree.SubElement(parent, EATS + 'languages')
        for language in languages:
            self._export_language(language, languages_element)

    def _export_language (self, language, parent):
        """Exports `language`, appending it to `parent`.

        :param language: language to export
        :type language: `Language`
        :param parent: XML element that will contain the exported language
        :type parent: `Element`

        """
        language_element = etree.SubElement(parent, EATS + 'language')
        language_element.set(XML + 'id', 'language-%d' % language.get_id())
        name_element = etree.SubElement(language_element, EATS + 'name')
        name_element.text = language.get_admin_name()
        code_element = etree.SubElement(language_element, EATS + 'code')
        code_element.text = language.get_code()
        self._export_language_name_part_types(language, language_element)

    def _export_language_name_part_types (self, language, parent):
        """Exports the name part types associated with `language`.

        :param language: language whose name part types will be exported
        :type language: `Language`
        :param parent: XML element that will contain the export name part types
        :type parent: `Element`

        """
        name_part_types = language.name_part_types
        if name_part_types:
            name_part_types_element = etree.SubElement(parent, EATS +
                                                       'name_part_types')
        for name_part_type in name_part_types:
            name_part_type_element = etree.SubElement(name_part_types_element,
                                                      EATS + 'name_part_type')
            name_part_type_element.set('ref', 'name_part_type-%d' %
                                       name_part_type.get_id())

    def _export_name_types (self, name_types, parent):
        """Exports `name_types`, appending them to `parent`.

        :param name_types: name types to export
        :type name_types: `set` of `NameType`s
        :param parent: XML element that will contain the exported name types
        :type parent: `Element`

        """
        if name_types:
            name_types_element = etree.SubElement(parent, EATS + 'name_types')
        for name_type in name_types:
            self._export_name_type(name_type, name_types_element)

    def _export_name_type (self, name_type, parent):
        """Exports `name_type`, appending it to parent.

        :param name_type: name type to export
        :type name_type: `NameType`
        :param parent: XML element that will contain the exported name type
        :type parent: `Element`

        """
        name_type_element = etree.SubElement(parent, EATS + 'name_type')
        name_type_element.set(XML + 'id', 'name_type-%d' % name_type.get_id())
        name_element = etree.SubElement(name_type_element, EATS + 'name')
        name_element.text = name_type.get_admin_name()

    def _export_name_part_types (self, name_part_types, parent):
        """Exports `name_part_types`, appending them to `parent`.

        :param name_part_types: name part types to export
        :type name_part_types: `set` of `NamePartType`s
        :param parent: XML element that will contain the exported name
          part types
        :type parent: `Element`

        """
        if name_part_types:
            name_part_types_element = etree.SubElement(parent, EATS +
                                                       'name_part_types')
        for name_part_type in name_part_types:
            self._export_name_part_type(name_part_type, name_part_types_element)

    def _export_name_part_type (self, name_part_type, parent):
        """Exports `name_part_type`, appending it to `parent`.

        :param name_part_type: name part type to export
        :type name_part_type: `NamePartType`
        :param parent: XML element that will contain the export name part type
        :type parent: `Element`

        """
        name_part_type_element = etree.SubElement(parent, EATS +
                                                  'name_part_type')
        name_part_type_element.set(XML + 'id', 'name_part_type-%d' %
                                   name_part_type.get_id())
        name_element = etree.SubElement(name_part_type_element, EATS + 'name')
        name_element.text = name_part_type.get_admin_name()

    def _export_scripts (self, scripts, parent):
        """Exports `scripts`, appending them to `parent`.

        :param scripts: scripts to export
        :type scripts: `set` of `Script`s
        :param parent: XML element that will contain the exported scripts
        :type parent: `Element`

        """
        if scripts:
            scripts_element = etree.SubElement(parent, EATS + 'scripts')
        for script in scripts:
            self._export_script(script, scripts_element)

    def _export_script (self, script, parent):
        """Exports `script`, appending it to `parent`.

        :param script: script to export
        :type script: `Script`
        :param parent: XML element that will contain the exported script
        :type parent: `Element`

        """
        script_element = etree.SubElement(parent, EATS + 'script')
        script_element.set(XML + 'id', 'script-%d' % script.get_id())
        name_element = etree.SubElement(script_element, EATS + 'name')
        name_element.text = script.get_admin_name()
        code_element = etree.SubElement(script_element, EATS + 'code')
        code_element.text = script.get_code()
        separator_element = etree.SubElement(script_element, EATS + 'separator')
        separator_element.text = script.separator
