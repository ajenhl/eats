from django import forms

from eats.models import (Calendar, DatePeriod, DateType, EATSUser,
                         EntityRelationshipType, EntityType, Language,
                         NamePartType, NameType, Script)
from eats.forms.edit import create_choice_list


class AdminForm (forms.Form):

    name = forms.CharField(max_length=100)

    def __init__ (self, topic_map, model, data=None, instance=None, **kwargs):
        """Initialise the form.

        :param topic_map: the EATS Topic Map
        :type topic_map: `TopicMap`
        :param model: the model class
        :type model: class

        """
        self.topic_map = topic_map
        self.model = model
        self.instance = instance
        if instance is None:
            object_data = {}
        else:
            object_data = self._topic_to_dict(instance)
        super().__init__(initial=object_data, data=data, **kwargs)

    def clean_name (self):
        name = self.cleaned_data['name']
        try:
            existing = self.model.objects.get_by_admin_name(name)
            if self.instance is None or self.instance != existing:
                raise forms.ValidationError(
                    'The name of the %s must be unique' %
                    self.model._meta.verbose_name)
        except self.model.DoesNotExist:
            pass
        return name

    def save (self, create_method):
        name = self.cleaned_data['name']
        if self.instance is None:
            model_object = create_method(name)
        else:
            model_object = self.instance
            model_object.set_admin_name(name)
        return model_object

    def _topic_to_dict (self, topic):
        return {'name': topic.get_admin_name()}


class AuthorityForm (AdminForm):

    calendars = forms.MultipleChoiceField(choices=[], required=False)
    date_periods = forms.MultipleChoiceField(choices=[], required=False)
    date_types = forms.MultipleChoiceField(choices=[], required=False)
    entity_relationship_types = forms.MultipleChoiceField(choices=[],
                                                          required=False)
    entity_types = forms.MultipleChoiceField(choices=[], required=False)
    languages = forms.MultipleChoiceField(choices=[], required=False)
    name_types = forms.MultipleChoiceField(choices=[], required=False)
    name_part_types = forms.MultipleChoiceField(choices=[], required=False)
    scripts = forms.MultipleChoiceField(choices=[], required=False)
    editors = forms.MultipleChoiceField(choices=[], required=False)

    def __init__ (self, topic_map, model, data=None, instance=None, **kwargs):
        super().__init__(topic_map, model, data=data, instance=instance,
                         **kwargs)
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
        self.fields['name_part_types'].choices = create_choice_list(
            topic_map, NamePartType.objects.all())[1:]
        self.fields['scripts'].choices = create_choice_list(
            topic_map, Script.objects.all())[1:]
        self.fields['editors'].choices = [(editor.user.pk, editor.user.username)
                                          for editor in EATSUser.objects.all()]

    def _objectify_data (self, base_data):
        # It would be nice to handle this process of converting
        # submitted form data into model objects where appropriate in
        # the same fashion as with ModelForms (that is, in each
        # field's to_python method). However, since the rendering of
        # the object relies on the authority and user preferences,
        # which aren't passed in to the field, this doesn't seem
        # possible, and so it is handled here.
        data = {}
        data_map = {'calendars': Calendar,
                    'date_periods': DatePeriod,
                    'date_types': DateType,
                    'entity_relationship_types': EntityRelationshipType,
                    'entity_types': EntityType,
                    'languages': Language,
                    'name_part_types': NamePartType,
                    'name_types': NameType,
                    'scripts': Script}
        for data_type, model in data_map.items():
            data[data_type] = [model.objects.get_by_identifier(topic_id) for
                               topic_id in base_data[data_type]]
        data['editors'] = [EATSUser.objects.get(pk=editor_id) for editor_id in
                           base_data['editors']]
        return data

    def save (self):
        name = self.cleaned_data['name']
        data = self._objectify_data(self.cleaned_data)
        if self.instance is None:
            authority = self.topic_map.create_authority(name)
        else:
            authority = self.instance
            authority.set_admin_name(name)
        authority.set_calendars(data['calendars'])
        authority.set_date_periods(data['date_periods'])
        authority.set_date_types(data['date_types'])
        authority.set_entity_relationship_types(
            data['entity_relationship_types'])
        authority.set_entity_types(data['entity_types'])
        authority.set_languages(data['languages'])
        authority.set_name_types(data['name_types'])
        authority.set_name_part_types(data['name_part_types'])
        authority.set_scripts(data['scripts'])
        authority.set_editors(data['editors'])
        return authority

    def _topic_to_dict (self, topic):
        data = super()._topic_to_dict(topic)
        data['calendars'] = [calendar.get_id() for calendar in
                             topic.get_calendars()]
        data['date_periods'] = [date_period.get_id() for date_period in
                                topic.get_date_periods()]
        data['date_types'] = [date_type.get_id() for date_type in
                                topic.get_date_types()]
        data['entity_relationship_types'] = [
            entity_relationship_type.get_id() for entity_relationship_type in
            topic.get_entity_relationship_types()]
        data['entity_types'] = [entity_type.get_id() for entity_type in
                                topic.get_entity_types()]
        data['languages'] = [language.get_id() for language in
                                topic.get_languages()]
        data['name_types'] = [name_type.get_id() for name_type in
                                topic.get_name_types()]
        data['name_part_types'] = [name_part_type.get_id() for name_part_type
                                   in topic.get_name_part_types()]
        data['scripts'] = [script.get_id() for script in topic.get_scripts()]
        data['editors'] = [editor.pk for editor in topic.get_editors()]
        return data


class CalendarForm (AdminForm):

    def save (self):
        return super().save(self.topic_map.create_calendar)


class DatePeriodForm (AdminForm):

    def save (self):
        return super().save(self.topic_map.create_date_period)


class DateTypeForm (AdminForm):

    def save (self):
        return super().save(self.topic_map.create_date_type)


class EntityRelationshipForm (AdminForm):

    reverse_name = forms.CharField(max_length=100)

    def clean (self):
        # Ensure that the combination of name and reverse name is unique.
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name')
        reverse_name = cleaned_data.get('reverse_name')
        if name and reverse_name:
            try:
                existing = self.model.objects.get_by_admin_name(
                    name, reverse_name)
                if self.instance is None or self.instance != existing:
                    raise forms.ValidationError(
                        'The name of the %s must be unique' %
                        self.model._meta.verbose_name)
            except self.model.DoesNotExist:
                pass
        return self.cleaned_data

    def clean_name (self):
        return self.cleaned_data['name']

    def save (self):
        name = self.cleaned_data['name']
        reverse_name = self.cleaned_data['reverse_name']
        if self.instance is None:
            er_type = self.topic_map.create_entity_relationship_type(
                name, reverse_name)
        else:
            er_type = self.instance
            er_type.set_admin_name(name, reverse_name)
        return er_type

    def _topic_to_dict (self, topic):
        return {'name': topic.get_admin_forward_name(),
                'reverse_name': topic.get_admin_reverse_name()}


class EntityTypeForm (AdminForm):

    def save (self):
        return super().save(
            self.topic_map.create_entity_type)


class LanguageForm (AdminForm):

    code = forms.CharField(max_length=3)

    def __init__ (self, topic_map, model, data=None, instance=None, **kwargs):
        super().__init__(topic_map, model, data, instance,
                                           **kwargs)
        self.npt_base_name = 'name_part_type-'
        self._create_form_fields(data, self.initial)

    def clean (self):
        # Enforce uniqueness among the values of all the name part
        # type fields.
        name_part_type_values = []
        for field, value in list(self.cleaned_data.items()):
            if field.startswith(self.npt_base_name) and value:
                name_part_type_values.append(value)
        if len(name_part_type_values) != len(set(name_part_type_values)):
            raise forms.ValidationError(
                'Name part types may only be specified once')
        return self.cleaned_data

    def clean_code (self):
        code = self.cleaned_data['code']
        try:
            existing = self.model.objects.get_by_code(code)
            if self.instance is None or self.instance != existing:
                raise forms.ValidationError(
                    'The code of the %s must be unique' %
                    self.model._meta.verbose_name)
        except self.model.DoesNotExist:
            pass
        return code

    def _create_form_fields (self, post_data, instance_data):
        """Creates dynamic fields to accomodate the post/instance data.

        :param post_data: POSTed data
        :type post_data: dictionary
        :param instance_data: `Language` instance data
        :type instance_data: dictionary

        """
        name_part_type_choices = create_choice_list(
            self.topic_map, NamePartType.objects.all())
        data = post_data or instance_data
        count = 2
        for name in data:
            if name.startswith(self.npt_base_name):
                count += 1
        count = max(count, 3)
        for i in range(count):
            self.fields[self.npt_base_name + str(i)] = forms.ChoiceField(
                choices=name_part_type_choices, required=False,
                label='Name part type %s' % str(i+1))

    def _objectify_data (self, base_data):
        data = {}
        index = len(self.npt_base_name)
        for name, value in list(base_data.items()):
            if name.startswith(self.npt_base_name) and value:
                order = int(name[index:])
                data[order] = NamePartType.objects.get_by_identifier(value)
        keys = list(data.keys())
        keys.sort()
        name_part_types = []
        for key in keys:
            name_part_types.append(data[key])
        return name_part_types

    def save (self):
        name = self.cleaned_data['name']
        code = self.cleaned_data['code']
        name_part_types = self._objectify_data(self.cleaned_data)
        if self.instance is None:
            language = self.topic_map.create_language(name, code)
        else:
            language = self.instance
            language.set_admin_name(name)
            language.set_code(code)
        language.name_part_types = name_part_types
        return language

    def _topic_to_dict (self, topic):
        data = super()._topic_to_dict(topic)
        data['code'] = topic.get_code()
        name_part_types = topic.name_part_types
        for i in range(len(name_part_types)):
            name_part_type = name_part_types[i]
            data['name_part_type-' + str(i)] = name_part_type.get_id()
        return data


class NamePartTypeForm (AdminForm):

    def save (self):
        return super().save(
            self.topic_map.create_name_part_type)


class NameTypeForm (AdminForm):

    def save (self):
        return super().save(self.topic_map.create_name_type)


class ScriptForm (AdminForm):

    code = forms.CharField(max_length=4)
    separator = forms.CharField(initial=' ', max_length=10, required=False)

    def clean_code (self):
        code = self.cleaned_data['code']
        try:
            existing = self.model.objects.get_by_code(code)
            if self.instance is None or self.instance != existing:
                raise forms.ValidationError(
                    'The code of the %s must be unique' %
                    self.model._meta.verbose_name)
        except self.model.DoesNotExist:
            pass
        return code

    def save (self):
        name = self.cleaned_data['name']
        code = self.cleaned_data['code']
        separator = self.cleaned_data['separator']
        if self.instance is None:
            script = self.topic_map.create_script(name, code, separator)
        else:
            script = self.instance
            script.set_admin_name(name)
            script.set_code(code)
            script.separator = separator
        return script

    def _topic_to_dict (self, topic):
        data = super()._topic_to_dict(topic)
        data['code'] = topic.get_code()
        data['separator'] = topic.separator
        return data
