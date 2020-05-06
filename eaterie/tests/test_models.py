from decimal import Decimal
from os import truncate

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

        user.is_customer = True

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
        self.assertEqual(customer.get_avatar(),'blank-profile-picture.png')


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


class RestaurantTest(TestCase):
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

        #get the user that is the restaurant
        User = get_user_model()
        cls.user = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        cls.user.is_restaurant = True

        restaurant = Restaurant.objects.create(
            restaurant_name="McPomonas",
            restaurant_address="23663 MeadCliff Place",
            phone_number=8582544873,
            description="Testing",
            zip_code=zip_code,
            user=cls.user,
        )

        category = MenuCategory.objects.create(
            category_name="Burgers",
            restaurant=restaurant
        )

        fooditem = MenuItem.objects.create(
            item_name="TestBurger",
            description="Testing",
            price=54.99,
            category=category
        )

        customer_user = User.objects.create_user(
            first_name="Terst",
            last_name="Testingrton",
            password="I<3Testing123",
            email="ttestington@cprp.edu",
        )

        customer_user.is_customer = True

        cust = Customer.objects.create(
            user=customer_user,
            customer_address="13119 Sienna Court",
            phone_number=1582544873,
            preference_1='ITA',
            preference_2='FF',
            zip_code=91765
        )

        order1 = Order.objects.create(
            restaurant=restaurant,
            customer=cust,
            special_instruction="Special instructions for testing",
            order_cancelled=True
        )
        order2 = Order.objects.create(
            restaurant=restaurant,
            customer=cust,
            special_instruction="Second set of special instructions",
        )

        review1 = Review.objects.create(
            order=order1,
            comment="This is a public review",
            food_quality=5,
            timeliness=5,
            make_public=True
        )

        review2 = Review.objects.create(
            order=order2,
            comment="This is a nonpublic review",
            food_quality=1,
            timeliness=1,
        )

    @python_2_unicode_compatible
    def test_getters(self):

        restaurant = Restaurant.objects.get(restaurant_name="McPomonas")
        self.assertEqual(restaurant.__str__(), "McPomonas")
        self.assertEqual(restaurant.get_name(), "McPomonas")
        self.assertEqual(restaurant.get_address(), "23663 MeadCliff Place")
        self.assertEqual(restaurant.get_phone_number(), "8582544873")
        self.assertEqual(restaurant.get_image_file(),"no-image-available.png")
        self.assertEqual(restaurant.get_description(), "Testing")
        self.assertEqual(restaurant.get_zip_code(), ZipCode.objects.get(zip_code="91765"))
        self.assertEqual(restaurant.get_user(), self.user)

        # self.assertQuerysetEqual(restaurant.get_public_reviews(), Review.objects.filter(Q(make_public=True)))
        # self.assertQuerysetEqual(restaurant.get_all_reviews(), Review.objects.filter(Q(order__restaurant=self)))
        #
        # self.assertQuerysetEqual(restaurant.get_orders(), Order.objects.all(), ordered=False)

        self.assertEqual(restaurant.get_cancelled_orders_percentage(), 50)

        self.assertEqual(restaurant.get_average_price(), "$$$$")

        self.assertEqual(restaurant.get_food_quality(), "★★★★★")

        self.assertEqual(restaurant.get_timeliness(), "★★★★★")

class CategoryTest(TestCase):
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
        cls.user = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        cls.user.is_restaurant = True

        cls.restaurant = Restaurant.objects.create(
            restaurant_name="McPomonas",
            restaurant_address="23663 MeadCliff Place",
            phone_number=8582544873,
            description="Testing",
            zip_code=zip_code,
            user=cls.user,
        )

        category = MenuCategory.objects.create(
            category_name="Burgers",
            restaurant=cls.restaurant
        )

        fooditem = MenuItem.objects.create(
            item_name="TestBurger",
            description="Testing",
            price=54.99,
            category=category
        )

    def test_getters(self):
        category = MenuCategory.objects.get(
            restaurant=self.restaurant,
            category_name="Burgers"
        )

        self.assertEqual(category.__str__(), "Burgers")
        self.assertEqual(category.get_category_name(), "Burgers")
        self.assertEqual(category.get_restaurant(), self.restaurant)
        #TODO GET MENU ITEMS


class MenuItemTest(TestCase):
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
        cls.user = User.objects.create_user(
            first_name="Test",
            last_name="Testington",
            password="I<3Testing123",
            email="ttestington@cpp.edu",
        )

        cls.user.is_restaurant = True

        restaurant = Restaurant.objects.create(
            restaurant_name="McPomonas",
            restaurant_address="23663 MeadCliff Place",
            phone_number=8582544873,
            description="Testing",
            zip_code=zip_code,
            user=cls.user,
        )

        cls.category = MenuCategory.objects.create(
            category_name="Burgers",
            restaurant=restaurant
        )

        fooditem = MenuItem.objects.create(
            item_name="TestBurger",
            description="Testing",
            price=54.99,
            category=cls.category
        )

    def test_getters(self):

        menu_item = MenuItem.objects.get(category=self.category,
                                         item_name="TestBurger")

        self.assertEqual(menu_item.__str__(), "TestBurger(s) from McPomonas")
        self.assertEqual(menu_item.get_name(), "TestBurger")
        self.assertEqual(menu_item.get_description(), "Testing")
        self.assertEqual(menu_item.get_image_file(), "no-image-available.png")
        self.assertEqual(menu_item.get_price(), Decimal('54.99'))
        self.assertEqual(menu_item.get_category(), self.category)






