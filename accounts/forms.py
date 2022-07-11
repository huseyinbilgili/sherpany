from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)

from accounts.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)
