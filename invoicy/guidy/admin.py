from django.contrib import admin
from guidy.models import Task
from clienty.models import Client

def make_delivered(modeladmin, request, queryset):
    rows_updated = queryset.update(status='delivered')
    modeladmin.message_user(request, "%s tasks successfully marked as delivered."%rows_updated)
make_delivered.short_description = "Mark tasks as delivered"

def make_active(modeladmin, request, queryset):
    rows_updated = queryset.update(status='active')
    modeladmin.message_user(request, "%s tasks successfully marked as active."%rows_updated)
make_active.short_description = "Mark tasks as active"

def make_complete(modeladmin, request, queryset):
    rows_updated = queryset.update(status='complete')
    modeladmin.message_user(request, "%s tasks successfully marked as complete."%rows_updated)    
make_complete.short_description = "Mark tasks as complete"

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'rate', 'status')
    list_display_links = ('name',)
    search_fields = ['name', 'description']
    exclude = ('user', )
    actions = [make_delivered, make_complete, make_active,]
    
    def queryset(self, request):
        """
        Show only rows specific to that user.
        """
        if request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(user=request.user)
        
    def save_model(self, request, obj, form, change):
        """
        Save user with the model.
        """
        if request.user:
            obj.user = request.user
        obj.save()

    # Django 1.1 feature.
    # This filters out my company from getting displayed in the list.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "client":
            kwargs["queryset"] = Client.objects.filter(user=request.user, own_company=False)
            return db_field.formfield(**kwargs)
        return super(TaskAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Task, TaskAdmin)
