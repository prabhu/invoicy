from django.db import models
from django.contrib.auth.models import User, Group

from common.utils.middleware import get_current_user

class InvoiceTemplate(models.Model):
    TEMPLATE_TYPES = (
        ('html', 'html'),
        ('markdown', 'markdown'),
        ('rml', 'rml'),
    )
    name = models.CharField(max_length=50, unique=True, help_text="Meaningful name for this template")
    description = models.TextField(help_text="Description about this template.", blank=True, null=True)
    template = models.TextField(help_text="Your template goes here")
    type = models.CharField(max_length=8, choices=TEMPLATE_TYPES, default='html')
    is_public = models.BooleanField(verbose_name="Share this template", help_text="Check if you wish to share this template with other invoicy users.", default=False)    
    user = models.ForeignKey(User, help_text="Owner user")

    def __unicode__(self):
        return u'%s - %s'%(self.name, self.type)

    class Meta:
        ordering = ['name']

    def save(self, **args):
        user = get_current_user()
        if user:
            self.user = user
        super(InvoiceTemplate, self).save(args)
        