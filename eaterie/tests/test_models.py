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

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        self.assertEquals(user._meta.get_field('first_name').verbose_name, 'first name')
        self.assertEquals(user._meta.get_field('last_name').verbose_name, 'last name')
        self.assertEquals(user._meta.get_field('email').verbose_name, 'email address')
        self.assertEquals(user._meta.get_field('password').verbose_name, 'password')

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

        self.assertEquals(admin_user._meta.get_field('first_name').verbose_name, 'first name')
        self.assertEquals(admin_user._meta.get_field('last_name').verbose_name, 'last name')
        self.assertEquals(admin_user._meta.get_field('email').verbose_name, 'email address')
        self.assertEquals(admin_user._meta.get_field('password').verbose_name, 'password')


class CustomerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        user = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        Customer.objects.create(
            user=user,
            customer_address="13119 Sienna Court",
            phone_number=8582544873,
            preference_1='ITA',
            preference_2='FF',
            zip_code=92129
        )

    def test_labels(self):
        customer = Customer.objects.get(id=1)

