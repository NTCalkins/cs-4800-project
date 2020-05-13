from eaterie.views import *
from django.test import TestCase, RequestFactory, Client, SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestLoginRedirect(TestCase):

    def test_login_redirect(self):
        User = get_user_model()
        user = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        user.is_customer = True

        Customer.objects.create(
            user=user,
            customer_address="13119 Sienna Court",
            phone_number=8582544873,
            preference_1='ITA',
            preference_2='FF',
            zip_code=92129
        )

        self.client.login(user=user,password="I<3Testing123")

        req = self.client.request()
        req.user = user
        response = login_redirect(req)
        self.assertEqual(response.status_code, 302)

        req.user.is_customer = False
        req.user.is_restauarant = True

        response = login_redirect(req)
        self.assertEqual(response.status_code, 302)

        req.user.is_restauarant = False

        response = login_redirect(req)
        self.assertEqual(response.status_code, 302)


class TestCustomerHomeView(TestCase):

    def test_customer_home_view(self):
        User = get_user_model()
        user = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        user.is_customer = True

        Customer.objects.create(
            user=user,
            customer_address="13119 Sienna Court",
            phone_number=8582544873,
            preference_1='ITA',
            preference_2='FF',
            zip_code=92129
        )

        request = RequestFactory().get('/customer/lets-eat/')
        request.user = user

        response = CustomerHomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestAccountUpdateView(UpdateView):

    def setup(self, request, *args, **kwargs):


    def customer_account_update_view(self):

