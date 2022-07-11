from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView, UpdateView

from events.forms import EventCreateForm, EventUpdateForm
from events.models import Attendance, Event


class EventListView(ListView):
    """List all events."""

    queryset = Event.objects.detailed().order_by("-date")
    paginate_by = settings.DEFAULT_PAGE_SIZE
    template_name = "list.html"


class EventCreateView(LoginRequiredMixin, CreateView):
    """Create an event."""

    model = Event
    form_class = EventCreateForm
    template_name = "create.html"
    success_url = reverse_lazy("event-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EventDetailView(DetailView):
    """Display event details."""

    model = Event
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["is_attended"] = self.object.attendees.filter(user=self.request.user).exists()
        return context


class EventUpdateView(LoginRequiredMixin, UpdateView):
    """Update event"""

    model = Event
    template_name = "update.html"
    success_url = reverse_lazy("event-list")
    form_class = EventUpdateForm

    def dispatch(self, request, *args, **kwargs):
        """
        check event owner.
        """
        if self.get_object().owner != request.user:
            raise Http404
        return super(EventUpdateView, self).dispatch(request, *args, **kwargs)


class MyEventListView(LoginRequiredMixin, ListView):
    """Logged in user's events are listing."""

    queryset = Event.objects.detailed().order_by("-date")
    paginate_by = settings.DEFAULT_PAGE_SIZE
    template_name = "list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class AttendanceView(LoginRequiredMixin, ListView):
    """Logged in user's attended events are listing."""

    queryset = Attendance.objects.detailed().order_by("pk")
    paginate_by = settings.DEFAULT_PAGE_SIZE
    template_name = "my_attended.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class AttendanceCreateView(LoginRequiredMixin, RedirectView):
    """Attend an event."""

    url = reverse_lazy("event-list")

    def get_redirect_url(self, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs.get("pk"))
        attendance, _ = Attendance.objects.get_or_create(user=self.request.user, event=event)

        return super().get_redirect_url(*args, **kwargs)


class AttendanceDeleteView(LoginRequiredMixin, RedirectView):
    """Might be soft delete."""

    url = reverse_lazy("event-list")

    def get_redirect_url(self, *args, **kwargs):
        event = get_object_or_404(Event, pk=kwargs.get("pk"))
        Attendance.objects.get(user=self.request.user, event=event).delete()

        return super().get_redirect_url(*args, **kwargs)
