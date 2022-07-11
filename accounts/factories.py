import factory

from accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = "sherpany@sherpany.com"

    class Meta:
        model = User
        django_get_or_create = ("email",)
