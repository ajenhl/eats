from django import forms

from eats.constants import CALENDAR_TYPE_IRI, DATE_PERIOD_TYPE_IRI, DATE_TYPE_TYPE_IRI, ENTITY_RELATIONSHIP_TYPE_TYPE_IRI, ENTITY_TYPE_TYPE_IRI, LANGUAGE_TYPE_IRI, NAME_TYPE_TYPE_IRI, SCRIPT_TYPE_IRI
from eats.models import Authority, Calendar, DatePeriod, DateType, EntityRelationshipType, EntityType, Language, NameType, Script
from eats.views.edit import create_choice_list


class AdminForm (forms.Form):

    name = forms.CharField(max_length=100)
    
    def __init__ (self, topic_map, instance=None, **kwargs):
        """Initialise the form.

        :param topic_map: the EATS Topic Map
        :type topic_map: `TopicMap`
        :param topic_id: the `Identifier` id of the topic
        :type topic_id: integer or None

        """
        self.topic_map = topic_map
        self.instance = instance
        if instance is None:
            object_data = {}
        else:
            object_data = self._topic_to_dict(instance)
        super(AdminForm, self).__init__(initial=object_data, **kwargs)

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

    def _topic_to_dict (self, topic):
        return {}


class AuthorityForm (AdminForm):

    calendars = forms.MultipleChoiceField(choices=[], required=False)
    date_periods = forms.MultipleChoiceField(choices=[], required=False)
    date_types = forms.MultipleChoiceField(choices=[], required=False)
    entity_relationship_types = forms.MultipleChoiceField(choices=[],
                                                          required=False)
    entity_types = forms.MultipleChoiceField(choices=[], required=False)
    languages = forms.MultipleChoiceField(choices=[], required=False)
    name_types = forms.MultipleChoiceField(choices=[], required=False)
    scripts = forms.MultipleChoiceField(choices=[], required=False)

    def __init__ (self, topic_map, data=None, instance=None, **kwargs):
        super(AuthorityForm, self).__init__(topic_map, data=data,
                                            instance=instance, **kwargs)
        self.fields['calendars'].choices = create_choice_list(
            topic_map, Calendar.objects.all())[1:]
        self.fields['date_periods'].choices = create_choice_list(
            topic_map, DatePeriod.objects.all())[1:]
        self.fields['date_types'].choices = create_choice_list(
            topic_map, DateType.objects.all())[1:]
        self.fields['entity_relationship_types'].choices = create_choice_list(
            topic_map, EntityRelationshipType.objects.all())[1:]
        self.fields['entity_types'].choices = create_choice_list(
            topic_map, EntityType.objects.all())[1:]
        self.fields['languages'].choices = create_choice_list(
            topic_map, Language.objects.all())[1:]
        self.fields['name_types'].choices = create_choice_list(
            topic_map, NameType.objects.all())[1:]
        self.fields['scripts'].choices = create_choice_list(
            topic_map, Script.objects.all())[1:]

    def clean_name (self):
        name = self.cleaned_data['name']
        try:
            authority = Authority.objects.get_by_admin_name(name)
            if self.instance is None or self.instance != authority:
                raise forms.ValidationError(
                    'The name of the authority must be unique')
        except Authority.DoesNotExist:
            pass
        return name

    def _objectify_data (self, base_data):
        # It would be nice to handle this process of converting
        # submitted form data into model objects where appropriate in
        # the same fashion as with ModelForms (that is, in each
        # field's to_python method). However, since the rendering of
        # the object relies on the authority and user preferences,
        # which aren't passed in to the field, this doesn't seem
        # possible, and so it is handled here.
        data = {'calendars': [], 'date_periods': [], 'date_types': [],
                'entity_relationship_types': [], 'entity_types': [],
                'languages': [], 'name_types': [], 'scripts': []}
        for calendar_id in base_data['calendars']:
            data['calendars'].append(Calendar.objects.get_by_identifier(
                    calendar_id))
        for date_period_id in base_data['date_periods']:
            data['date_periods'].append(DatePeriod.objects.get_by_identifier(
                    date_period_id))
        for date_type_id in base_data['date_types']:
            data['date_types'].append(DateType.objects.get_by_identifier(
                    date_type_id))
        for entity_relationship_type_id in base_data['entity_relationship_types']:
            data['entity_relationship_types'].append(
                EntityRelationshipType.objects.get_by_identifier(
                    entity_relationship_type_id))
        for entity_type_id in base_data['entity_types']:
            data['entity_types'].append(EntityType.objects.get_by_identifier(
                    entity_type_id))
        for language_id in base_data['languages']:
            data['languages'].append(Language.objects.get_by_identifier(
                    language_id))
        for name_type_id in base_data['name_types']:
            data['name_types'].append(NameType.objects.get_by_identifier(
                    name_type_id))
        for script_id in base_data['scripts']:
            data['scripts'].append(Script.objects.get_by_identifier(
                    script_id))
        return data
    
    def save (self):
        name = self.cleaned_data['name']
        data = self._objectify_data(self.cleaned_data)
        if self.instance is None:
            authority = self.topic_map.create_authority(name)
        else:
            authority = self.topic
        authority.set_calendars(data['calendars'])
        authority.set_date_periods(data['date_periods'])
        authority.set_date_types(data['date_types'])
        authority.set_entity_relationship_types(
            data['entity_relationship_types'])
        authority.set_entity_types(data['entity_types'])
        authority.set_languages(data['languages'])
        authority.set_name_types(data['name_types'])
        authority.set_scripts(data['scripts'])
        return authority


class CalendarForm (AdminForm):

    def clean_name (self):
        name = self.cleaned_data['name']
        if self.topic_map.topic_exists(CALENDAR_TYPE_IRI, name, self.topic_id):
            raise forms.ValidationError(
                'The name of the calendar must be unique')
        return name


class DatePeriodForm (AdminForm):

    def clean_name (self):
        name = self.cleaned_data['name']
        if self.topic_map.topic_exists(DATE_PERIOD_TYPE_IRI, name,
                                       self.topic_id):
            raise forms.ValidationError(
                'The name of the date period must be unique')
        return name


class DateTypeForm (AdminForm):

    def clean_name (self):
        name = self.cleaned_data['name']
        if self.topic_map.topic_exists(DATE_TYPE_TYPE_IRI, name,
                                       self.topic_id):
            raise forms.ValidationError(
                'The name of the date type must be unique')
        return name


class EntityRelationshipForm (AdminForm):

    reverse_name = forms.CharField(max_length=100)
    
    def clean_name (self):
        name = self.cleaned_data['name']
        if self.topic_map.topic_exists(ENTITY_RELATIONSHIP_TYPE_TYPE_IRI, name,
                                       self.topic_id):
            raise forms.ValidationError(
                'The name of the entity relationship type must be unique')
        return name

    def clean_reverse_name (self):
        name = self.cleaned_data['reverse_name']
        if self.topic_map.topic_exists(ENTITY_RELATIONSHIP_TYPE_TYPE_IRI, name,
                                       self.topic_id):
            raise forms.ValidationError(
                'The reverse name of the entity relationship type must be unique')
        return name


class EntityTypeForm (AdminForm):

    def clean_name (self):
        name = self.cleaned_data['name']
        if self.topic_map.topic_exists(ENTITY_TYPE_TYPE_IRI, name,
                                       self.topic_id):
            raise forms.ValidationError(
                'The name of the entity type must be unique')
        return name
    

class LanguageForm (AdminForm):

    code = forms.CharField(max_length=3)

    def clean_code (self):
        code = self.cleaned_data['code']
        # QAZ: Need to ensure that the code is unique, along with the
        # name. topic_exists checks on the admin name, and so is not
        # suitable.
        return code

    def clean_name (self):
        name = self.cleaned_data['name']
        if self.topic_map.topic_exists(LANGUAGE_TYPE_IRI, name, self.topic_id):
            raise forms.ValidationError(
                'The name of the language must be unique')
        return name


class NameTypeForm (AdminForm):

    def clean_name (self):
        name = self.cleaned_data['name']
        if self.topic_map.topic_exists(NAME_TYPE_TYPE_IRI, name, self.topic_id):
            raise forms.ValidationError(
                'The name of the name type must be unique')
        return name

    

class ScriptForm (AdminForm):

    code = forms.CharField(max_length=4)

    def clean_code (self):
        code = self.cleaned_data['code']
        # QAZ: Need to ensure that the code is unique, along with the
        # name. topic_exists checks on the admin name, and so is not
        # suitable.
        return code

    def clean_name (self):
        name = self.cleaned_data['name']
        if self.topic_map.topic_exists(SCRIPT_TYPE_IRI, name, self.topic_id):
            raise forms.ValidationError(
                'The name of the script must be unique')
        return name
