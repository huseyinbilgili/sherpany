from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from events.factories import AttendanceFactory, EventFactory
from events.models import Attendance, Event


class TestEventListView(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_get(self):
        EventFactory.create_batch(20, owner=self.user)
        response = self.client.get(reverse("event-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), settings.DEFAULT_PAGE_SIZE)


class TestEventCreateView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(user=self.user)

    def test_create_event__not_auth_user(self):
        self.client.logout()
        data = {"title": "Call Conference", "description": "Conference with team", "date": "2022-01-01"}
        response = self.client.post(path=reverse("event-create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/events/create/")

    def test_create_event__success(self):
        data = {"title": "Call Conference", "description": "Conference with team", "date": "2022-01-01"}
        response = self.client.post(path=reverse("event-create"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Event.objects.count(), 1)

    def test_create_event_failed(self):
        data = {"description": "Conference with team", "date": "2022-01-01"}
        response = self.client.post(path=reverse("event-create"), data=data)
        self.assertContains(response, "This field is required")


class TestEventUpdateView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(user=self.user)
        self.obj = EventFactory(owner=self.user)

    def test_update_event__not_auth_user(self):
        self.client.logout()
        data = {"title": "Call Conference"}
        response = self.client.post(path=reverse("event-update", kwargs={"pk": self.obj.pk}), data=data)
        self.assertEqual(response.status_code, 404)

    def test_update__dispatch(self):
        other_user = UserFactory(email="foo@bar.com")
        other_obj = EventFactory(owner=other_user)
        response = self.client.post(path=reverse("event-update", kwargs={"pk": other_obj.pk}), data={})
        self.assertEqual(response.status_code, 404)

    def test_update__success(self):
        data = {"title": "Changed Title", "description": self.obj.description, "date": self.obj.date}
        response = self.client.post(path=reverse("event-update", kwargs={"pk": self.obj.pk}), data=data)
        self.assertEqual(response.status_code, 302)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, "Changed Title")


class TestEventDetailView(TestCase):
    def setUp(self):
        self.obj = EventFactory()

    def test_get(self):
        user = UserFactory(email="foo@bar.com")
        AttendanceFactory(user=user, event=self.obj)
        self.client.force_login(user=user)

        response = self.client.get(path=reverse("event-detail", kwargs={"pk": self.obj.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.obj)
        self.assertTrue(response.context["is_attended"])

        self.obj.attendees.all().delete()
        response = self.client.get(path=reverse("event-detail", kwargs={"pk": self.obj.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.obj)
        self.assertFalse(response.context["is_attended"])


class TestMyEventListView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(user=self.user)

    def test_get__not_auth_user(self):
        self.client.logout()
        response = self.client.get(path=reverse("my-event-list"))
        self.assertEqual(response.status_code, 302)

    def test_get(self):
        event = EventFactory(owner=self.user)
        response = self.client.get(reverse("my-event-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 1)
        self.assertEqual(response.context["object_list"][0], event)


class TestAttendanceView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(user=self.user)

    def test_get__not_auth_user(self):
        self.client.logout()
        response = self.client.get(path=reverse("event-attended"))
        self.assertEqual(response.status_code, 302)

    def test_get(self):
        event = EventFactory(owner=UserFactory(email="foo@bar.com"))
        AttendanceFactory(user=self.user, event=event)
        response = self.client.get(path=reverse("event-attended"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["object_list"])
        self.assertEqual(response.context["object_list"][0].event, event)


class TestAttendanceCreateView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(user=self.user)
        self.event = EventFactory(owner=UserFactory(email="foo@bar.com"))

    def test_post__not_auth_user(self):
        self.client.logout()
        response = self.client.post(path=reverse("event-attend", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/accounts/login/?next=/events/attend/{self.event.pk}")

    def test_post__success(self):
        response = self.client.post(path=reverse("event-attend", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/events/")
        self.assertEqual(Attendance.objects.count(), 1)


class TestAttendanceDeleteView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(user=self.user)
        self.event = EventFactory(owner=UserFactory(email="foo@bar.com"))

    def test_get__not_auth_user(self):
        self.client.logout()
        response = self.client.get(path=reverse("event-attend-delete", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/accounts/login/?next=/events/attend-delete/{self.event.pk}")

    def test_post__success(self):
        AttendanceFactory(user=self.user, event=self.event)
        self.assertEqual(Attendance.objects.count(), 1)
        response = self.client.post(path=reverse("event-attend-delete", kwargs={"pk": self.event.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/events/")
        self.assertEqual(Attendance.objects.count(), 0)
