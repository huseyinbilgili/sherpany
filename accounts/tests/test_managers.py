from django.test import TestCase

from accounts.managers import UserManager
from accounts.models import User


class TestUserManager(TestCase):
    def setUp(self):
        self.manager = UserManager()
        self.manager.model = User

    def test_create_superuser__success(self):
        user = self.manager.create_superuser(email="foo@bar.com", password="12345")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser__failed__is_staff(self):
        with self.assertRaises(ValueError):
            self.manager.create_superuser(email="foo@bar.com", password="12345", is_staff=False)

    def test_create_superuser__failed__is_superuser(self):
        with self.assertRaises(ValueError):
            self.manager.create_superuser(email="foo@bar.com", password="12345", is_superuser=False)

    def test_create_superuser__failed__without_email(self):
        with self.assertRaises(ValueError):
            self.manager.create_superuser(email=None, password="12345")

    def test_create_user(self):
        user = self.manager.create_user(email="foo@bar.com", password="12345")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
