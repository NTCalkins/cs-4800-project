import datetime

from django.test import TestCase
from django.utils import timezone

from eaterie.forms import *

class CustomerSignUpForm(TestCase):

    def test_user_creation(self):

        form = CustomerSignUpForm(
                data= {
                    'first_name' : "Test",
                    'last_name' : "Testington",
                    'email' : "ttestington@cpp.edu",
                    'password1' : '123123aaa',
                    'password2' : '123123aaa'
                }
            )

        form.save()

