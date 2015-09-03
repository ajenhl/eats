"""Module containing admin-related model forms.

These are kept separate from the other admin forms due to the
behaviour commented on in views/admin.py in the user_change
function.

"""

from django import forms

from eats.models import EATSUser


class EATSUserForm (forms.ModelForm):

    class Meta:
        model = EATSUser
        exclude = ('editable_authorities', 'current_authority', 'user')
