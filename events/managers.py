from datetime import datetime

from django.db import models


class EventQuerySet(models.QuerySet):
    def actives(self):
        return self.filter(date__gte=datetime.now())

    def detailed(self):
        return self.actives().prefetch_related("attendees")


class AttendanceQuerySet(models.QuerySet):
    def detailed(self):
        return self.select_related("event", "user")
