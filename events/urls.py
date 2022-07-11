from django.urls import path

from events.views import (
    AttendanceCreateView,
    AttendanceDeleteView,
    AttendanceView,
    EventCreateView,
    EventDetailView,
    EventListView,
    EventUpdateView,
    MyEventListView,
)

urlpatterns = [
    path("", EventListView.as_view(), name="event-list"),
    path("my-events", MyEventListView.as_view(), name="my-event-list"),
    path("create/", EventCreateView.as_view(), name="event-create"),
    path("detail/<int:pk>", EventDetailView.as_view(), name="event-detail"),
    path("update/<int:pk>", EventUpdateView.as_view(), name="event-update"),
    path("attended/", AttendanceView.as_view(), name="event-attended"),
    path("attend/<int:pk>", AttendanceCreateView.as_view(), name="event-attend"),
    path(
        "attend-delete/<int:pk>",
        AttendanceDeleteView.as_view(),
        name="event-attend-delete",
    ),
]
