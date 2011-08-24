from django import forms


class EntitySearchForm (forms.Form):

    name = forms.CharField(label='Name')
