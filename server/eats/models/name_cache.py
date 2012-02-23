from django.db import models


class NameCache (models.Model):

    entity = models.ForeignKey('Entity', related_name='cached_names')
    name = models.ForeignKey('Name', related_name='cached_name', unique=True)
    form = models.CharField(max_length=800)
    language = models.ForeignKey('Language')
    script = models.ForeignKey('Script')
    authority = models.ForeignKey('Authority')

    class Meta:
        app_label = 'eats'
