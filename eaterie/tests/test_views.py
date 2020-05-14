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

    @classmethod
    def setUpTestData(cls):
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
        cls.user1 = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        cls.user1.is_customer = True

        Customer.objects.create(
            user=cls.user1,
            customer_address="13119 Sienna Court",
            phone_number=8582544873,
            preference_1='ITA',
            preference_2='FF',
            zip_code=92129
        )

        cls.user2 = User.objects.create_user(
            first_name="Tester",
            last_name="Testingtoner",
            password="I<3Testing1233",
            email="ttestington@cpep.edu",
        )

        cls.user2.is_restaurant = True

        Restaurant.objects.create(
            user=cls.user2,
            restaurant_name="McPomonas",
            restaurant_address="23663 MeadCliff Place",
            phone_number=8582545873,
            description="Testing",
            zip_code=zip_code,

        )

    def test_customer_account_update_view(self):

        request = RequestFactory().get('/account/pk/update', kwargs={'pk' : self.user1.id } )
        request.user = self.user1
        print(request)
        response = AccountUpdateView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)

        request = RequestFactory().post('/account/{pk}/update', kwargs={'pk' : 2})
        request.user = self.user2
        response = AccountUpdateView.as_view()(request, pk=2)
        self.assertEqual(response.status_code, 200)

        #TODO: Test get_success_url


class TestMenuView(TestCase):

    @classmethod
    def setUpTestData(cls):
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
        cls.user1 = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        cls.user1.is_customer = True

        Customer.objects.create(
            user=cls.user1,
            customer_address="13119 Sienna Court",
            phone_number=8582544873,
            preference_1='ITA',
            preference_2='FF',
            zip_code=92129
        )

        cls.user2 = User.objects.create_user(
            first_name="Tester",
            last_name="Testingtoner",
            password="I<3Testing1233",
            email="ttestington@cpep.edu",
        )

        cls.user2.is_restaurant = True

        cls.restaurant = Restaurant.objects.create(
            user=cls.user2,
            restaurant_name="McPomonas",
            restaurant_address="23663 MeadCliff Place",
            phone_number=8582545873,
            description="Testing",
            zip_code=zip_code,

        )

        category = MenuCategory.objects.create(
            category_name="Burgers",
            restaurant=cls.restaurant
        )

        cls.fooditem = MenuItem.objects.create(
            item_name="TestBurger",
            description="Testing",
            price=54.99,
            category=category
        )

    def test_adding_to_cart(self):
        request = RequestFactory().post(
            '/restaurant/2/menu',
        )
        request.user = self.user1
        request.POST._mutable = True
        request.POST['add_to_cart_button'] = "Add to cart"
        request.POST['mipk'] = 1
        request.POST['item_amount'] = 10
        response = MenuView.as_view()(
            request,
            pk=1,
            add_to_cart_button="Add to cart",
            mipk=1,
            item_amount=10
        )



