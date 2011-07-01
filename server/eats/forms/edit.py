from django import forms
from django.forms.formsets import formset_factory, BaseFormSet

import selectable.forms as selectable

from eats.constants import FORWARD_RELATIONSHIP_MARKER, \
    REVERSE_RELATIONSHIP_MARKER
from eats.lookups import EntityLookup
from eats.models import Calendar, DatePeriod, DateType, EntityRelationshipPropertyAssertion, EntityTypePropertyAssertion, ExistencePropertyAssertion, NamePropertyAssertion, NotePropertyAssertion


class PropertyAssertionFormSet (BaseFormSet):

    def __init__ (self, topic_map, entity, authority_choices, **kwargs):
        self.topic_map = topic_map
        self.entity = entity
        self.authority_choices = authority_choices
        super(PropertyAssertionFormSet, self).__init__(**kwargs)

    def _construct_form (self, i, **kwargs):
        kwargs.update({'topic_map': self.topic_map, 'entity': self.entity,
                       'authority_choices': self.authority_choices})
        return super(PropertyAssertionFormSet, self)._construct_form(
            i, **kwargs)


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

    def __init__ (self, *args, **kwargs):
        self.topic_map = kwargs.pop('topic_map')
        self.entity = kwargs.pop('entity')
        authority_choices = kwargs.pop('authority_choices')
        super(PropertyAssertionForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            authority_choices = authority_choices[1:]
        self.fields['authority'].choices = authority_choices

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
        assertion = self._get_construct('assertion',
                                        self._property_assertion_model)
        if assertion is None:
            return
        assertion.remove()

    def save (self):
        raise NotImplementedError
        
        
class ExistenceForm (PropertyAssertionForm):

    _property_assertion_model = ExistencePropertyAssertion
    
    def save (self):
        authority = self._get_construct('authority')
        assertion = self._get_construct('assertion',
                                        self._property_assertion_model)
        if assertion is None:
            # Create a new assertion.
            self.entity.create_existence_property_assertion(authority)
        else:
            # Update an existing assertion.
            assertion.update(authority)


class EntityRelationshipForm (PropertyAssertionForm):

    relationship_type = forms.ChoiceField(choices=[])
    related_entity = selectable.AutoCompleteSelectField(
        lookup_class=EntityLookup)

    _property_assertion_model = EntityRelationshipPropertyAssertion

    def __init__ (self, *args, **kwargs):
        relationship_type_choices = kwargs.pop('relationship_type_choices')
        super(EntityRelationshipForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            relationship_type_choices = relationship_type_choices[1:]
        self.fields['relationship_type'].choices = relationship_type_choices

    def save (self):
        authority = self._get_construct('authority')
        assertion = self._get_construct('assertion',
                                        proxy=self._property_assertion_model)
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
        if assertion is None:
            # Create a new assertion.
            self.entity.create_entity_relationship_property_assertion(
                authority, relationship_type, domain_entity, range_entity)
        else:
            # Update an existing assertion.
            assertion.update(authority, relationship_type, domain_entity,
                             range_entity)


class EntityTypeForm (PropertyAssertionForm):

    entity_type = forms.ChoiceField(choices=[])

    _property_assertion_model = EntityTypePropertyAssertion

    def __init__ (self, *args, **kwargs):
        entity_type_choices = kwargs.pop('entity_type_choices')
        super(EntityTypeForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            entity_type_choices = entity_type_choices[1:]
        self.fields['entity_type'].choices = entity_type_choices

    def delete (self):
        assertion = self._get_construct('assertion',
                                        proxy=self._property_assertion_model)
        assertion.remove()
        
    def save (self):
        authority = self._get_construct('authority')
        assertion = self._get_construct('assertion',
                                        proxy=self._property_assertion_model)
        entity_type = self._get_construct('entity_type')
        if assertion is None:
            # Create a new assertion.
            self.entity.create_entity_type_property_assertion(
                authority, entity_type)
        else:
            # Update an existing assertion.
            assertion.update(authority, entity_type)


class NameForm (PropertyAssertionForm):

    name_type = forms.ChoiceField(choices=[])
    language = forms.ChoiceField(choices=[])
    script = forms.ChoiceField(choices=[])
    display_form = forms.CharField()

    _property_assertion_model = NamePropertyAssertion

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

    def delete (self):
        assertion = self._get_construct('assertion',
                                        proxy=self._property_assertion_model)
        assertion.remove()

    def save (self):
        authority = self._get_construct('authority')
        assertion = self._get_construct('assertion',
                                        proxy=self._property_assertion_model)
        name_type = self._get_construct('name_type')
        language = self._get_construct('language')
        script = self._get_construct('script')
        display_form = self.cleaned_data['display_form']
        if assertion is None:
            # Create a new assertion.
            self.entity.create_name_property_assertion(
                authority, name_type, language, script, display_form)
        else:
            # Update an existing assertion.
            assertion.update(authority, name_type, language, script,
                             display_form)


class NoteForm (PropertyAssertionForm):

    note = forms.CharField(widget=forms.Textarea)

    _property_assertion_model = NotePropertyAssertion

    def save (self):
        authority = self._get_construct('authority')
        assertion = self._get_construct('assertion',
                                        proxy=self._property_assertion_model)
        note = self.cleaned_data['note']
        if assertion is None:
            # Create a new assertion.
            self.entity.create_note_property_assertion(authority, note)
        else:
            # Update an existing assertion.
            assertion.update(authority, note)


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

    def _objectify_data (self, base_data):
        data = {}
        data['date_period'] = DatePeriod.objects.get_by_identifier(
            base_data['date_period'])
        for prefix in ('start', 'start_taq', 'start_tpq', 'end', 'end_taq',
                       'end_tpq', 'point', 'point_taq', 'point_tpq'):
            data[prefix] = base_data.get(prefix)
            data[prefix + '_normalised'] = base_data.get(prefix + '_normalised')
            calendar_attr = prefix + '_calendar'
            calendar_id = base_data.get(calendar_attr)
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
            pass
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
