from django.test import TestCase

from accounts.factories import UserFactory
from events.factories import AttendanceFactory, EventFactory


class TestEventModel(TestCase):
    def test_model_str(self):
        event = EventFactory(title="Conference Call", date="2022-01-02")
        self.assertEqual(
            str(event),
            "Title: Conference Call - Date: 2022-01-02",
        )


class TestAttendanceModel(TestCase):
    def test_model_str(self):
        event = EventFactory(
            title="Conference Call",
            date="2022-01-01",
        )
        user = UserFactory(email="foo@bar.com")
        attendance = AttendanceFactory(event=event, user=user)
        self.assertEqual(str(attendance), "Event: Conference Call - User: foo@bar.com")
