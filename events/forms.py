from django import forms

from events.models import Event


class DateInput(forms.DateInput):
    input_type = "date"


class EventCreateForm(forms.ModelForm):
    title = forms.CharField(min_length=2)

    class Meta:
        model = Event
        fields = ["title", "description", "date"]
        widgets = {"date": DateInput()}


class EventUpdateForm(EventCreateForm):
    pass
