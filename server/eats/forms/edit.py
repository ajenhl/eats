from django import forms
from django.forms.formsets import formset_factory, BaseFormSet

from eats.api.topic_map import get_admin_name


class PropertyAssertionFormSet (BaseFormSet):

    def __init__ (self, *args, **kwargs):
        self.authority_choices = kwargs.pop('authority_choices')
        super(PropertyAssertionFormSet, self).__init__(*args, **kwargs)

    def _construct_forms (self):
        self.forms = []
        for i in xrange(self.total_form_count()):
            self.forms.append(self._construct_form(
                    i, authority_choices=self.authority_choices))


class EntityTypeAssertionFormSet (PropertyAssertionFormSet):

    def __init__ (self, *args, **kwargs):
        self.entity_type_choices = kwargs.pop('entity_type_choices')
        super(EntityTypeAssertionFormSet, self).__init__(*args, **kwargs)

    def _construct_forms (self):
        self.forms = []
        for i in xrange(self.total_form_count()):
            self.forms.append(self._construct_form(
                    i, authority_choices=self.authority_choices,
                    entity_type_choices=self.entity_type_choices))


class CreateEntityForm (forms.Form):

    authority = forms.ChoiceField(choices=[])

    def __init__ (self, topic_map, authorities, *args, **kwargs):
        super(CreateEntityForm, self).__init__(*args, **kwargs)
        self.fields['authority'].choices = create_choice_list(
            topic_map, authorities, True)


class PropertyAssertionForm (forms.Form):

    authority = forms.ChoiceField(choices=[])

    def __init__ (self, *args, **kwargs):
        authority_choices = kwargs.pop('authority_choices')
        super(PropertyAssertionForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            authority_choices = authority_choices[1:]
        self.fields['authority'].choices = authority_choices
        
        
class ExistenceForm (PropertyAssertionForm):

    pass


class EntityTypeForm (PropertyAssertionForm):

    entity_type = forms.ChoiceField(choices=[])

    def __init__ (self, *args, **kwargs):
        entity_type_choices = kwargs.pop('entity_type_choices')
        super(EntityTypeForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            entity_type_choices = entity_type_choices[1:]
        self.fields['entity_type'].choices = entity_type_choices


ExistenceFormSet = formset_factory(ExistenceForm, can_delete=True,
                                   formset=PropertyAssertionFormSet)
EntityTypeFormSet = formset_factory(EntityTypeForm, can_delete=True,
                                    formset=EntityTypeAssertionFormSet)


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
    choices = [(unicode(item.get_id()), get_admin_name(topic_map, item))
               for item in queryset]
    if not (queryset.count() == 1 and default):
        choices = [('', '----------')] + choices
    return choices
