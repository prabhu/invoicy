from django.db import models
from django.contrib.auth.models import User, Group
from common.utils.middleware import get_current_user
from clienty.models import Client

class Task(models.Model):
    """
    Model representing a task.
    """
    TASK_STATUS = (
        ('active', 'active'),
        ('complete', 'complete'),
        ('delivered', 'delivered'),
    )
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=120, help_text="Task description.")
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Rate in GBP.")
    status = models.CharField(max_length=15, choices=TASK_STATUS, default='active')
    user = models.ForeignKey(User, help_text="Owner user")
    client = models.ForeignKey(Client, null=False, help_text="Client paying for this task")
    
    def __unicode__(self):
        return u'%s %s' %(self.name, self.description)
    
    def save(self, **args):
        user = get_current_user()
        if user:
            self.user = user
        super(Task, self).save(args)
