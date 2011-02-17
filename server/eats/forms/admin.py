from django import forms

from eats.api.topic_map import authority_exists


class AuthorityForm (forms.Form):

    name = forms.CharField(max_length=100)

    def __init__ (self, topic_map, authority_id, *args, **kwargs):
        """Initialise the form.

        :param topic_map: the EATS Topic Map
        :type topic_map: `TopicMap`
        :param authority_id: the `Identifier` id of the authority topic
        :type authority_id: integer or None

        """
        self._topic_map = topic_map
        self._authority_id = authority_id
        super(AuthorityForm, self).__init__(*args, **kwargs)

    def clean_name (self):
        name = self.cleaned_data['name']
        if authority_exists(self._topic_map, name, self._authority_id):
            raise forms.ValidationError(
                'The name of the authority must be unique')
        return name
