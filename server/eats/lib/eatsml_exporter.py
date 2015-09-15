from lxml import etree

from eats.constants import EATS, EATS_NAMESPACE, XML
from eats.lib.eatsml_handler import EATSMLHandler
from eats.models import Authority, Calendar, DatePeriod, DateType, Entity, EntityRelationshipType, EntityType, Language, NamePartType, NameType, Script


NSMAP = {None: EATS_NAMESPACE}


class EATSMLExporter (EATSMLHandler):

    def __init__ (self, topic_map):
        super(EATSMLExporter, self).__init__(topic_map)
        self._topic_map = topic_map
        self._infrastructure_required = {
            'authority': set(),
            'calendar': set(),
            'date_period': set(),
            'date_type': set(),
            'entity_relationship_type': set(),
            'entity_type': set(),
            'language': set(),
            'name_part_type': set(),
            'name_type': set(),
            'script': set(),
            }
        self._entities_required = set()
        self._user_authority = None
        self._user_language = None
        self._user_script = None

    def export_full (self):
        """Returns an XML tree of all EATS data (infrastructure and
        entities) exported into EATSML."""
        root = etree.Element(EATS + 'collection', nsmap=NSMAP)
        entities = Entity.objects.all()
        if entities:
            self._export_entities(entities, root)
        # All infrastructure must be exported, not just that which is
        # required by the existing entities.
        self._infrastructure_required['authority'] = set(
            Authority.objects.all())
        self._infrastructure_required['calendar'] = set(Calendar.objects.all())
        self._infrastructure_required['date_period'] = set(
            DatePeriod.objects.all())
        self._infrastructure_required['date_type'] = set(DateType.objects.all())
        self._infrastructure_required['entity_relationship_type'] = \
            set(EntityRelationshipType.objects.all())
        self._infrastructure_required['entity_type'] = set(
            EntityType.objects.all())
        self._infrastructure_required['language'] = set(Language.objects.all())
        self._infrastructure_required['name_part_type'] = set(
            NamePartType.objects.all())
        self._infrastructure_required['name_type'] = set(NameType.objects.all())
        self._infrastructure_required['script'] = set(Script.objects.all())
        self._export_infrastructure(root)
        tree = root.getroottree()
        self._validate(tree)
        return tree

    def export_entities (self, entities, user=None):
        """Returns an XML tree of `entities` exported into EATSML.

        If `user` is specified, the preferred name of each entity is
        annotated.

        :param entities: entities to export
        :type entities: `list` or `QuerySet` of `Entity`s
        :param user: optional user
        :type user: `EATSUser`
        :rtype: `ElementTree`

        """
        root = etree.Element(EATS + 'collection', nsmap=NSMAP)
        if user is not None:
            self._user_authority = user.get_current_authority()
            self._user_language = user.get_language()
            self._user_script = user.get_script()
        if entities:
            self._export_entities(entities, root)
        # Export any required infrastructure elements.
        self._export_infrastructure(root)
        tree = root.getroottree()
        self._validate(tree)
        return tree

    def _export_entities (self, entities, parent):
        """Exports `entities`.

        :param entities: entities to export
        :type entities: `list` or `QuerySet` of `Entity`s
        :param parent: XML element that will contain the exported entities
        :type parent: `Element`

        """
        entities_element = etree.SubElement(parent, EATS + 'entities')
        for entity in entities:
            self._export_entity(entity, entities_element)
        # Export any additional entities that might need to be
        # exported (due to being referenced from another entity).
        for entity in self._entities_required:
            if entity not in entities:
                self._export_entity(entity, entities_element, True)

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
        entity_id = str(entity.get_id())
        entity_element.set(XML + 'id', 'entity-%s' % entity_id)
        entity_element.set('eats_id', entity_id)
        url = entity.get_eats_subject_identifier().to_external_form()
        entity_element.set('url', url)
        if extra:
            entity_element.set('related_entity', 'true')
        else:
            # Only export relationships for primary entities (those
            # specifically requested to be exported); otherwise there
            # is the possibility of recursion.
            self._export_entity_relationship_property_assertions(
                entity, entity_element)
        self._export_entity_type_property_assertions(entity, entity_element)
        self._export_existence_property_assertions(entity, entity_element)
        self._export_name_property_assertions(entity, entity_element)
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
        assertion_element = etree.SubElement(parent, EATS +
                                             'entity_relationship')
        authority = assertion.authority
        assertion_element.set('authority', 'authority-%d' % authority.get_id())
        certainty = assertion.certainty
        if certainty == self._topic_map.property_assertion_full_certainty:
            certainty_value = 'full'
        else:
            certainty_value = 'none'
        assertion_element.set('certainty', certainty_value)
        assertion_element.set('eats_id', str(assertion.get_id()))
        relationship_type = assertion.entity_relationship_type
        assertion_element.set(
            'entity_relationship_type', 'entity_relationship_type-%d' %
            relationship_type.get_id())
        domain_entity = assertion.domain_entity
        range_entity = assertion.range_entity
        assertion_element.set('domain_entity', 'entity-%d' %
                              domain_entity.get_id())
        assertion_element.set('range_entity', 'entity-%d' %
                              range_entity.get_id())
        self._infrastructure_required['authority'].add(authority)
        self._infrastructure_required['entity_relationship_type'].add(
            relationship_type)
        if domain_entity == entity:
            self._entities_required.add(range_entity)
        else:
            self._entities_required.add(domain_entity)
        self._export_dates(assertion, assertion_element)

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
        assertion_element = etree.SubElement(parent, EATS + 'entity_type')
        authority = assertion.authority
        entity_type = assertion.entity_type
        assertion_element.set('authority', 'authority-%d' % authority.get_id())
        assertion_element.set('eats_id', str(assertion.get_id()))
        assertion_element.set('entity_type', 'entity_type-%d' %
                              entity_type.get_id())
        self._infrastructure_required['authority'].add(authority)
        self._infrastructure_required['entity_type'].add(entity_type)
        self._export_dates(assertion, assertion_element)

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
        assertion_element = etree.SubElement(parent, EATS + 'existence')
        authority = existence.authority
        assertion_element.set('authority', 'authority-%d' % authority.get_id())
        assertion_element.set('eats_id', str(existence.get_id()))
        self._infrastructure_required['authority'].add(authority)
        self._export_dates(existence, assertion_element)

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
            preferred_name = None
            if self._user_authority or self._user_language or self._user_script:
                preferred_name = entity.get_preferred_name(
                    self._user_authority, self._user_language,
                    self._user_script)
        for name in names:
            is_preferred = False
            if name == preferred_name:
                is_preferred = True
            self._export_name_property_assertion(name, names_element,
                                                 is_preferred)

    def _export_name_property_assertion (self, assertion, parent, is_preferred):
        """Exports the name in `assertion`.

        :param assertion: name to export
        :type assertion: `NamePropertyAssertion`
        :param parent: XML element that will contain the exported name
        :type parent: `Element`
        :param is_preferred: indicates if this `assertion` is
          preferred by the exporter
        :type is_preferred: `bool`

        """
        name_element = etree.SubElement(parent, EATS + 'name')
        authority = assertion.authority
        name = assertion.name
        name_type = name.name_type
        language = name.language
        script = name.script
        name_element.set('authority', 'authority-%d' % authority.get_id())
        name_element.set('eats_id', str(assertion.get_id()))
        name_element.set('is_preferred', str(assertion.is_preferred).lower())
        name_element.set('language', 'language-%d' % language.get_id())
        name_element.set('name_type', 'name_type-%d' % name_type.get_id())
        name_element.set('script', 'script-%d' % script.get_id())
        if is_preferred:
            name_element.set('user_preferred', 'true')
        self._infrastructure_required['authority'].add(authority)
        self._infrastructure_required['language'].add(language)
        self._infrastructure_required['script'].add(script)
        self._infrastructure_required['name_type'].add(name_type)
        assembled_form_element = etree.SubElement(name_element,
                                                  EATS + 'assembled_form')
        assembled_form_element.text = name.assembled_form
        display_form_element = etree.SubElement(name_element,
                                                EATS + 'display_form')
        display_form_element.text = name.display_form
        name_parts_data = name.get_name_parts()
        name_part_types = []
        if name_parts_data:
            name_parts_element = etree.SubElement(name_element,
                                                  EATS + 'name_parts')
            name_part_types = language.name_part_types
        # To maintain correct order of name parts, export them in type
        # order based on language, and then output any remaining in
        # essentially random order.
        for name_part_type in name_part_types:
            name_parts = name_parts_data.pop(name_part_type, None)
            if name_parts is not None:
                self._export_name_parts(name_part_type, name_parts,
                                        name_parts_element)
        for name_part_type, name_parts in list(name_parts_data.items()):
            self._export_name_parts(name_part_type, name_parts,
                                    name_parts_element)
        self._export_dates(assertion, name_element)

    def _export_name_parts (self, name_part_type, name_parts,
                            name_parts_element):
        name_part_type_id = name_part_type.get_id()
        self._infrastructure_required['name_part_type'].add(name_part_type)
        for name_part in name_parts:
            self._export_name_part(name_part_type_id, name_part,
                                   name_parts_element)

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
        note_element.set('eats_id', str(assertion.get_id()))
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
        subject_identifiers = entity.get_eats_subject_identifiers()
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
        subject_identifier_element.set('eats_id', str(assertion.get_id()))
        subject_identifier_element.text = assertion.subject_identifier
        self._infrastructure_required['authority'].add(authority)

    def _export_dates (self, assertion, parent):
        """Exports the dates associated with `assertion`.

        :param assertion: property assertion whose dates will be exported
        :type assertion: `PropertyAssertion`
        :param parent: XML element that will contain the exported dates
        :type parent; `Element`

        """
        dates = assertion.get_dates()
        if dates:
            dates_element = etree.SubElement(parent, EATS + 'dates')
        for date in dates:
            self._export_date(date, dates_element)

    def _export_date (self, date, parent):
        """Exports `date`, appending it to `parent`.

        :param date: date to export
        :type date: `Date`
        :param parent: XML element that will contain the exported date
        :type parent: `Element`

        """
        date_element = etree.SubElement(parent, EATS + 'date')
        date_period = date.period
        date_element.set('date_period', 'date_period-%d' % date_period.get_id())
        self._infrastructure_required['date_period'].add(date_period)
        assembled_form_element = etree.SubElement(date_element, EATS +
                                                  'assembled_form')
        assembled_form_element.text = date.assembled_form
        date_parts_element = etree.SubElement(date_element, EATS + 'date_parts')
        for date_part_name in date.date_part_names:
            date_part = getattr(date, date_part_name)
            self._export_date_part(date_part, date_part_name,
                                   date_parts_element)

    def _export_date_part (self, date_part, date_part_name, parent):
        """Exports `date_part` (if it has content), appending it to
        `parent`.

        :param date_part: date part to export
        :type date_part: `DatePart`
        :param date_part_name: name of date part
        :type date_part_name: `str`
        :param parent: XML element that will contain the exported date part
        :type parent: `Element`

        """
        assembled_form = date_part.assembled_form
        if assembled_form:
            date_part_element = etree.SubElement(parent, EATS + 'date_part')
            date_part_element.set('type', date_part_name)
            calendar = date_part.calendar
            date_part_element.set('calendar', 'calendar-%d' % calendar.get_id())
            self._infrastructure_required['calendar'].add(calendar)
            date_type = date_part.date_type
            date_part_element.set('date_type', 'date_type-%d' %
                                  date_type.get_id())
            self._infrastructure_required['date_type'].add(date_type)
            certainty = date_part.certainty
            if certainty == self._topic_map.date_full_certainty:
                certainty_value = 'full'
            else:
                certainty_value = 'none'
            date_part_element.set('certainty', certainty_value)
            raw_element = etree.SubElement(date_part_element, EATS + 'raw')
            raw_element.text = date_part.get_value()
            normalised_element = etree.SubElement(date_part_element, EATS +
                                                  'normalised')
            normalised_element.text = date_part.get_normalised_value()

    def export_infrastructure (self, user=None):
        """Returns an XML tree of infrastructural elements, exported
        into EATSML.

        If `user` is specified, the export is limited to those
        authorities and their associated elements that are editable by
        the user.

        :param user: optional user
        :type user: `EATSUser`
        :rtype: `ElementTree`

        """
        root = etree.Element(EATS + 'collection', nsmap=NSMAP)
        if user is not None:
            self._user_authority = user.get_current_authority()
            self._user_language = user.get_language()
            self._user_script = user.get_script()
            authorities = user.editable_authorities.all()
            calendars = []
            date_periods = []
            date_types = []
            entity_relationship_types = []
            entity_types = []
            languages = []
            name_part_types = []
            name_types = []
            scripts = []
            for authority in authorities:
                calendars.extend(authority.get_calendars())
                date_periods.extend(authority.get_date_periods())
                date_types.extend(authority.get_date_types())
                entity_relationship_types.extend(authority.get_entity_relationship_types())
                entity_types.extend(authority.get_entity_types())
                languages.extend(authority.get_languages())
                name_part_types.extend(authority.get_name_part_types())
                name_types.extend(authority.get_name_types())
                scripts.extend(authority.get_scripts())
        else:
            authorities = Authority.objects.all()
            calendars = Calendar.objects.all()
            date_periods = DatePeriod.objects.all()
            date_types = DateType.objects.all()
            entity_relationship_types = EntityRelationshipType.objects.all()
            entity_types = EntityType.objects.all()
            languages = Language.objects.all()
            name_part_types = NamePartType.objects.all()
            name_types = NameType.objects.all()
            scripts = Script.objects.all()
        # Turn these lists of objects into sets so that they can be
        # later intersected with another set of objects.
        self._infrastructure_required['authority'] = set(authorities)
        self._infrastructure_required['calendar'] = set(calendars)
        self._infrastructure_required['date_period'] = set(date_periods)
        self._infrastructure_required['date_type'] = set(date_types)
        self._infrastructure_required['entity_relationship_type'] = \
            set(entity_relationship_types)
        self._infrastructure_required['entity_type'] = set(entity_types)
        self._infrastructure_required['language'] = set(languages)
        self._infrastructure_required['name_part_type'] = set(name_part_types)
        self._infrastructure_required['name_type'] = set(name_types)
        self._infrastructure_required['script'] = set(scripts)
        self._export_infrastructure(root)
        tree = root.getroottree()
        self._validate(tree)
        return tree

    def _export_infrastructure (self, parent):
        """Exports required infrastructure elements, appending them to
        `parent`.

        :param parent: XML element that will contain the export infrastructure
        :type parent: `Element`

        """
        authorities = self._infrastructure_required['authority']
        self._export_authorities(authorities, parent)
        # Order each set of items by admin name.
        for key, objects in list(self._infrastructure_required.items()):
            ordered_objects = list(objects)
            ordered_objects.sort(key=lambda item: item.get_admin_name())
            self._infrastructure_required[key] = ordered_objects
        calendars = self._infrastructure_required['calendar']
        self._export_calendars(calendars, parent)
        date_periods = self._infrastructure_required['date_period']
        self._export_date_periods(date_periods, parent)
        date_types = self._infrastructure_required['date_type']
        self._export_date_types(date_types, parent)
        entity_relationship_types = self._infrastructure_required['entity_relationship_type']
        self._export_entity_relationship_types(entity_relationship_types,
                                               parent)
        entity_types = self._infrastructure_required['entity_type']
        self._export_entity_types(entity_types, parent)
        languages = self._infrastructure_required['language']
        self._export_languages(languages, parent)
        name_part_types = self._infrastructure_required['name_part_type']
        self._export_name_part_types(name_part_types, parent)
        name_types = self._infrastructure_required['name_type']
        self._export_name_types(name_types, parent)
        scripts = self._infrastructure_required['script']
        self._export_scripts(scripts, parent)
        # If there is an entities element that has already been
        # created, move it to after the infrastructure elements.
        if len(parent) and parent[0].tag == EATS + 'entities':
            parent.append(parent[0])

    def _export_authorities (self, authorities, parent):
        """Exports `authorities`, appending them to `parent`.

        :param authorities: authorities to export
        :type authorities: `set` of `Authority`s
        :param parent: XML element that will contain the exported authorities
        :type parent: `Element`

        """
        authorities = list(authorities)
        authorities.sort(key=lambda item: item.get_admin_name())
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
        authority_id = str(authority.get_id())
        authority_element.set(XML + 'id', 'authority-%s' % authority_id)
        authority_element.set('eats_id', authority_id)
        if authority == self._user_authority:
            authority_element.set('user_preferred', 'true')
        name_element = etree.SubElement(authority_element, EATS + 'name')
        name_element.text = authority.get_admin_name()
        calendars = authority.get_calendars()
        self._export_authority_infrastructure(
            'calendar', 'calendars', 'calendar', calendars, authority_element)
        date_periods = authority.get_date_periods()
        self._export_authority_infrastructure(
            'date_period', 'date_periods', 'date_period', date_periods,
            authority_element)
        date_types = authority.get_date_types()
        self._export_authority_infrastructure(
            'date_type', 'date_types', 'date_type', date_types,
            authority_element)
        relationship_types = authority.get_entity_relationship_types()
        self._export_authority_infrastructure(
            'entity_relationship_type', 'entity_relationship_types',
            'entity_relationship_type', relationship_types, authority_element)
        entity_types = authority.get_entity_types()
        self._export_authority_infrastructure(
            'entity_type', 'entity_types', 'entity_type', entity_types,
            authority_element)
        languages = authority.get_languages()
        self._export_authority_infrastructure(
            'language', 'languages', 'language', languages, authority_element)
        name_part_types = authority.get_name_part_types()
        self._export_authority_infrastructure(
            'name_part_type', 'name_part_types', 'name_part_type',
            name_part_types, authority_element)
        name_types = authority.get_name_types()
        self._export_authority_infrastructure(
            'name_type', 'name_types', 'name_type', name_types,
            authority_element)
        scripts = authority.get_scripts()
        self._export_authority_infrastructure('script', 'scripts', 'script',
                                              scripts, authority_element)

    def _export_authority_infrastructure (self, infrastructure_element_name,
                                          container_element_name, element_name,
                                          authority_items, parent):
        """Exports a type of infrastructure as it related to an authority.

        :param infrastructure_element_name: name of the infrastructure
          element to export
        :type infrastructure_element_name: `str`
        :param container_element_name: name of the element to contain
          the exported infrastructure elements
        :type container_element_name: `str`
        :param element_name: name of the element for each infrastructure element
        :type element_name: `str`
        :param authority_items: infrastructure items associated with
          the authority
        :type authority_items: `list` of infrastructure items
        :param parent: XML element that will contain the exported elements
        :type parent: `Element`

        """
        # Only export those items that are required, and only those
        # that are associated with the current authority.
        all_items = self._infrastructure_required[infrastructure_element_name]
        items = all_items & set(authority_items)
        if items:
            container_element = etree.SubElement(parent, EATS +
                                                 container_element_name)
            items = list(items)
            items.sort(key=lambda item: item.get_admin_name())
        for item in items:
            element = etree.SubElement(container_element, EATS +
                                       element_name)
            element.set('ref', '%s-%d' % (infrastructure_element_name,
                                          item.get_id()))

    def _export_calendars (self, calendars, parent):
        """Exports `calendars`, appending them to `parent`.

        :param calendars: date periods to export
        :type calendars: `set` of `Calendar`s
        :param parent: XML element that will contain the exported date periods
        :type parent: `Element`

        """
        if calendars:
            calendars_element = etree.SubElement(parent, EATS +
                                                    'calendars')
        for calendar in calendars:
            self._export_calendar(calendar, calendars_element)

    def _export_calendar (self, calendar, parent):
        """Exports `calendar`, appending it to `parent`.

        :param calendar: calendar to export
        :type calendar: `Calendar`
        :param parent: XML element that will contain the exported calendar
        :type parent: `Element`

        """
        calendar_element = etree.SubElement(parent, EATS + 'calendar')
        calendar_id = str(calendar.get_id())
        calendar_element.set(XML + 'id', 'calendar-%s' % calendar_id)
        calendar_element.set('eats_id', calendar_id)
        name_element = etree.SubElement(calendar_element, EATS + 'name')
        name_element.text = calendar.get_admin_name()

    def _export_date_periods (self, date_periods, parent):
        """Exports `date_periods`, appending them to `parent`.

        :param date_periods: date periods to export
        :type date_periods: `set` of `DatePeriod`s
        :param parent: XML element that will contain the exported date periods
        :type parent: `Element`

        """
        if date_periods:
            date_periods_element = etree.SubElement(parent, EATS +
                                                    'date_periods')
        for date_period in date_periods:
            self._export_date_period(date_period, date_periods_element)

    def _export_date_period (self, date_period, parent):
        """Exports `date_period`, appending it to `parent`.

        :param date_period: date period to export
        :type date_period: `DatePeriod`
        :param parent: XML element that will contain the exported date period
        :type parent: `Element`

        """
        date_period_element = etree.SubElement(parent, EATS + 'date_period')
        date_period_id = str(date_period.get_id())
        date_period_element.set(XML + 'id', 'date_period-%s' % date_period_id)
        date_period_element.set('eats_id', date_period_id)
        name_element = etree.SubElement(date_period_element, EATS + 'name')
        name_element.text = date_period.get_admin_name()

    def _export_date_types (self, date_types, parent):
        """Exports `date_types`, appending them to `parent`.

        :param date_types: date types to export
        :type date_types: `set` of `DateType`s
        :param parent: XML element that will contain the exported date types
        :type parent: `Element`

        """
        if date_types:
            date_types_element = etree.SubElement(parent, EATS +
                                                  'date_types')
        for date_type in date_types:
            self._export_date_type(date_type, date_types_element)

    def _export_date_type (self, date_type, parent):
        """Exports `date_type`, appending it to `parent`.

        :param date_type: date type to export
        :type date_type: `DateType`
        :param parent: XML element that will contain the exported date type
        :type parent: `Element`

        """
        date_type_element = etree.SubElement(parent, EATS + 'date_type')
        date_type_id = str(date_type.get_id())
        date_type_element.set(XML + 'id', 'date_type-%s' % date_type_id)
        date_type_element.set('eats_id', date_type_id)
        name_element = etree.SubElement(date_type_element, EATS + 'name')
        name_element.text = date_type.get_admin_name()

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
        relationship_type_id = str(relationship_type.get_id())
        relationship_type_element.set(XML + 'id', 'entity_relationship_type-%s'
                                      % relationship_type_id)
        relationship_type_element.set('eats_id', relationship_type_id)
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
        entity_type_id = str(entity_type.get_id())
        entity_type_element.set(XML + 'id', 'entity_type-%s' % entity_type_id)
        entity_type_element.set('eats_id', entity_type_id)
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
        language_id = str(language.get_id())
        language_element.set(XML + 'id', 'language-%s' % language_id)
        language_element.set('eats_id', language_id)
        if language == self._user_language:
            language_element.set('user_preferred', 'true')
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
        name_part_types_element = etree.Element(EATS + 'name_part_types')
        for name_part_type in name_part_types:
            if name_part_type in self._infrastructure_required['name_part_type']:
                name_part_type_element = etree.SubElement(
                    name_part_types_element, EATS + 'name_part_type')
                name_part_type_element.set('ref', 'name_part_type-%d' %
                                           name_part_type.get_id())
        if len(name_part_types_element):
            parent.append(name_part_types_element)

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
        name_type_id = str(name_type.get_id())
        name_type_element.set(XML + 'id', 'name_type-%s' % name_type_id)
        name_type_element.set('eats_id', name_type_id)
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
        name_part_type_id = str(name_part_type.get_id())
        name_part_type_element.set(XML + 'id', 'name_part_type-%s' %
                                   name_part_type_id)
        name_part_type_element.set('eats_id', name_part_type_id)
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
        script_id = str(script.get_id())
        script_element.set(XML + 'id', 'script-%s' % script_id)
        script_element.set('eats_id', script_id)
        if script == self._user_script:
            script_element.set('user_preferred', 'true')
        name_element = etree.SubElement(script_element, EATS + 'name')
        name_element.text = script.get_admin_name()
        code_element = etree.SubElement(script_element, EATS + 'code')
        code_element.text = script.get_code()
        separator_element = etree.SubElement(script_element, EATS + 'separator')
        separator_element.text = script.separator
