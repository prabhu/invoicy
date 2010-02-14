from django.contrib import admin
from clienty.models import Client, Contact, OwnCompany

class ClientAdmin(admin.ModelAdmin):
    list_display = ('ref', 'short_name', 'name')
    list_display_links = ('ref', 'short_name', 'name')
    search_fields = ['ref', 'name', 'short_name']
    exclude = ('user', 'own_company', 'currency',)
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
    
    # Django 1.1 feature.
    # This filters out my company from getting displayed in the list.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            kwargs["queryset"] = Client.objects.filter(user=request.user, own_company=False)
            return db_field.formfield(**kwargs)
        return super(ContactAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class OwnCompanyAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name',)
    list_display_links = ('short_name', 'name',)    
    exclude = ('user', 'own_company', 'ref')
    
    def queryset(self, request):
        """
        Show only rows specific to that user.
        """
        if request.user.is_superuser:
            return OwnCompany.objects.all()
        return OwnCompany.objects.filter(user=request.user, own_company=True)

    def save_model(self, request, obj, form, change):
        """
        Save user and groups with the model.
        """
        if request.user:
            obj.user = request.user
        # Own company would have username + name as ref.    
        obj.ref = request.user.username + '-' + obj.name
        obj.own_company = True
        obj.save()

admin.site.register(Client, ClientAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(OwnCompany, OwnCompanyAdmin)
