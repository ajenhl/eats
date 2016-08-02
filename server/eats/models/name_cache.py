from django.db import models


class NameCache (models.Model):

    """Model providing a "cache" of names, shortcutting the highly
    disaggregated topic map representation in order to improve
    performance.

    NameCache and NameIndex are both necessary: the index must be able
    to handle searches over two name parts that are joined by the
    empty string.

    """

    entity = models.ForeignKey('Entity', related_name='cached_names_for_entity')
    assertion = models.OneToOneField('NamePropertyAssertion',
                                     related_name='cached_name_for_assertion')
    name = models.OneToOneField('Name', related_name='cached_name_for_name')
    authority = models.ForeignKey('Authority', related_name='cached_names_for_authority')
    form = models.CharField(max_length=800)
    is_preferred = models.BooleanField(default=False)
    language = models.ForeignKey('Language', related_name='cached_names_for_language')
    script = models.ForeignKey('Script', related_name='cached_names_for_script')

    class Meta:
        app_label = 'eats'
