from django.contrib.auth.models import User
from django.db import models

from base_manager import BaseManager


class EditorManager (BaseManager):

    def get_query_set (self):
        return super(EditorManager, self).get_query_set().filter(
            editable_authorities__isnull=False)


class EATSUser (models.Model):

    user = models.OneToOneField(User, primary_key=True,
                                related_name='eats_user')
    language = models.ForeignKey('Language', related_name='language_users',
                                 null=True)
    script = models.ForeignKey('Script', related_name='script_users', null=True)
    editable_authorities = models.ManyToManyField('Authority',
                                                  related_name='editors')
    current_authority = models.ForeignKey('Authority', null=True,
                                          related_name='current_editors')

    objects = models.Manager()
    editors = EditorManager()
    
    class Meta:
        app_label = 'eats'

    def get_current_authority (self):
        # QAZ: Direct access to self.current_authority bypasses this
        # logic, which may lead to incorrect results. Implementing the
        # logic in the save method is insufficient to prevent this,
        # however, since changes to editable_authorities does not call
        # this save method.
        editable_authorities = self.editable_authorities.all()
        if self.current_authority is None and editable_authorities:
            self.current_authority = editable_authorities[0]
            self.save()
        elif self.current_authority not in editable_authorities:
            if editable_authorities:
                self.current_authority = editable_authorities[0]
            else:
                self.current_authority = None
            self.save()
        return self.current_authority
        
    def get_language (self):
        return self.language

    def get_script (self):
        return self.script

    def is_editor (self):
        if self.editable_authorities.count() > 0:
            return True
        return False

    def set_current_authority (self, authority):
        if authority not in self.editable_authorities.all():
            # QAZ: Raise specific exception with error message.
            raise Exception
        self.current_authority = authority
        self.save()

    def set_language (self, language):
        self.language = language
        self.save()

    def set_script (self, script):
        self.script = script
        self.save()
