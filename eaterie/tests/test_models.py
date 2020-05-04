from django.test import TestCase
from eaterie.models import *
from django.contrib.auth import get_user_model

class UserTest(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        self.assertEqual(user.email, 'ttestington@cpp.edu')
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Testington")
        self.assertEqual(user.email, "ttestington@cpp.edu")

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        self.assertEqual(admin_user.email, 'ttestington@cpp.edu')
        self.assertEqual(admin_user.first_name, "Test")
        self.assertEqual(admin_user.last_name, "Testington")
        self.assertEqual(admin_user.email, "ttestington@cpp.edu")

        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)