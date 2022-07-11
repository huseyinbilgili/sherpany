from datetime import timedelta

import factory
from django.utils import timezone
from factory import fuzzy

from accounts.factories import UserFactory
from events.models import Attendance, Event


class EventFactory(factory.django.DjangoModelFactory):
    description = fuzzy.FuzzyText()
    date = timezone.now().date() + timedelta(days=30)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Event


class AttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attendance
