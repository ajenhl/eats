from django.db import models


class NameCache (models.Model):

    entity = models.ForeignKey('Entity', related_name='cached_names')
    assertion = models.ForeignKey('NamePropertyAssertion',
                                  related_name='cached_name', unique=True)
    name = models.ForeignKey('Name', related_name='cached_name', unique=True)
    authority = models.ForeignKey('Authority')
    form = models.CharField(max_length=800)
    is_preferred = models.BooleanField()
    language = models.ForeignKey('Language')
    script = models.ForeignKey('Script')

    class Meta:
        app_label = 'eats'
