from django.db import models


class NameIndex (models.Model):

    entity = models.ForeignKey('Entity', related_name='indexed_names')
    name = models.ForeignKey('Entity', related_name='indexed_name_forms')
    form = models.CharField(max_length=800)

    class Meta:
        app_label = 'eats'
