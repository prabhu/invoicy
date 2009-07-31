from django.contrib import admin
from clienty.models import Client, Contact

class ClientAdmin(admin.ModelAdmin):
    list_display = ('ref', 'short_name', 'name', 'phone')
    list_display_links = ('ref', 'short_name', 'name')
    search_fields = ['ref', 'name', 'short_name']
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
    
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_display_links = ('first_name', 'last_name', 'email')
    
admin.site.register(Client, ClientAdmin)
admin.site.register(Contact, ContactAdmin)
