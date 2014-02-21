from django import forms

from eats.views.edit import create_choice_list


class EntitySearchForm (forms.Form):

    name = forms.CharField(label='Name')
    entity_type = forms.ChoiceField(required=False)

    def __init__ (self, topic_map, *args, **kwargs):
        entity_types = kwargs.pop('entity_types', [])
        super(EntitySearchForm, self).__init__(*args, **kwargs)
        self.fields['entity_type'].choices = create_choice_list(
            topic_map, entity_types)
