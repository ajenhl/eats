import datetime

from django.db import models

from eats_user import EATSUser


class EATSMLImport (models.Model):

    importer = models.ForeignKey(EATSUser, related_name='eatsml_imports')
    description = models.CharField(max_length=200)
    raw_xml = models.TextField()
    annotated_xml = models.TextField()
    import_date = models.DateTimeField(editable=False)

    class Meta:
        app_label = 'eats'

    def save (self, *args, **kwargs):
        if not self.id:
            self.import_date = datetime.datetime.today()
        super(EATSMLImport, self).save(*args, **kwargs)
