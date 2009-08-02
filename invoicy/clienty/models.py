from django.db import models
from django.contrib.auth.models import User, Group
from common.utils.middleware import get_current_user

class Client(models.Model):
    """
    Model representing a customer.
    """
    ref = models.CharField(max_length=15, verbose_name='Client Ref#', help_text="Unique reference number for this client. Eg: CL123", unique=True)
    short_name = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    addr1 = models.CharField(max_length=45, verbose_name="Building")
    addr2 = models.CharField(max_length=45, verbose_name="Street Name")
    addr3 = models.CharField(max_length=45, null=True, blank=True, verbose_name="Address Line 3")
    postcode = models.CharField(max_length=9)
    city = models.CharField(max_length=45, null=True, blank=True)
    state = models.CharField(max_length=45, verbose_name="State/County", null=True, blank=True)
    country = models.CharField(max_length=45, verbose_name="Country", default="United Kingdom")
    website = models.URLField(null=True, verify_exists=True, max_length=100, verbose_name="Website", blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    fax = models.CharField(max_length=25, null=True, blank=True)
    user = models.ForeignKey(User, help_text="Owner user")
    own_company = models.BooleanField(verbose_name="Own Company", help_text="Is this your own company?")

    def __unicode__(self):
        return u'%s %s' %(self.ref, self.name)

    class Meta:
        permissions = (("can_generate_invoice", "Can generate invoice for the client"),)                       
        ordering = ['name']

    def save(self, **args):
        user = get_current_user()
        if user:
            self.user = user
        super(Client, self).save(args)

class Contact(models.Model):
    """
    Model representing a customer's contact. A customer can have multiple contacts.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=25, null=True, blank=True)
    home_phone = models.CharField(max_length=25, null=True, blank=True)
    work_phone = models.CharField(max_length=25, null=True, blank=True)
    nick = models.CharField(max_length=10, null=True, blank=True)
    company = models.ForeignKey(Client)
    primary = models.BooleanField(verbose_name='Primary Contact', help_text='Check if the person is a primary contact')
    user = models.ForeignKey(User, help_text="Owner user")
    
    def __unicode__(self):
        return u'%s %s' %(self.first_name, self.last_name)

    def save(self, **args):
        user = get_current_user()
        if user:
            self.user = user
        super(Contact, self).save(args)

class OwnCompany(Client):
    """
    Proxy model representing your own company.
    """
    class Meta:
        proxy = True
        verbose_name = 'My company'
        verbose_name_plural = 'My company'
        