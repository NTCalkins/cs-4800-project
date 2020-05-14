from eaterie.views import *
from eaterie.models import *
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


class TestAccountUpdateView(TestCase):

    def setup(self):

        #Set up the location information for the restaurant

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

        User = get_user_model()
        self.user1 = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        self.user1.is_customer = True

        Customer.objects.create(
            user=self.user1,
            customer_address="13119 Sienna Court",
            phone_number=8582544873,
            preference_1='ITA',
            preference_2='FF',
            zip_code=92129
        )

        self.user2 = User.objects.create_user(
            first_name="Tester",
            last_name="Testingtoner",
            password="I<3Testing1233",
            email="ttestington@cpep.edu",
        )

        self.user2.is_restaurant = True

        Restaurant.objects.create(
            user=self.user2,
            restaurant_name="McPomonas",
            restaurant_address="23663 MeadCliff Place",
            phone_number=8582545873,
            description="Testing",
            zip_code=zip_code,

        )

    def customer_account_update_view(self):

        request = RequestFactory().get('/account/{pk}/update', kwargs={'pk' : self.user1.id})
        request.user = self.user1
        response = AccountUpdateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

        request = RequestFactory().post('/account/{pk}/update', kwargs={'pk' : self.user1.id})
        request.user = self.user1
        response = AccountUpdateView.as_view()(request)
        response.get_form_kwargs()
        request.get_form_kwargs()
        self.assertEqual(response.status_code, 200)

