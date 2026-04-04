from django.contrib import admin
from .models import Meeting, ActionItem


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "owner")
    list_filter = ("date", "owner")
    search_fields = ("title", "owner")


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "meeting", "owner", "due_date", "status")
    list_filter = ("status", "owner")
    search_fields = ("description", "owner")

    @admin.action(description="Mark selected tasks as completed")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")
