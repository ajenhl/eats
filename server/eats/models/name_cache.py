from django.db import models


class NameCache (models.Model):

    """Model providing a "cache" of names, shortcutting the highly
    disaggregated topic map representation in order to improve
    performance.

    NameCache and NameIndex are both necessary: the index must be able
    to handle searches over two name parts that are joined by the
    empty string.

    """

    entity = models.ForeignKey('Entity', related_name='cached_names')
    assertion = models.OneToOneField('NamePropertyAssertion',
                                     related_name='cached_name')
    name = models.OneToOneField('Name', related_name='cached_name')
    authority = models.ForeignKey('Authority')
    form = models.CharField(max_length=800)
    is_preferred = models.BooleanField(default=False)
    language = models.ForeignKey('Language')
    script = models.ForeignKey('Script')

    class Meta:
        app_label = 'eats'
