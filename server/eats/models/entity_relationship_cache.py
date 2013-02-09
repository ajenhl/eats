from django.db import models


class EntityRelationshipCache(models.Model):
    """Model providing a "cache" of entity relationships, shortcutting the
    highly disaggregated topic map representation in order to improve
    performance.

    """
    entity_relationship = models.OneToOneField(
        'EntityRelationshipPropertyAssertion',
        related_name='cached_relationship', primary_key=True)
    authority = models.ForeignKey('Authority',
                                  related_name='cached_entity_relationships')
    domain_entity = models.ForeignKey('Entity',
                                      related_name='domain_relationships')
    range_entity = models.ForeignKey('Entity',
                                     related_name='range_relationships')
    relationship_type = models.ForeignKey('EntityRelationshipType',
                                          related_name='cached_relationships')
    forward_relationship_name = models.TextField()
    reverse_relationship_name = models.TextField()

    class Meta:
        app_label = 'eats'
