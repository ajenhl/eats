from django import forms
from django.forms.formsets import formset_factory, BaseFormSet

import selectable.forms as selectable

from eats.constants import FORWARD_RELATIONSHIP_MARKER, \
    REVERSE_RELATIONSHIP_MARKER
from eats.lookups import EntityLookup
from eats.models import Calendar, DatePeriod, DateType


class PropertyAssertionFormSet (BaseFormSet):

    """Base class for the formsets of specific property assertion types.

    This code is heavily influenced by Django's BaseModelFormSet,
    since we are dealing with objects that are tied to models, just in
    an aggregated way that makes using ModelFormSets impossible.

    """

    def __init__ (self, topic_map, entity, authority_choices, instances,
                  **kwargs):
        self.topic_map = topic_map
        self.entity = entity
        self.authority_choices = authority_choices
        self.instances = instances or []
        super(PropertyAssertionFormSet, self).__init__(**kwargs)

    def _construct_form (self, i, **kwargs):
        kwargs.update({'topic_map': self.topic_map, 'entity': self.entity,
                       'authority_choices': self.authority_choices})
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
        if not (self.data):
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
        self.changed_objects = []
        self.deleted_objects = []
        if not self.instances:
            return []
        saved_assertions = []
        for form in self.initial_forms:
            raw_id_value = form._raw_value('assertion')
            id_value = form.fields['assertion'].clean(raw_id_value)
            obj = self._existing_object(id_value)
            if self.can_delete and self._should_delete_form(form):
                self.deleted_objects.append(obj)
                obj.remove()
                continue
            if form.has_changed():
                self.changed_objects.append((obj, form.changed_data))
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
        self.name_type_choices = kwargs.pop('name_type_choices')
        self.language_choices = kwargs.pop('language_choices')
        self.script_choices = kwargs.pop('script_choices')
        super(NameAssertionFormSet, self).__init__(**kwargs)

    def _construct_form (self, i, **kwargs):
        kwargs.update({'name_type_choices': self.name_type_choices,
                       'language_choices': self.language_choices,
                       'script_choices': self.script_choices})
        return super(NameAssertionFormSet, self)._construct_form(
            i, **kwargs)


class NoteAssertionFormSet (PropertyAssertionFormSet):

    pass
        


class CreateEntityForm (forms.Form):

    authority = forms.ChoiceField(choices=[])

    def __init__ (self, topic_map, authorities, *args, **kwargs):
        super(CreateEntityForm, self).__init__(*args, **kwargs)
        self.fields['authority'].choices = create_choice_list(
            topic_map, authorities, True)


class PropertyAssertionForm (forms.Form):

    authority = forms.ChoiceField(choices=[])
    assertion = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def __init__ (self, topic_map, entity, authority_choices, initial=None,
                  instance=None, **kwargs):
        self.topic_map = topic_map
        self.entity = entity
        self.instance = instance
        if instance is None:
            object_data = {}
        else:
            object_data = self._assertion_to_dict(instance)
        if initial is not None:
            object_data.update(initial)
        super(PropertyAssertionForm, self).__init__(initial=object_data,
                                                    **kwargs)
        if 'instance' in kwargs:
            authority_choices = authority_choices[1:]
        self.fields['authority'].choices = authority_choices

    def _assertion_to_dict (self, assertion):
        """Returns a dictionary containing the data in `assertion`
        suitable for passing as a Form's `initial` keyword argument.

        :rtype: dict

        """
        data = {'authority': assertion.authority.get_id(),
                'assertion': assertion.get_id()}
        return data
        
    def _get_construct (self, name, proxy=None):
        """Returns the construct specified by `name`.

        `name` corresponds to the name of one of the form's fields.

        :param name: name of the construct to return
        :type name: string
        :param proxy: Django proxy model
        :type proxy: class
        :rtype: `Construct` or proxy object

        """
        construct_id = self.cleaned_data[name]
        construct = None
        if construct_id is not None:
            construct = self.topic_map.get_construct_by_id(construct_id, proxy)
        return construct
        
    def delete (self):
        """Deletes the assertion."""
        self.instance.remove()

    def save (self):
        raise NotImplementedError
        
        
class ExistenceForm (PropertyAssertionForm):

    def save (self):
        authority = self._get_construct('authority')
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_existence_property_assertion(authority)
        else:
            # Update an existing assertion.
            self.instance.update(authority)


class EntityRelationshipForm (PropertyAssertionForm):

    relationship_type = forms.ChoiceField(choices=[])
    related_entity = selectable.AutoCompleteSelectField(
        lookup_class=EntityLookup)

    def __init__ (self, *args, **kwargs):
        relationship_type_choices = kwargs.pop('relationship_type_choices')
        super(EntityRelationshipForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            relationship_type_choices = relationship_type_choices[1:]
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
        return data
        
    def save (self):
        authority = self._get_construct('authority')
        relationship_type_id = self.cleaned_data['relationship_type']
        relationship_type = self.topic_map.get_construct_by_id(
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
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_entity_relationship_property_assertion(
                authority, relationship_type, domain_entity, range_entity)
        else:
            # Update an existing assertion.
            self.instance.update(authority, relationship_type, domain_entity,
                                 range_entity)


class EntityTypeForm (PropertyAssertionForm):

    entity_type = forms.ChoiceField(choices=[])

    def __init__ (self, *args, **kwargs):
        entity_type_choices = kwargs.pop('entity_type_choices')
        super(EntityTypeForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            entity_type_choices = entity_type_choices[1:]
        self.fields['entity_type'].choices = entity_type_choices

    def _assertion_to_dict (self, assertion):
        data = super(EntityTypeForm, self)._assertion_to_dict(assertion)
        data['entity_type'] = assertion.entity_type.get_id()
        return data
        
    def save (self):
        authority = self._get_construct('authority')
        entity_type = self._get_construct('entity_type')
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_entity_type_property_assertion(
                authority, entity_type)
        else:
            # Update an existing assertion.
            self.instance.update(authority, entity_type)


class NameForm (PropertyAssertionForm):

    name_type = forms.ChoiceField(choices=[])
    language = forms.ChoiceField(choices=[])
    script = forms.ChoiceField(choices=[])
    display_form = forms.CharField()

    def __init__ (self, *args, **kwargs):
        name_type_choices = kwargs.pop('name_type_choices')
        language_choices = kwargs.pop('language_choices')
        script_choices = kwargs.pop('script_choices')
        super(NameForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            name_type_choices = name_type_choices[1:]
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
        return data

    def save (self):
        authority = self._get_construct('authority')
        name_type = self._get_construct('name_type')
        language = self._get_construct('language')
        script = self._get_construct('script')
        display_form = self.cleaned_data['display_form']
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_name_property_assertion(
                authority, name_type, language, script, display_form)
        else:
            # Update an existing assertion.
            self.instance.update(authority, name_type, language, script,
                                 display_form)


class NoteForm (PropertyAssertionForm):

    note = forms.CharField(widget=forms.Textarea)

    def _assertion_to_dict (self, assertion):
        data = super(NoteForm, self)._assertion_to_dict(assertion)
        data['note'] = assertion.note
        return data
    
    def save (self):
        authority = self._get_construct('authority')
        note = self.cleaned_data['note']
        if self.instance is None:
            # Create a new assertion.
            self.entity.create_note_property_assertion(authority, note)
        else:
            # Update an existing assertion.
            self.instance.update(authority, note)


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
    start__taq_normalised = forms.CharField(label='Normalised value',
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
    point_tpq__normalised = forms.CharField(label='Normalised value',
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

    def __init__ (self, *args, **kwargs):
        self.topic_map = kwargs.pop('topic_map')
        calendar_choices = kwargs.pop('calendar_choices')
        date_period_choices = kwargs.pop('date_period_choices')
        date_type_choices = kwargs.pop('date_type_choices')
        super(DateForm, self).__init__(*args, **kwargs)
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
        cleaned_data = super(DateForm, self).clean()
        for prefix in ('start', 'start_taq', 'start_tpq', 'end', 'end_taq',
                       'end_tpq', 'point', 'point_taq', 'point_tpq'):
            if cleaned_data.get(prefix):
                # If a date string is given, there must be a calendar
                # and date type for it. A normalised form is not
                # required, and certainty may be empty (meaning no
                # certainty).
                for part in ('_calendar', '_type'):
                    if not cleaned_data.get(prefix + part):
                        raise forms.ValidationError('A calendar and date type must be specified for each date part that is not blank')
        return cleaned_data

    def _objectify_data (self, base_data):
        # It would be nice to handle this process of converting
        # submitted form data into model objects where appropriate in
        # the same fashion as with ModelForms (that is, in each
        # field's to_python method). However, since the rendering of
        # the object relies on the authority and user preferences,
        # which aren't passed in to the field, this doesn't seem
        # possible, and so it is handled here.
        data = {}
        data['date_period'] = DatePeriod.objects.get_by_identifier(
            base_data['date_period'])
        for prefix in ('start', 'start_taq', 'start_tpq', 'end', 'end_taq',
                       'end_tpq', 'point', 'point_taq', 'point_tpq'):
            if base_data[prefix]:
                data[prefix] = base_data.get(prefix)
                data[prefix + '_normalised'] = base_data[prefix + '_normalised']
                calendar_attr = prefix + '_calendar'
                calendar_id = base_data[calendar_attr]
                if calendar_id:
                    data[calendar_attr] = Calendar.objects.get_by_identifier(
                        calendar_id)
                type_attr = prefix + '_type'
                date_type_id = base_data.get(type_attr)
                if date_type_id:
                    data[type_attr] = DateType.objects.get_by_identifier(
                        date_type_id)
                certainty_attr = prefix + '_certainty'
                if base_data[certainty_attr]:
                    data[certainty_attr] = self.topic_map.date_full_certainty
                else:
                    data[certainty_attr] = self.topic_map.date_no_certainty
        return data
        
    def save (self, assertion, date=None):
        data = self._objectify_data(self.cleaned_data)
        if date is None:
            # Create a new date.
            date = assertion.create_date(data)
        else:
            # Update an existing date.
            date.update(data)
        return date.get_id()

        
ExistenceFormSet = formset_factory(ExistenceForm, can_delete=True,
                                   formset=ExistenceAssertionFormSet)
EntityRelationshipFormSet = formset_factory(
    EntityRelationshipForm, can_delete=True,
    formset=EntityRelationshipAssertionFormSet)
EntityTypeFormSet = formset_factory(EntityTypeForm, can_delete=True,
                                    formset=EntityTypeAssertionFormSet)
NameFormSet = formset_factory(NameForm, can_delete=True,
                              formset=NameAssertionFormSet)
NoteFormSet = formset_factory(NoteForm, can_delete=True,
                              formset=NoteAssertionFormSet)


def create_choice_list (topic_map, queryset, default=False):
    """Return a list of 2-tuples created from the items in
    `queryset`.

    If `queryset` contains only one record, and `default` is True, do
    not provide an empty option.

    :param topic_map: the EATS topic map
    :type topic_map: `TopicMap`
    :param queryset: source of data for choices
    :type queryset: `QuerySet`
    :rtype: list

    """
    # QAZ: need a function for getting the most appropriate name,
    # based on the user's preferences.
    choices = [(unicode(item.get_id()), topic_map.get_admin_name(item))
               for item in queryset]
    if not (queryset.count() == 1 and default):
        choices = [('', '----------')] + choices
    return choices
