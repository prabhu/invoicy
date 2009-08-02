from django.contrib import admin
from django.db.models import Q

from invoicy.exporty.models import InvoiceTemplate

class InvoiceTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name', 'description',]
    exclude = ('user',)
    actions = ['make_public', 'make_private']
    
    fieldsets = (
        (None, {
            'fields' : ('template', 'type')
        }
        ),
        ('More options', {
            'classes' : ('collapse',),
            'fields' : ('description', 'name', 'is_public'),
        }
        ),
    )

    def make_public(self, request, queryset):
        rows = queryset.filter(user=request.user).update(is_public=True)
        if rows == 1:
            message = "1 template was"
        else:
            message = "%s templates were" %rows
        self.message_user(request, "%s made public" %message)
    make_public.short_description = 'Make selected templates public'   
        
    def make_private(self, request, queryset):
        rows = queryset.filter(user=request.user).update(is_public=False)
        if rows == 1:
            message = "1 template was"
        else:
            message = "%s templates were" %rows
        self.message_user(request, "%s made private" %message)
    make_private.short_description = "Make selected templates private"   

    def queryset(self, request):
        """
        Show only templates that are created by the user or is public.
        """
        if request.user.is_superuser:
            return InvoiceTemplate.objects.all()
        return InvoiceTemplate.objects.filter(
                Q(user=request.user) |
                Q(is_public=True)
               )

    def save_model(self, request, obj, form, change):
        """
        Save user with the model.
        """
        if request.user:
            obj.user = request.user
        obj.save()
    
admin.site.register(InvoiceTemplate, InvoiceTemplateAdmin)
