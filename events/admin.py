from django.contrib import admin

from events.models import Attendance, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    search_fields = ("title",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "event__title")
    list_display = ("event", "user")
