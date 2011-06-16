from django import forms
from django.forms.formsets import formset_factory, BaseFormSet

import selectable.forms as selectable

from eats.lookups import EntityLookup
from eats.models import EntityTypePropertyAssertion, ExistencePropertyAssertion, NamePropertyAssertion, NotePropertyAssertion


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
        self.relationship_choices = kwargs.pop('relationship_choices')
        super(EntityRelationshipAssertionFormSet, self).__init__(**kwargs)

    def _construct_form (self, i, **kwargs):
        kwargs.update({'relationship_choices': self.relationship_choices})
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

    domain_entity = selectable.AutoCompleteSelectField(EntityLookup)
    relationship = forms.ChoiceField(choices=[])
    range_entity = forms.CharField()

    def __init__ (self, *args, **kwargs):
        relationship_choices = kwargs.pop('relationship_choices')
        super(EntityRelationshipForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            relationship_choices = relationship_choices[1:]
        self.fields['relationship'].choices = relationship_choices


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
