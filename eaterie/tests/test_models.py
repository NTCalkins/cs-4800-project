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

        self.assertEqual(user.get_email(), 'ttestington@cpp.edu')
        self.assertEqual(user.get_first_name(), "Test")
        self.assertEqual(user.get_last_name(), "Testington")

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

        self.assertEqual(admin_user.get_email(), 'ttestington@cpp.edu')
        self.assertEqual(admin_user.get_first_name(), "Test")
        self.assertEqual(admin_user.get_last_name(), "Testington")

        self.assertEqual(admin_user.__str__(), "ttestington@cpp.edu")

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

    def test_getters(self):
        customer = Customer.objects.get(id=1)
        self.assertEqual(customer.user,customer.get_user())
        self.assertEqual(customer.cart, customer.get_cart())
        self.assertEqual(customer.__str__(), customer.user.email)
        self.assertEqual(customer.customer_address, customer.get_address())
        self.assertEqual(customer.user, customer.get_user())
        self.assertEqual(customer.phone_number, customer.get_phone_number())
        self.assertEqual(customer.preference_1, customer.get_preference1())
        self.assertEqual(customer.preference_2, customer.get_preference2())
        self.assertEqual(customer.zip_code, customer.get_zip_code())


class LocationTest(TestCase):

    def test_getters(self):

        state = State.objects.create(
            state_code="CA",
            state_name="California"
        )

        city = City.objects.create(
            city_name="Diamond Bar",
            state_code=State.objects.get(state_code="CA")
        )

        zip_code = ZipCode.objects.create(
            zip_code="91765",
            city=city
        )

        self.assertEqual(state.get_code(), "CA")
        self.assertEqual(state.get_name(), "California")
        self.assertEqual(state.__str__(), "CA")

        self.assertEqual(city.get_city_name(), "Diamond Bar")
        self.assertEqual(city.get_state(), state)
        self.assertEqual(city.__str__(), "Diamond Bar")

        self.assertEqual(zip_code.get_zip(), "91765")
        self.assertEqual(zip_code.get_zip_city_state(), "91765 Diamond Bar, California")
        self.assertEqual(zip_code.__str__(), "91765")

