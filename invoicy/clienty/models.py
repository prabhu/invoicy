from django.db import models

class Client(models.Model):
    ref = models.CharField(max_length=15, help_text="Unique reference number for this client.", unique=True)
    short_name = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=100, unique=True)
    addr1 = models.CharField(max_length=45)
    addr2 = models.CharField(max_length=45)
    add3 = models.CharField(max_length=45, null=True)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    website = models.URLField(null=True)
    phone = models.CharField(max_length=25)
    fax = models.CharField(max_length=25, null=True)
    
    def __unicode__(self):
        return u'%s %s' %(self.ref, self.name)
            
class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=25, null=True)
    home_phone = models.CharField(max_length=25, null=True)
    work_phone = models.CharField(max_length=25, null=True)
    nick = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return u'%s %s' %(self.first_name, self.last_name)
