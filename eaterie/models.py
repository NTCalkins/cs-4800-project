import pytz
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from eaterie.validators import *
from django.utils import timezone
from datetime import datetime


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError(_('Superuser must have is_staff=True.'))
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_customer = models.BooleanField('customer status', default=False)
    is_restaurant = models.BooleanField('restaurant owner status', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_email(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name


class State(models.Model):
    state_code = models.CharField(primary_key=True, max_length=2)
    state_name = models.CharField(max_length=30)

    def __str__(self):
        return self.state_code

    def get_name(self):
        return self.state_name

    def get_code(self):
        return self.state_code


class City(models.Model):
    city_name = models.CharField(max_length=40)
    state_code = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city_name

    def get_city_name(self):
        return self.city_name

    def get_state(self):
        return self.state_code


class ZipCode(models.Model):
    zip_code = models.CharField(primary_key=True, max_length=5)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.zip_code

    def get_zip_city_state(self):
        zip = self.zip_code
        city = self.city.get_city_name()
        state = self.city.get_state().get_name()
        return zip + " " + city + ", " + state

    def get_zip(self):
        return self.zip_code


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=80)
    restaurant_address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=10)
    image_file = models.ImageField(default='no-image-available.png', blank=True)
    description = models.TextField(max_length=256, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.restaurant_name

    def get_name(self):
        return self.restaurant_name

    def get_categories(self):
        return MenuCategory.objects.filter(restaurant=self)

    def get_address(self):
        return self.restaurant_address

    def get_phone_number(self):
        return self.phone_number

    def get_image_file(self):
        return self.image_file

    def get_description(self):
        return self.description

    def get_zip_code(self):
        return self.zip_code

    def get_user(self):
        return self.user

    def get_public_reviews(self):
        return Review.objects.filter(
            Q(order__restaurant=self),
            Q(make_public=True)
        )

    def get_all_reviews(self):
        return Review.objects.filter(
            Q(order__restaurant=self)
        )

    def get_orders(self):
        return Order.objects.filter(restaurant=self)

    def get_cancelled_orders_percentage(self):
        orders = self.get_orders()
        total_orders = orders.count()
        cancel_orders = orders.filter(order_cancelled=True).count()
        if cancel_orders == 0:
            return 0
        else:
            return (cancel_orders / total_orders) * 100

    def get_average_price(self):
        categories = MenuCategory.objects.filter(restaurant=self)
        total_price = 0
        total_items = 0
        for c in categories:
            food_items = MenuItem.objects.filter(category=c).values()
            for f in food_items:
                total_price += f["price"]
                total_items += 1
                # print(f)
        if total_items == 0:
            return "Not enough data for average price"
        else:
            average = int(total_price / total_items)
            '''Everything below this designates the difference
            in average price values that will return $, $$, etc.'''
            if average <= 10:
                return "$"
            if 10 < average <= 20:
                return "$$"
            if 20 < average <= 30:
                return "$$$"
            else:
                return "$$$$"

    @python_2_unicode_compatible
    def get_food_quality(self):
        total_ratings = 0
        actual_ratings = 0
        ratings = self.get_public_reviews().values()
        for r in ratings:
            actual_ratings += r['food_quality']
            total_ratings += 1
            # print(r)
        if total_ratings == 0:
            return "No Ratings Yet"
        average = int(actual_ratings / total_ratings)
        if average == 1:
            return "★"
        elif average == 2:
            return "★★"
        elif average == 3:
            return "★★★"
        elif average == 4:
            return "★★★★"
        else:
            return "★★★★★"

    @python_2_unicode_compatible
    def get_timeliness(self):
        total_ratings = 0
        actual_ratings = 0
        orders = Order.objects.filter(restaurant=self)
        for o in orders:
            ratings = self.get_public_reviews().values()
            for r in ratings:
                actual_ratings += r['timeliness']
                total_ratings += 1
                # print(r)
        if total_ratings == 0:
            return "No Ratings Yet"
        average = int(actual_ratings / total_ratings)
        if average == 1:
            return "★"
        elif average == 2:
            return "★★"
        elif average == 3:
            return "★★★"
        elif average == 4:
            return "★★★★"
        else:
            return "★★★★★"


class Customer(models.Model):
    customer_address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    avatar = models.ImageField(default='blank-profile-picture.png', blank=True)
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    PREFERENCE_CHOICES = [
        ('ITA', 'Italian'),
        ('FF', 'Fast Food'),
        ('CHN', 'Chinese'),
        ('VTN', 'Vietnamese'),
        ('MEX', 'Mexican'),
    ]
    preference_1 = models.CharField(max_length=64, choices=PREFERENCE_CHOICES, default='ITA')
    preference_2 = models.CharField(max_length=64, choices=PREFERENCE_CHOICES, default='VTN')
    zip_code = models.CharField(max_length=5, blank=True)

    def get_user(self):
        return self.user

    def get_cart(self):
        return Cart.objects.get(customer=self)

    def __str__(self):
        return self.user.get_email()

    def get_address(self):
        return self.customer_address

    def get_phone_number(self):
        return self.phone_number

    def get_avatar(self):
        return self.avatar

    def get_preference1(self):
        return self.preference_1

    def get_preference2(self):
        return self.preference_2

    def get_zip_code(self):
        return self.zip_code

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user_cart, created = Cart.objects.get_or_create(customer=self)
        user_cart.save()


class MenuCategory(models.Model):
    category_name = models.CharField(max_length=60)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)

    class Meta:
        # one restaurant won't allow duplicate menu categories
        unique_together = ('category_name', 'restaurant')
        verbose_name_plural = "MenuCategories"

    def __str__(self):
        return self.category_name

    def get_menu_items(self):
        return MenuItem.objects.filter(category=self)

    def get_category_name(self):
        return self.category_name

    def get_restaurant(self):
        return self.restaurant


class MenuItem(models.Model):
    item_name = models.CharField(max_length=80)
    description = models.TextField(max_length=512, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    image_file = models.ImageField(default='no-image-available.png', blank=True)
    # optional: choices = models.ManyToManyField(ItemChoices, blank=true)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name + "(s) from " + self.category.restaurant.restaurant_name

    def get_name(self):
        return self.item_name

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    def get_image_file(self):
        return self.image_file

    def get_category(self):
        return self.category


class Order(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    special_instruction = models.CharField(max_length=512, blank=True)
    order_fulfilled = models.BooleanField(default=False)
    order_cancelled = models.BooleanField(default=False)

    def flip_cancelled(self):
        self.order_cancelled = not self.order_cancelled
        self.save()

    def flip_fulfilled(self):
        self.order_fulfilled = not self.order_fulfilled
        self.save()

    def get_order_items(self):
        return OrderItem.objects.filter(order=self)

    def get_restaurant(self):
        return self.restaurant

    def get_customer(self):
        return self.customer

    def get_order_date(self):
        return self.order_date

    def get_special_instruction(self):
        return self.special_instruction

    def is_fulfilled(self):
        return self.order_fulfilled

    def is_cancelled(self):
        return self.order_cancelled

    def __str__(self):
        return "Order from " + self.restaurant.restaurant_name

    def get_total_cost(self):
        order_items = OrderItem.objects.filter(order=self)
        sum = 0
        for order_item in order_items:
            sum += order_item.get_price()
        return sum

    def get_date(self):
        date = self.order_date
        timezone = pytz.timezone("America/Los_Angeles")
        date_aware = date.astimezone(timezone)
        return date_aware.strftime("%x")

    def get_time(self):
        date = self.order_date
        timezone = pytz.timezone("America/Los_Angeles")
        date_aware = date.astimezone(timezone)
        return date_aware.strftime("%X")

    def get_review(self):
        review = Review.objects.get(order=self)
        return review


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_DEFAULT, default=None)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('order', 'menu_item')

    def __str__(self):
        return str(self.quantity) + " units of " + str(self.menu_item)

    def get_price(self):
        return self.menu_item.price * self.quantity

    def get_order(self):
        return self.order

    def get_menu_item(self):
        return self.menu_item

    def get_quantity(self):
        return self.quantity


class CartEntry(models.Model):
    """
    Cart entry that is linked to a specific user's cart (ForeignKey cart).
    """
    cart = models.ForeignKey("Cart", null=True, on_delete='CASCADE')
    menu_item = models.ForeignKey(MenuItem, null=True, on_delete='CASCADE')
    quantity = models.PositiveIntegerField()

    def get_cart(self):
        return self.cart

    def get_menu_item(self):
        return self.menu_item

    def get_quantity(self):
        return self.quantity

    def get_price(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return str(self.quantity) + " " + str(self.menu_item)


class Cart(models.Model):
    """
    The Cart model that will hold CartEntrys related to a user's unique cart.
    """
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        primary_key=True
    )  # gives each customer has their unique cart
    menu_items = models.ManyToManyField(MenuItem, blank=True)
    total_cost = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def calculate_total_cost(self):
        cart_entries = CartEntry.objects.filter(cart=self)
        sumCost = 0
        for entry in cart_entries:
            sumCost += CartEntry.get_price(entry)
        return sumCost

    def get_cart_entries(self):
        return CartEntry.objects.filter(cart=self)

    def get_cart_quantity(self):
        cart_entries = self.get_cart_entries()
        cartTotal = 0
        for entry in cart_entries:
            cartTotal += entry.quantity
        return cartTotal

    def add_cart_item(self, menu_item_id, amount):
        """
        Adds a menu item to a user's cart.
        """

        try:
            item = MenuItem.objects.get(pk=menu_item_id)  # will access the MenuItem that user is trying to add to cart
            try:  # if the cart entry already exists, just increment that item's quantity
                item_exists = CartEntry.objects.get(cart=self, menu_item=item)
                item_exists.quantity += amount
                item_exists.save()
            except CartEntry.DoesNotExist:  # create a new cart entry with this item
                new_entry = CartEntry.objects.create(cart=self, menu_item=item, quantity=amount)
                new_entry.save()
        except ObjectDoesNotExist:  # checks that the item is reachable
            pass

    def change_quantity_cart_item(self, cart_entry_item_id, amount):
        """
        Changes quantity of an item in a user's cart.
        """

        try:
            # will access the MenuItem the user is trying to change quantity of
            item = MenuItem.objects.get(pk=cart_entry_item_id)
            try:  # if the cart entry already exists, just change that item's quantity
                item_exists = CartEntry.objects.get(cart=self, menu_item=item)
                item_exists.quantity = amount
                item_exists.save()
                if item_exists.quantity == 0:  # if the quantity is 0, delete CartEntry
                    item_exists.delete()
            except CartEntry.DoesNotExist:  # this shouldn't be encountered, but if so
                pass
        except ObjectDoesNotExist:  # checks that the item is reachable
            pass

    def delete_cart_item(self, cart_entry_item_id):
        """
        Deletes entire cart entry from a user's cart
        """

        try:
            # will access the MenuItem the user is trying to delete from cart
            item = MenuItem.objects.get(pk=cart_entry_item_id)
            try:  # if the cart item exists, then delete the item
                item_exists = CartEntry.objects.get(cart=self, menu_item=item)
                item_exists.delete()
            except CartEntry.DoesNotExist:  # this shouldn't be encountered, but if so
                pass
        except ObjectDoesNotExist:  # checks that the item is reachable
            pass

    def checkout(self):
        """
        Creates an Order from the CartEntrys in the user's cart.
        """

        cart_entries = self.get_cart_entries()
        if not cart_entries:
            # print("Unable to make order, nothing in cart!")
            return
        restaurants = set()
        # print(cart_entries)

        # Get a unique set of the restaurants in the cart order O(cart_entries.length)
        for cart_entry in cart_entries:
            restaurants.add(cart_entry.get_menu_item().get_category().get_restaurant())

        for restaurant in restaurants:
            new_order = Order.objects.create(customer=self.customer, restaurant=restaurant)
            new_order.save()
            new_review = Review.objects.create(order=new_order)
            new_review.save()
            for cart_entry in cart_entries:
                if cart_entry.get_menu_item().get_category().get_restaurant() == restaurant:
                    new_order_item = OrderItem.objects.create(order=new_order, quantity=cart_entry.get_quantity(),
                                                              menu_item=cart_entry.get_menu_item())
                    cart_entry.delete()
                    new_order_item.save()

        # self.order_date = datetime.now()
        # new_order = Order.objects.create(customer=self.customer, order_date=self.order_date)
        # new_order.save()
        # # Populate the new order with its order items, and destroy all the cart items so it can be used again
        # for cart_entry in cart_entries:
        #     new_order_item = OrderItem.objects.create(order=new_order, quantity=cart_entry.quantity,
        #                                               menu_item=cart_entry.menu_item)
        #     new_order_item.save()
        #     cart_entry.delete()


class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=512, blank=True)
    food_quality = models.IntegerField(validators=[validate_ratings], default=3)
    timeliness = models.IntegerField(validators=[validate_ratings], default=3)
    make_public = models.BooleanField(default=False)

    def __str__(self):
        return str(self.food_quality) + "/5  food quality and " + str(self.timeliness) \
               + "/5 timeliness for " + str(self.order.get_restaurant())


    def get_order(self):
        return self.order

    def get_comment(self):
        return self.comment

    def get_food_quality(self):
        return self.food_quality

    def get_timeliness(self):
        return self.timeliness


