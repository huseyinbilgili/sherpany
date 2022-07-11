from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from events.managers import AttendanceQuerySet, EventQuerySet


class Event(models.Model):
    owner = models.ForeignKey(
        to=User, verbose_name=_("Owner"), on_delete=models.CASCADE
    )
    title = models.TextField(verbose_name=_("Title"))
    description = models.TextField(_("Description"))
    date = models.DateField(verbose_name=_("Date"))

    objects = EventQuerySet.as_manager()

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self):
        return f"Title : {self.title} - Date : {self.date}"


class Attendance(models.Model):
    event = models.ForeignKey(
        to=Event,
        verbose_name=_("Event"),
        on_delete=models.CASCADE,
        related_name="attendees",
    )
    user = models.ForeignKey(
        to=User, verbose_name=_("User"), on_delete=models.CASCADE
    )

    objects = AttendanceQuerySet.as_manager()

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendees")

    def __str__(self):
        return f"{self.event} - {self.user.email}"
