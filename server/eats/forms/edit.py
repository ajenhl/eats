from django import forms
from django.conf import settings
from django.forms.formsets import formset_factory, BaseFormSet

import selectable.forms as selectable

from eats.constants import FORWARD_RELATIONSHIP_MARKER, \
    REVERSE_RELATIONSHIP_MARKER, UNNAMED_ENTITY_NAME
from eats.lookups import EntityLookup
from eats.models import Calendar, DatePeriod, DateType, EntityRelationshipType, EntityType, Language, NamePart, NamePartType, NameType, Script


class PropertyAssertionFormSet (BaseFormSet):

    """Base class for the formsets of specific property assertion types.

    This code is heavily influenced by Django's BaseModelFormSet,
    since we are dealing with objects that are tied to models, just in
    an aggregated way that makes using ModelFormSets impossible.

    """

    def __init__ (self, topic_map, entity, authority, instances, **kwargs):
        self.topic_map = topic_map
        self.entity = entity
        self.authority = authority
        self.instances = instances or []
        super(PropertyAssertionFormSet, self).__init__(**kwargs)

    def _construct_form (self, i, **kwargs):
        kwargs.update({'topic_map': self.topic_map, 'entity': self.entity,
                       'authority': self.authority})
        if self.is_bound and i < self.initial_form_count():
            id_key = '%s-%s' % (self.add_prefix(i), 'assertion')
            id = self.data[id_key]
            kwargs['instance'] = self._existing_object(id)
        if i < self.initial_form_count() and not kwargs.get('instance'):
            kwargs['instance'] = self.instances[i]
        return super(PropertyAssertionFormSet, self)._construct_form(
            i, **kwargs)

    def _existing_object (self, id):
        if not hasattr(self, '_object_dict'):
            self._object_dict = dict([(o.get_id(), o) for o in self.instances])
        return self._object_dict.get(id)

    def initial_form_count (self):
        """Returns the number of forms that are required in this FormSet."""
        if not self.data:
            return len(self.instances)
        return super(PropertyAssertionFormSet, self).initial_form_count()

    def save (self):
        """Saves property assertion instances for every form, adding
        and changing instances as necessary, and returns a list of
        instances."""
        return self.save_existing_assertions() + self.save_new_assertions()

    def save_new (self, form):
        return form.save()

    def save_existing (self, form, assertion):
        return form.save()

    def save_existing_assertions (self):
        if not self.instances:
            return []
        saved_assertions = []
        for form in self.initial_forms:
            id_value = form.fields['assertion'].clean(form['assertion'].value())
            obj = self._existing_object(id_value)
            if self.can_delete and self._should_delete_form(form):
                form.delete()
                continue
            if form.has_changed():
                saved_assertions.append(self.save_existing(form, obj))
        return saved_assertions

    def save_new_assertions (self):
        self.new_objects = []
        for form in self.extra_forms:
            if not form.has_changed():
                continue
            if self.can_delete and self._should_delete_form(form):
                continue
            self.new_objects.append(self.save_new(form))
        return self.new_objects


class ExistenceAssertionFormSet (PropertyAssertionFormSet):

    pass


class EntityRelationshipAssertionFormSet (PropertyAssertionFormSet):

    def __init__ (self, **kwargs):
        self.relationship_type_choices = kwargs.pop('relationship_type_choices')
        super(EntityRelationshipAssertionFormSet, self).__init__(**kwargs)

    def _construct_form (self, i, **kwargs):
        kwargs.update({'relationship_type_choices':
                           self.relationship_type_choices})
        return super(EntityRelationshipAssertionFormSet, self)._construct_form(
            i, **kwargs)


class EntityTypeAssertionFormSet (PropertyAssertionFormSet):

    def __init__ (self, **kwargs):
        self.entity_type_choices = kwargs.pop('entity_type_choices')
        super(EntityTypeAssertionFormSet, self).__init__(**kwargs)

    def _construct_form (self, i, **kwargs):
        kwargs.update({'entity_type_choices': self.entity_type_choices})
        return super(EntityTypeAssertionFormSet, self)._construct_form(
            i, **kwargs)


class NameAssertionFormSet (PropertyAssertionFormSet):

    def __init__ (self, **kwargs):
        self.name_part_type_choices = kwargs.pop('name_part_type_choices')
        self.name_type_choices = kwargs.pop('name_type_choices')
        self.language_choices = kwargs.pop('language_choices')
        self.script_choices = kwargs.pop('script_choices')
        super(NameAssertionFormSet, self).__init__(**kwargs)

    def _construct_form (self, i, **kwargs):
        kwargs.update({'name_type_choices': self.name_type_choices,
                       'language_choices': self.language_choices,
                       'script_choices': self.script_choices})
        form = super(NameAssertionFormSet, self)._construct_form(
            i, **kwargs)
        try:
            instance = self.instances[i]
            instances = [[name_part_type, name_parts] for name_part_type,
                         name_parts in list(instance.name.get_name_parts().items())]
            # QAZ: It would be nice to order these instances by the
            # name part type order associated with the language of
            # this name.
        except IndexError:
            instances = None
        name_part_data = {
            'topic_map': self.topic_map, 'authority': self.authority,
            'data': self.data or None, 'instances': instances,
            'name_prefix': self.add_prefix(i),
            'name_part_type_choices': self.name_part_type_choices,
            'language_choices': self.language_choices,
            'script_choices': self.script_choices
            }
        form.name_part_formset = NamePartFormSet(**name_part_data)
        return form

    def is_valid (self):
        """Returns True if every form in self.forms is valid and if each
        form's name part formset is valid."""
        if not self.is_bound:
            return False
        forms_valid = True
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            # is_valid is called now so that cleaned_data exists when
            # checked in _should_delete_form.
            is_valid = form.is_valid()
            if self.can_delete:
                if self._should_delete_form(form):
                    # This form is going to be deleted so any of its errors
                    # should not cause the entire formset to be invalid.
                    continue
            forms_valid &= is_valid
            form.name_part_formset.set_name_language(form.cleaned_data.get(
                'language'))
            if not form.name_part_formset.is_valid():
                forms_valid = False
        return forms_valid and not bool(self.non_form_errors())

    def save_existing_assertions (self):
        if not self.instances:
            return []
        saved_assertions = []
        for form in self.initial_forms:
            id_value = form.fields['assertion'].clean(
                form['assertion'].value())
            obj = self._existing_object(id_value)
            if self.can_delete and self._should_delete_form(form):
                form.delete()
                continue
            if form.has_changed():
                saved_assertions.append(self.save_existing(form, obj))
            form.name_part_formset.save(obj)
        return saved_assertions

    def save_new_assertions (self):
        self.new_objects = []
        for form in self.extra_forms:
            if not form.has_changed():
                continue
            if self.can_delete and self._should_delete_form(form):
                continue
            assertion = self.save_new(form)
            self.new_objects.append(assertion)
            form.name_part_formset.save(assertion)
        return self.new_objects


class NoteAssertionFormSet (PropertyAssertionFormSet):

    pass


class SubjectIdentifierAssertionFormSet (PropertyAssertionFormSet):

    def clean (self):
        if self.is_valid():
            # Ensure that the subject identifiers across all the forms in
            # the formset are unique.
            subject_identifier_values = []
            for form_data in self.cleaned_data:
                for field, value in list(form_data.items()):
                    if field == 'subject_identifier' and value:
                        subject_identifier_values.append(value)
            if len(subject_identifier_values) != len(set(
                    subject_identifier_values)):
                raise forms.ValidationError(
                    'Subject identifier URLs must be unique to an authority')


class NamePartInlineFormSet (BaseFormSet):

    def __init__ (self, topic_map, authority, name_prefix, instances,
                  name_part_type_choices, language_choices, script_choices,
                  **kwargs):
        self.topic_map = topic_map
        self.authority = authority
        self.name_prefix = name_prefix
        self.instances = instances or []
        self.name_part_type_choices = name_part_type_choices
        self.language_choices = language_choices
        self.script_choices = script_choices
        prefix = name_prefix + '-name_parts'
        super(NamePartInlineFormSet, self).__init__(prefix=prefix, **kwargs)

    def _construct_form (self, i, **kwargs):
        kwargs.update({'topic_map': self.topic_map, 'authority': self.authority,
                       'name_part_type_choices': self.name_part_type_choices,
                       'language_choices': self.language_choices,
                       'script_choices': self.script_choices})
        if self.is_bound and i < self.initial_form_count():
            # Get the name parts of this particular type.
            id_key = '%s-%s' % (self.add_prefix(i), 'name_part_type')
            kwargs['instance'] = self._existing_object(self.data[id_key])
        if i < self.initial_form_count() and not kwargs.get('instance'):
            kwargs['instance'] = self.instances[i]
        return super(NamePartInlineFormSet, self)._construct_form(i, **kwargs)

    def _existing_object (self, id):
        if not hasattr(self, '_object_dict'):
            self._object_dict = dict([(o[0].get_id(), o)
                                      for o in self.instances])
        return self._object_dict.get(id)

    def initial_form_count (self):
        """Returns the number of forms that are required in this FormSet."""
        if not self.data:
            return len(self.instances)
        return super(NamePartInlineFormSet, self).initial_form_count()

    def save (self, name_assertion):
        """Saves name part instances for every form, adding and
        changing instances as necessary, and returns a list of
        instances."""
        return self.save_existing(name_assertion) + \
            self.save_new(name_assertion)

    def save_existing (self, name_assertion):
        if not self.instances:
            return []
        saved_assertions = []
        for form in self.initial_forms:
            if self.can_delete and self._should_delete_form(form):
                form.delete()
                continue
            if form.has_changed():
                saved_assertions.append(form.save(name_assertion))
        return saved_assertions

    def save_new (self, name_assertion):
        self.new_objects = []
        for form in self.extra_forms:
            if not form.has_changed():
                continue
            if self.can_delete and self._should_delete_form(form):
                continue
            self.new_objects.append(form.save(name_assertion))
        return self.new_objects

    def set_name_language (self, language):
        """Sets the language of the parent name for the forms in this
        formset."""
        for form in self.initial_forms + self.extra_forms:
            form.set_name_language(language)


class CreateEntityForm (forms.Form):

    authority = forms.ChoiceField(choices=[])

    def __init__ (self, topic_map, authorities, *args, **kwargs):
        super(CreateEntityForm, self).__init__(*args, **kwargs)
        self.fields['authority'].choices = create_choice_list(
            topic_map, authorities, True)


class CurrentAuthorityForm (forms.Form):

    current_authority = forms.ChoiceField(choices=[])

    def __init__ (self, topic_map, editable_authorities, data=None, **kwargs):
        super(CurrentAuthorityForm, self).__init__(data, **kwargs)
        self.fields['current_authority'].choices = create_choice_list(
            topic_map, editable_authorities)[1:]


class PropertyAssertionForm (forms.Form):

    assertion = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def __init__ (self, topic_map, entity, authority, instance=None, **kwargs):
        self.topic_map = topic_map
        self.entity = entity
        self.authority = authority
        self.instance = instance
        if instance is None:
            object_data = {}
        else:
            object_data = self._assertion_to_dict(instance)
        super(PropertyAssertionForm, self).__init__(initial=object_data,
                                                    **kwargs)

    def _assertion_to_dict (self, assertion):
        """Returns a dictionary containing the data in `assertion`
        suitable for passing as a Form's `initial` keyword argument.

        :param assertion: property assertion
        :type assertion: `PropertyAssertion`
        :rtype: dict

        """
        return {'assertion': assertion.get_id()}

    def _get_construct (self, identifier, proxy):
        """Returns the construct specified by `identifer`.

        :param identifier: identifier of the construct to return
        :type name: string
        :param proxy: Django proxy model
        :type proxy: class
        :rtype: proxy object

        """
        return proxy.objects.get_by_identifier(identifier)

    def delete (self):
        """Deletes the assertion."""
        self.instance.remove()

    def save (self):
        raise NotImplementedError


class ExistenceForm (PropertyAssertionForm):

    authority = forms.ChoiceField(choices=[])

    def __init__ (self, topic_map, entity, authority, instance=None, **kwargs):
        super(ExistenceForm, self).__init__(
            topic_map, entity, authority, instance, **kwargs)
        authority_choices = create_choice_list(topic_map, [authority])
        if instance is not None:
            authority_choices = authority_choices[1:]
        self.fields['authority'].choices = authority_choices

    def _assertion_to_dict (self, assertion):
        data = super(ExistenceForm, self)._assertion_to_dict(assertion)
        data['authority'] = assertion.authority.get_id()
        return data

    def save (self):
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_existence_property_assertion(self.authority)
        else:
            # Update an existing assertion - a noop.
            pass


class EntityRelationshipForm (PropertyAssertionForm):

    relationship_type = forms.ChoiceField(choices=[])
    related_entity = selectable.AutoCompleteSelectField(
        lookup_class=EntityLookup)
    certainty = forms.BooleanField(required=False)

    def __init__ (self, *args, **kwargs):
        relationship_type_choices = kwargs.pop('relationship_type_choices')
        super(EntityRelationshipForm, self).__init__(*args, **kwargs)
        self.fields['relationship_type'].choices = relationship_type_choices

    def _assertion_to_dict (self, assertion):
        data = super(EntityRelationshipForm, self)._assertion_to_dict(assertion)
        relationship_id = str(assertion.entity_relationship_type.get_id())
        direction_marker = FORWARD_RELATIONSHIP_MARKER
        related_entity = assertion.range_entity
        if self.entity == assertion.range_entity:
            direction_marker = REVERSE_RELATIONSHIP_MARKER
            related_entity = assertion.domain_entity
        data['relationship_type'] = relationship_id + direction_marker
        data['related_entity'] = related_entity.get_id()
        if assertion.certainty == \
                self.topic_map.property_assertion_full_certainty:
            certainty = True
        else:
            certainty = False
        data['certainty'] = certainty
        return data

    def save (self):
        relationship_type_id = self.cleaned_data['relationship_type']
        relationship_type = EntityRelationshipType.objects.get_by_identifier(
            relationship_type_id[:-1])
        # The autocomplete selection library, via lookups.py, takes
        # care of retrieving the entity from its id.
        related_entity = self.cleaned_data['related_entity']
        direction = relationship_type_id[-1]
        if direction == FORWARD_RELATIONSHIP_MARKER:
            domain_entity = self.entity
            range_entity = related_entity
        elif direction == REVERSE_RELATIONSHIP_MARKER:
            domain_entity = related_entity
            range_entity = self.entity
        if self.cleaned_data['certainty']:
            certainty = self.topic_map.property_assertion_full_certainty
        else:
            certainty = self.topic_map.property_assertion_no_certainty
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_entity_relationship_property_assertion(
                self.authority, relationship_type, domain_entity, range_entity,
                certainty)
        else:
            # Update an existing assertion.
            self.instance.update(relationship_type, domain_entity, range_entity,
                                 certainty)


class EntityTypeForm (PropertyAssertionForm):

    entity_type = forms.ChoiceField(choices=[])

    def __init__ (self, *args, **kwargs):
        entity_type_choices = kwargs.pop('entity_type_choices')
        super(EntityTypeForm, self).__init__(*args, **kwargs)
        self.fields['entity_type'].choices = entity_type_choices

    def _assertion_to_dict (self, assertion):
        data = super(EntityTypeForm, self)._assertion_to_dict(assertion)
        data['entity_type'] = assertion.entity_type.get_id()
        return data

    def clean (self):
        cleaned_data = super().clean()
        cleaned_data['entity_type'] = self._get_construct(
            cleaned_data['entity_type'], EntityType)
        self.cleaned_data = cleaned_data
        return cleaned_data

    def save (self):
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_entity_type_property_assertion(
                self.authority, self.cleaned_data['entity_type'])
        else:
            # Update an existing assertion.
            self.instance.update(self.cleaned_data['entity_type'])


class NameForm (PropertyAssertionForm):

    name_type = forms.ChoiceField(choices=[])
    language = forms.ChoiceField(choices=[])
    script = forms.ChoiceField(choices=[])
    display_form = forms.CharField(required=False)
    is_preferred = forms.BooleanField(required=False)

    def __init__ (self, *args, **kwargs):
        name_type_choices = kwargs.pop('name_type_choices')
        language_choices = kwargs.pop('language_choices')
        script_choices = kwargs.pop('script_choices')
        super(NameForm, self).__init__(*args, **kwargs)
        self.fields['name_type'].choices = name_type_choices
        self.fields['language'].choices = language_choices
        self.fields['script'].choices = script_choices

    def _assertion_to_dict (self, assertion):
        data = super(NameForm, self)._assertion_to_dict(assertion)
        name = assertion.name
        data['display_form'] = name.display_form
        data['name_type'] = name.name_type.get_id()
        data['language'] = name.language.get_id()
        data['script'] = name.script.get_id()
        data['is_preferred'] = assertion.is_preferred
        return data

    def clean (self):
        cleaned_data = super(NameForm, self).clean()
        data = (('name_type', NameType), ('language', Language),
                ('script', Script))
        for field_name, model in data:
            field_data = cleaned_data.get(field_name)
            if field_data is not None:
                cleaned_data[field_name] = self._get_construct(field_data,
                                                               model)
        # QAZ: Add check that we don't have a name part to add,
        # without this form either representing an existing name
        # instance or being valid to create one.
        self.cleaned_data = cleaned_data
        return cleaned_data

    def save (self):
        name_type = self.cleaned_data['name_type']
        language = self.cleaned_data['language']
        script = self.cleaned_data['script']
        display_form = self.cleaned_data['display_form']
        is_preferred = self.cleaned_data['is_preferred']
        if self.instance is None:
            # Create a new assertion.
            assertion = self.entity.create_name_property_assertion(
                self.authority, name_type, language, script, display_form,
                is_preferred)
        else:
            # Update an existing assertion.
            self.instance.update(name_type, language, script, display_form,
                                 is_preferred)
            assertion = self.instance
        return assertion


class NoteForm (forms.Form):

    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    is_internal = forms.BooleanField(required=False)


class NotePropertyAssertionForm (NoteForm, PropertyAssertionForm):

    def _assertion_to_dict (self, assertion):
        data = super()._assertion_to_dict(assertion)
        data['note'] = assertion.note
        data['is_internal'] = assertion.is_internal
        return data

    def save (self):
        note = self.cleaned_data['note']
        is_internal = self.cleaned_data['is_internal']
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_note_property_assertion(self.authority, note,
                                                       is_internal)
        else:
            # Update an existing assertion.
            self.instance.update(note, is_internal)


class NoteBearingNoteForm (NoteForm):

    def __init__ (self, bearer, data=None, instance=None, **kwargs):
        self.bearer = bearer
        self.instance = instance
        if instance is None:
            initial = {}
        else:
            initial = {'is_internal': instance.is_internal,
                       'note': instance.note}
        super().__init__(data, initial=initial, **kwargs)

    def delete (self):
        self.instance.remove()

    def save (self):
        note_text = self.cleaned_data['note']
        is_internal = self.cleaned_data['is_internal']
        if self.instance is None:
            note = self.bearer.create_note(note_text, is_internal)
        else:
            self.instance.update(note_text, is_internal)
            note = self.instance
        return note.get_id()


class SubjectIdentifierForm (PropertyAssertionForm):

    subject_identifier = forms.URLField()

    def _assertion_to_dict (self, assertion):
        data = super(SubjectIdentifierForm, self)._assertion_to_dict(assertion)
        data['subject_identifier'] = assertion.subject_identifier
        return data

    def clean_subject_identifier (self):
        subject_identifier = self.cleaned_data['subject_identifier']
        duplicate_entities = self.entity.get_duplicate_subject_identifiers(
            subject_identifier, self.authority)
        if duplicate_entities:
            names = []
            for duplicate_entity in duplicate_entities:
                name = duplicate_entity.get_preferred_name(None, None, None)
                try:
                    name_form = name.name.assembled_form
                except AttributeError:
                    name_form = UNNAMED_ENTITY_NAME
                names.append(name_form)
            raise forms.ValidationError(
                'This URL is also used by this authority to identify %s; either the URL is incorrect or these entities should be merged.' % (', '.join(names)))
        return subject_identifier

    def save (self):
        subject_identifier = self.cleaned_data['subject_identifier']
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_subject_identifier_property_assertion(
                self.authority, subject_identifier)
        else:
            # Update an existing assertion.
            self.instance.update(subject_identifier)


class NamePartForm (forms.Form):

    name_part_type = forms.ChoiceField(choices=[])

    def __init__ (self, topic_map, authority, name_part_type_choices,
                  language_choices, script_choices, instance=None, **kwargs):
        self.topic_map = topic_map
        self.authority = authority
        self.language_choices = language_choices
        self.script_choices = script_choices
        self.instance = instance
        self.name_part_fieldsets = []
        if instance is None:
            object_data = {}
        else:
            object_data = self._name_part_to_dict(instance)
        super(NamePartForm, self).__init__(initial=object_data, **kwargs)
        self.fields['name_part_type'].choices = name_part_type_choices
        self._create_form_fields(kwargs.get('data'), object_data)
        self.name_language = None

    def clean (self):
        cleaned_data = super().clean()
        for name, value in list(cleaned_data.items()):
            if not value or name == 'name_part_type':
                cleaned_data[name] = value
            elif name.startswith('name_part_display_form'):
                cleaned_data[name] = value
            else:
                if name.startswith('name_part_language'):
                    model = Language
                elif name.startswith('name_part_script'):
                    model = Script
                elif name.startswith('name_part_id'):
                    model = NamePart
                else:
                    model = None
                if model is not None:
                    cleaned_data[name] = model.objects.get_by_identifier(value)
        self.cleaned_data = cleaned_data
        return cleaned_data

    def clean_name_part_type (self):
        """Validates the name_part_type field, and converts its cleaned form
        into a model instance."""
        name_part_type_id = self.cleaned_data['name_part_type']
        name_part_type = NamePartType.objects.get_by_identifier(
            name_part_type_id)
        if name_part_type not in self.name_language.name_part_types:
            raise forms.ValidationError("The selected name part type is not associated with the name's language")
        return name_part_type

    def _create_form_fields (self, post_data, object_data):
        count = 2
        data = object_data
        field_name = 'name_part_display_form'
        if post_data:
            data = post_data
            field_name = self.add_prefix(field_name)
        for name in data:
            if name.startswith(field_name) and data[name]:
                count += 1
        if count < 3:
            count = 3
        for i in range(count):
            suffix = str(i)
            id_name = 'name_part_id-' + suffix
            display_form_name = 'name_part_display_form-' + suffix
            language_name = 'name_part_language-' + suffix
            script_name = 'name_part_script-' + suffix
            self.fields[id_name] = forms.IntegerField(
                widget=forms.HiddenInput, required=False)
            self.fields[display_form_name] = forms.CharField(
                required=False, widget=forms.TextInput(attrs={'size': 12}))
            self.fields[language_name] = forms.ChoiceField(
                choices=self.language_choices, required=False)
            self.fields[script_name] = forms.ChoiceField(
                choices=self.script_choices, required=False)
            self.name_part_fieldsets.append(
                (self[id_name], self[display_form_name], self[language_name],
                 self[script_name]))

    def delete (self):
        """Deletes the name parts in this form."""
        for name_part in self.instance[1]:
            name_part.remove()

    def _name_part_to_dict (self, name_parts):
        """Returns a dictionary containing the data in `name_parts`
        suitable for passing as a Form's `initial` keyword argument.

        :param name_parts: list of name parts (first element is name
          part type, second a list of name_parts)
        :type name_parts: list
        :rtype: dict

        """
        data = {'name_part_type': name_parts[0].get_id()}
        name_parts = name_parts[1]
        for i in range(len(name_parts)):
            name_part = name_parts[i]
            suffix = str(i)
            data['name_part_id-' + suffix] = name_part.get_id()
            data['name_part_display_form-' + suffix] = name_part.display_form
            data['name_part_language-' + suffix] = name_part.language.get_id()
            data['name_part_script-' + suffix] = name_part.script.get_id()
        return data

    def save (self, name_assertion):
        name = name_assertion.name
        i = 0
        while True:
            suffix = str(i)
            name_part = self.cleaned_data.get('name_part_id-' + suffix, False)
            if name_part is None:
                # There is such a field, but it does not hold a name
                # part.
                if self.cleaned_data['name_part_display_form-' + suffix]:
                    save_data = self._save_data(name, self.cleaned_data, suffix)
                    self._save_new(name, save_data)
            elif name_part:
                # There is such a field, and it holds a name part.
                if self.cleaned_data['name_part_display_form-' + suffix]:
                    save_data = self._save_data(name, self.cleaned_data, suffix)
                    self._save_existing(name_part, save_data)
                else:
                    # Delete the name part.
                    name_part.remove()
            else:
                # There is no such field.
                break
            i += 1

    def _save_data (self, name, data, suffix):
        return {
            'name_part_type': data['name_part_type'],
            'language': data['name_part_language-' + suffix] or name.language,
            'script': data['name_part_script-' + suffix] or name.script,
            'display_form': data['name_part_display_form-' + suffix],
            'order': int(suffix)
            }

    def _save_existing (self, name_part, data):
        name_part.name_part_type = data['name_part_type']
        name_part.language = data['language']
        name_part.script = data['script']
        name_part.display_form = data['display_form']
        name_part.order = data['order']
        name_part.update_name_index()
        return name_part

    def _save_new (self, name, data):
        return name.create_name_part(
            data['name_part_type'], data['language'], data['script'],
            data['display_form'], data['order'])

    def set_name_language (self, language):
        """Sets the language of the parent name."""
        self.name_language = language


class DateForm (forms.Form):

    date_period = forms.ChoiceField(choices=[])
    start = forms.CharField(label='Date', required=False)
    start_calendar = forms.ChoiceField(choices=[], label='Calendar',
                                       required=False)
    start_normalised = forms.CharField(label='Normalised value', required=False)
    start_type = forms.ChoiceField(choices=[], label='Type', required=False)
    start_certainty = forms.BooleanField(label='Certain', required=False)
    start_tpq = forms.CharField(label='Date', required=False)
    start_tpq_calendar = forms.ChoiceField(choices=[], label='Calendar',
                                           required=False)
    start_tpq_normalised = forms.CharField(label='Normalised value',
                                           required=False)
    start_tpq_type = forms.ChoiceField(choices=[], label='Type', required=False)
    start_tpq_certainty = forms.BooleanField(label='Certain', required=False)
    start_taq = forms.CharField(label='Date', required=False)
    start_taq_calendar = forms.ChoiceField(choices=[], label='Calendar',
                                           required=False)
    start_taq_normalised = forms.CharField(label='Normalised value',
                                           required=False)
    start_taq_type = forms.ChoiceField(choices=[], label='Type', required=False)
    start_taq_certainty = forms.BooleanField(label='Certain', required=False)
    end = forms.CharField(label='Date', required=False)
    end_calendar = forms.ChoiceField(choices=[], label='Calendar',
                                     required=False)
    end_normalised = forms.CharField(label='Normalised value', required=False)
    end_type = forms.ChoiceField(choices=[], label='Type', required=False)
    end_certainty = forms.BooleanField(label='Certain', required=False)
    end_tpq = forms.CharField(label='Date', required=False)
    end_tpq_calendar = forms.ChoiceField(choices=[], label='Calendar',
                                         required=False)
    end_tpq_normalised = forms.CharField(label='Normalised value',
                                         required=False)
    end_tpq_type = forms.ChoiceField(choices=[], label='Type', required=False)
    end_tpq_certainty = forms.BooleanField(label='Certain', required=False)
    end_taq = forms.CharField(label='Date', required=False)
    end_taq_calendar = forms.ChoiceField(choices=[], label='Calendar',
                                         required=False)
    end_taq_normalised = forms.CharField(label='Normalised value',
                                         required=False)
    end_taq_type = forms.ChoiceField(choices=[], label='Type', required=False)
    end_taq_certainty = forms.BooleanField(label='Certain', required=False)
    point = forms.CharField(label='Date', required=False)
    point_calendar = forms.ChoiceField(choices=[], label='Calendar',
                                       required=False)
    point_normalised = forms.CharField(label='Normalised value', required=False)
    point_type = forms.ChoiceField(choices=[], label='Type', required=False)
    point_certainty = forms.BooleanField(label='Certain', required=False)
    point_tpq = forms.CharField(label='Date', required=False)
    point_tpq_calendar = forms.ChoiceField(choices=[], label='Calendar',
                                           required=False)
    point_tpq_normalised = forms.CharField(label='Normalised value',
                                           required=False)
    point_tpq_type = forms.ChoiceField(choices=[], label='Type', required=False)
    point_tpq_certainty = forms.BooleanField(label='Certain', required=False)
    point_taq = forms.CharField(label='Date', required=False)
    point_taq_calendar = forms.ChoiceField(choices=[], label='Calendar',
                                           required=False)
    point_taq_normalised = forms.CharField(label='Normalised value',
                                           required=False)
    point_taq_type = forms.ChoiceField(choices=[], label='Type', required=False)
    point_taq_certainty = forms.BooleanField(label='Certain', required=False)

    def __init__ (self, topic_map, calendar_choices, date_period_choices,
                  date_type_choices, data=None, instance=None, **kwargs):
        self.topic_map = topic_map
        self.instance = instance
        calendar_choices = calendar_choices
        date_period_choices = date_period_choices
        date_type_choices = date_type_choices
        if instance is None:
            object_data = {}
        else:
            object_data = instance.get_form_data()
        super(DateForm, self).__init__(data, initial=object_data, **kwargs)
        self.fields['date_period'].choices = date_period_choices
        self.fields['start_calendar'].choices = calendar_choices
        self.fields['start_taq_calendar'].choices = calendar_choices
        self.fields['start_tpq_calendar'].choices = calendar_choices
        self.fields['end_calendar'].choices = calendar_choices
        self.fields['end_taq_calendar'].choices = calendar_choices
        self.fields['end_tpq_calendar'].choices = calendar_choices
        self.fields['point_calendar'].choices = calendar_choices
        self.fields['point_taq_calendar'].choices = calendar_choices
        self.fields['point_tpq_calendar'].choices = calendar_choices
        self.fields['start_type'].choices = date_type_choices
        self.fields['start_taq_type'].choices = date_type_choices
        self.fields['start_tpq_type'].choices = date_type_choices
        self.fields['end_type'].choices = date_type_choices
        self.fields['end_taq_type'].choices = date_type_choices
        self.fields['end_tpq_type'].choices = date_type_choices
        self.fields['point_type'].choices = date_type_choices
        self.fields['point_taq_type'].choices = date_type_choices
        self.fields['point_tpq_type'].choices = date_type_choices

    def clean (self):
        data = super(DateForm, self).clean()
        # In addition to performing some validation and objectifying
        # of data (replacing model object ids with model objects),
        # throw out all data that is associated with a blank date
        # part.
        new_data = {}
        if 'date_period' in data:
            new_data['date_period'] = DatePeriod.objects.get_by_identifier(
                data['date_period'])
        for prefix in ('start', 'start_taq', 'start_tpq', 'end', 'end_taq',
                       'end_tpq', 'point', 'point_taq', 'point_tpq'):
            if data.get(prefix):
                # If a date string is given, there must be a calendar
                # and date type for it. A normalised form is not
                # required, and certainty may be empty (meaning no
                # certainty).
                for part in ('_calendar', '_type'):
                    if not data.get(prefix + part):
                        raise forms.ValidationError('A calendar and date type must be specified for each date part that is not blank')
                new_data[prefix] = data[prefix]
                new_data[prefix + '_normalised'] = data[prefix + '_normalised']
                calendar_attr = prefix + '_calendar'
                calendar_id = data[calendar_attr]
                if calendar_id:
                    new_data[calendar_attr] = Calendar.objects.get_by_identifier(
                        calendar_id)
                type_attr = prefix + '_type'
                date_type_id = data.get(type_attr)
                if date_type_id:
                    new_data[type_attr] = DateType.objects.get_by_identifier(
                        date_type_id)
                certainty_attr = prefix + '_certainty'
                if data[certainty_attr]:
                    new_data[certainty_attr] = self.topic_map.date_full_certainty
                else:
                    new_data[certainty_attr] = self.topic_map.date_no_certainty
        self.cleaned_data = new_data
        return new_data

    def delete (self):
        self.instance.remove()

    def save (self, assertion=None):
        date = self.instance
        if date is None:
            # Create a new date.
            date = assertion.create_date(self.cleaned_data)
        else:
            # Update an existing date.
            date.update(self.cleaned_data)
        return date.get_id()



extra_existence_forms = getattr(settings, 'EATS_EXTRA_EXISTENCE_FORMS', 1)
ExistenceFormSet = formset_factory(ExistenceForm, can_delete=True,
                                   extra=extra_existence_forms,
                                   formset=ExistenceAssertionFormSet)

extra_relationship_forms = getattr(
    settings, 'EATS_EXTRA_ENTITY_RELATIONSHIP_FORMS', 2)
EntityRelationshipFormSet = formset_factory(
    EntityRelationshipForm, can_delete=True, extra=extra_relationship_forms,
    formset=EntityRelationshipAssertionFormSet)

extra_entity_type_forms = getattr(settings, 'EATS_EXTRA_ENTITY_TYPE_FORMS', 1)
EntityTypeFormSet = formset_factory(EntityTypeForm, can_delete=True,
                                    extra=extra_entity_type_forms,
                                    formset=EntityTypeAssertionFormSet)

extra_name_forms = getattr(settings, 'EATS_EXTRA_NAME_FORMS', 2)
NameFormSet = formset_factory(NameForm, can_delete=True, extra=extra_name_forms,
                              formset=NameAssertionFormSet)

extra_name_part_forms = getattr(settings, 'EATS_EXTRA_NAME_PART_FORMS', 2)
NamePartFormSet = formset_factory(NamePartForm, can_delete=True,
                                  extra=extra_name_part_forms,
                                  formset=NamePartInlineFormSet)

extra_note_forms = getattr(settings, 'EATS_EXTRA_NOTE_FORMS', 1)
NoteFormSet = formset_factory(NotePropertyAssertionForm, can_delete=True,
                              extra=extra_note_forms,
                              formset=NoteAssertionFormSet)

extra_si_forms = getattr(
    settings, 'EATS_EXTRA_SUBJECT_IDENTIFIER_FORMS', 2)
SubjectIdentifierFormSet = formset_factory(
    SubjectIdentifierForm, can_delete=True, extra=extra_si_forms,
    formset=SubjectIdentifierAssertionFormSet)


class EATSMLImportForm (forms.Form):

    import_file = forms.FileField()
    description = forms.CharField(max_length=200)


class EntityMergeForm (forms.Form):

    merge_entity = selectable.AutoCompleteSelectField(
        lookup_class=EntityLookup)


def create_choice_list (topic_map, queryset, default=False, multiple=False):
    """Return a list of 2-tuples created from the items in
    `queryset`.

    If `multiple` is True, or if `queryset` contains only one record
    and `default` is True, do not provide an empty option.

    :param topic_map: the EATS topic map
    :type topic_map: `TopicMap`
    :param queryset: source of data for choices
    :type queryset: `QuerySet`
    :param default:
    :type default: `bool`
    :param multiple: whether multiple choices are allowed
    :type multiple: `bool`
    :rtype: list

    """
    # QAZ: need a function for getting the most appropriate name,
    # based on the user's preferences.
    choices = [(str(item.get_id()), item.get_admin_name())
               for item in queryset]
    choices.sort(key=lambda x: x[1])
    if not (multiple or (len(queryset) == 1 and default)):
        choices = [('', '----------')] + choices
    return choices
