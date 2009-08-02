from django.contrib import admin
from clienty.models import Client, Contact, OwnCompany

class ClientAdmin(admin.ModelAdmin):
    list_display = ('ref', 'short_name', 'name', 'phone')
    list_display_links = ('ref', 'short_name', 'name')
    search_fields = ['ref', 'name', 'short_name']
    exclude = ('user', 'own_company', )
    fieldsets = (
        (None, {
            'fields' : ('ref', 'short_name', 'name')
        }
        ),
        ('Client Address', {
            'classes' : ('collapse',),
            'fields' : ('addr1', 'addr2', 'addr3', 'postcode', 'city', 'state', 'country', 'website', 'phone', 'fax'),
        }
        ),
    )

    def queryset(self, request):
        """
        Show only rows specific to that user.
        """
        if request.user.is_superuser:
            return Client.objects.all()
        return Client.objects.filter(user=request.user, own_company=False)

    def save_model(self, request, obj, form, change):
        """
        Save user with the model.
        """
        if request.user:
            obj.user = request.user
        obj.save()

class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name', 'email')
    exclude = ('user',)

    def queryset(self, request):
        """
        Show only rows specific to that user.
        """
        if request.user.is_superuser:
            return Contact.objects.all()
        return Contact.objects.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """
        Save user and groups with the model.
        """
        if request.user:
            obj.user = request.user
        obj.save()

class OwnCompanyAdmin(admin.ModelAdmin):

    verbose_name = 'My Company'
    verbose_name_plural = 'My Company'
    exclude = ('user', 'own_company', 'ref')
    
    def queryset(self, request):
        """
        Show only rows specific to that user.
        """
        if request.user.is_superuser:
            return OwnCompany.objects.all()
        return OwnCompany.objects.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """
        Save user and groups with the model.
        """
        if request.user:
            obj.user = request.user
        # Own company would have username as ref.    
        obj.ref = request.user.username
        obj.own_company = True
        obj.save()

admin.site.register(Client, ClientAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(OwnCompany, OwnCompanyAdmin)
