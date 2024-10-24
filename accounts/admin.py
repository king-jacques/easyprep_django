from django.contrib import admin
from .models import User, ActivityLog
# Register your models here.

admin.site.register(User)


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'type', 'timestamp')  # Fields to display in the list view
    search_fields = ('action', 'status', 'user', 'type')           # Fields that will be searchable
    list_filter = ('type', 'status', 'action')             # Fields you can filter by in the list view
    ordering = ('timestamp',)                         # Default ordering of the records

admin.site.register(ActivityLog, ActivityLogAdmin)