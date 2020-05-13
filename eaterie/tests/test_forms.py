import datetime

from django.test import TestCase
from django.utils import timezone

from eaterie.forms import *
from eaterie.models import *

class CustomerSignUpFormTest(TestCase):

    def test_user_creation(self):

        data = {
            'first_name': "Test",
            'last_name': "Testington",
            'email': "ttestington@cpp.edu",
            'password1': '123123aaa',
            'password2': '123123aaa',
        }

        form = CustomerSignUpForm(data)

        print(form)

        self.assertEqual(form.is_valid(), True)

        form.is_valid()

        print(form.errors)

        form.save()


class RestaurantSignUpFormTest(TestCase):

    def test_restaurant_creation(self):

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

        data = {
            'first_name' : "Ronald",
            'last_name' : "McDonald",
            'email' : "RMCDONALD@CPP.edu",
            'phone_number' : 1231231112,
            'restaurant_name' : "McDonalds",
            'password1' : '123123aaa',
            'password2' : '123123aaa',
            'zip_code' : 91765,
        }

        form = RestaurantSignUpForm(data)

        form.is_valid()

        self.assertEqual(form.is_valid(), True)

        self.assertEqual(form.clean_zip_code(), '91765')

        form.save()

        data = {
            'first_name' : "Ronald",
            'last_name' : "McDonald",
            'email' : "RMCDONALD@CPP.edu",
            'phone_number' : 1231231112,
            'restaurant_name' : "McDonalds",
            'password1' : '123123aaa',
            'password2' : '123123aaa',
            'zip_code' : 91766,
        }

        form = RestaurantSignUpForm(data)

        form.is_valid()

        self.assertEqual(form.is_valid(), False)



