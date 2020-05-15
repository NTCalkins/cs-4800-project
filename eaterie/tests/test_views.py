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

    def test_account_update_view(self):

        request = RequestFactory().get('/account/pk/update', kwargs={'pk' : self.user1.id } )
        request.user = self.user1
        response = AccountUpdateView.as_view()(request, pk=self.user1.id)
        self.assertEqual(response.status_code, 200)

        request = RequestFactory().post('/account/{pk}/update', kwargs={'pk' : 2})
        request.user = self.user2
        response = AccountUpdateView.as_view()(request, pk=self.user2.id)
        self.assertEqual(response.status_code, 200)

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

    def test_add_to_cart(self):
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
        self.assertEqual(response.status_code, 302)

        #MenuView.get_success_url(MenuView(request))


class TestMenuUpdateView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up the location information for the restaurant
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

    def test_menu_view(self):
        request = RequestFactory().get(
            '/restaurant/2/menu/update',
        )
        request.user = self.user2
        response = MenuUpdateView.as_view()(request, pk=self.restaurant.pk)

        self.assertEqual(response.status_code, 200)

class TestCartView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up the location information for the restaurant
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

        cls.customer = Customer.objects.create(
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

        cls.customer.cart.add_cart_item(menu_item_id=1, amount=10)

    def test_cart_view(self):
        request = RequestFactory().post(
            '/customer/cart',
        )

        request.user = self.user1
        request.POST._mutable = True
        request.POST['special_instructions'] = "Testing instructions"
        request.POST['cartpk'] = 1
        request.POST['item_amount'] = 12
        request.POST['item_amount_button'] = True
        response = CartView.as_view()(request, pk=self.customer.id)
        self.assertEqual(response.status_code, 302)
        request.POST['remove_from_cart_button'] = True
        request.POST['item_amount_button'] = False
        response = CartView.as_view()(request, pk=self.customer.id)
        self.assertEqual(response.status_code, 302)
        request.POST['remove_from_cart_button'] = False
        self.customer.cart.add_cart_item(menu_item_id=self.fooditem.id, amount=10)
        request.POST['checkout_button'] = True
        response = CartView.as_view()(request, pk=self.customer.id)
        self.assertEqual(response.status_code, 302)

class TestOrderListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up the location information for the restaurant
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

        # get the user that is the restaurant
        User = get_user_model()
        cls.restaurant_user = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        cls.restaurant_user.is_restaurant = True

        cls.restaurant = Restaurant.objects.create(
            restaurant_name="McPomonas",
            restaurant_address="23663 MeadCliff Place",
            phone_number=8582544873,
            description="Testing",
            zip_code=zip_code,
            user=cls.restaurant_user,
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

        cls.customer_user = User.objects.create_user(
            first_name="Terst",
            last_name="Testingrton",
            password="I<3Testing123",
            email="ttestington@cprp.edu",
        )

        cls.customer_user.is_customer = True

        cls.cust = Customer.objects.create(
            user=cls.customer_user,
            customer_address="13119 Sienna Court",
            phone_number=1582544873,
            preference_1='ITA',
            preference_2='FF',
            zip_code=91765
        )

        cls.order1 = Order.objects.create(
            restaurant=cls.restaurant,
            customer=cls.cust,
            special_instruction="Special instructions for testing",
        )

        cls.order1item = OrderItem.objects.create(
            menu_item=cls.fooditem,
            quantity=10,
            order=cls.order1
        )

        order2 = Order.objects.create(
            restaurant=cls.restaurant,
            customer=cls.cust,
            special_instruction="Second set of special instructions",
        )

        cls.review1 = Review.objects.create(
            order=cls.order1,
            comment="This is a public review",
            food_quality=5,
            timeliness=5,
            make_public=True
        )

    def test_order_list_views(self):

        request = RequestFactory().get(
            '/restaurant/orders',
        )
        request.user = self.restaurant_user
        response = OrderListView.as_view()(request, pk=self.restaurant_user.id)
        self.assertEqual(response.status_code, 200)

        request = RequestFactory().post(
            '/restaurant/orders',
        )
        request.user = self.restaurant_user
        request.POST._mutable = True
        request.POST['fulfill'] = True
        request.POST['order_id'] = self.order1.id
        response = OrderListView.as_view()(request, pk=self.restaurant_user.id)
        self.assertEqual(response.status_code, 302)

        #Check if the order can be cancelled
        request = RequestFactory().post(
            '/restaurant/orders',
        )
        request.POST._mutable = True
        request.POST['cancel'] = True
        request.POST['order_id'] = self.order1.id
        request.user = self.restaurant_user
        response = OrderListView.as_view()(request, pk=self.restaurant_user.id)
        self.assertEqual(response.status_code, 302)

        request = RequestFactory().get(
            '/customer/orders',
        )
        request.user = self.customer_user
        response = OrderListView.as_view()(request, pk=self.customer_user.id)
        self.assertEqual(response.status_code, 200)




