from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as django_now
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

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
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


class State(models.Model):
    state_code = models.CharField(primary_key=True, max_length=2)
    state_name = models.CharField(max_length=30)

    def __str__(self):
        return self.state_code


class City(models.Model):
    city_name = models.CharField(max_length=40)
    state_code = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city_name


class ZipCode(models.Model):
    zip_code = models.CharField(primary_key=True, max_length=5)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.zip_code


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=80)
    restaurant_address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=10)
    image_file = models.ImageField(default='no-image-available.png', blank=True)
    description = models.TextField(max_length=256, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.restaurant_name

    def get_average_price(self):
        categories = MenuCategory.objects.filter(restaurant=self)
        total_price = 0
        total_items = 0
        for c in categories:
            food_items = MenuItem.objects.filter(category=c).values()
            for f in food_items:
                total_price += f["price"]
                total_items += 1
                print(f)
        if total_items == 0:
            return 0
        else:
            return total_price / total_items


class Customer(models.Model):
    customer_address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    avatar = models.ImageField(default='blank-profile-picture.png', blank=True)
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    PREFERENCE_CHOICES = [
        ('ITA', 'Italian'),
        ('FF', 'Fastfood'),
        ('CHN', 'Chinese'),
        ('VTN', 'Vietnamese')
    ]
    preference_1 = models.CharField(max_length=64, choices=PREFERENCE_CHOICES, default='ITA')
    preference_2 = models.CharField(max_length=64, choices=PREFERENCE_CHOICES, default='VTN')
    zip_code = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user_cart, created = Cart.objects.get_or_create(customer=self)
        if not created:
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


class MenuItem(models.Model):
    item_name = models.CharField(max_length=80)
    description = models.TextField(max_length=512, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    image_file = models.ImageField(default='no-image-available.png', blank=True)
    # optional: choices = models.ManyToManyField(ItemChoices, blank=true)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name + "(s) from " + self.category.restaurant.restaurant_name;


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=django_now)
    special_instruction = models.CharField(max_length=512, blank=True)
    order_fulfilled = models.BooleanField(default=False)
    order_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.user.email + " order made at: " + str(self.order_date)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_DEFAULT, default=None)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('order', 'menu_item')

    def __str__(self):
        return str(self.quantity) + " units of " + self.menu_item


class CartEntry(models.Model):
    """
    Cart entry that is linked to a specific user's cart (ForeignKey cart).
    """
    cart = models.ForeignKey("Cart", null=True, on_delete='CASCADE')
    menu_item = models.ForeignKey(MenuItem, null=True, on_delete='CASCADE')
    quantity = models.PositiveIntegerField()

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
        sum = 0
        for entry in cart_entries:
            sum += CartEntry.get_price(entry)
        return sum

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
            except CartEntry.DoesNotExist:  #create a new cart entry with this item
                new_entry = CartEntry.objects.create(cart=self, menu_item=item, quantity=amount)
                new_entry.save()
        except ObjectDoesNotExist:  # checks that the item is reachable
            pass

    def remove_cart_item(self, menu_item_id):
        """
        Removes a menu item from a user's cart.
        """

        try:
            item = MenuItem.objects.get(pk=menu_item_id)  # will access the MenuItem that user is trying to add to cart
            try:  # if the cart entry already exists, just decrement that item's quantity
                item_exists = CartEntry.objects.get(cart=self, menu_item=item)
                item_exists.quantity -= 1
                item_exists.save()
                if item_exists.quantity == 0:  # if the quantity is 0, delete CartEntry
                    item_exists.delete()
            except CartEntry.DoesNotExist:  # this shouldn't be encountered, but if so
                pass
        except ObjectDoesNotExist:  # checks that the item is reachable
            pass

    def checkout(self):
        """
        Creates an Order from the CartEntrys in the user's cart.
        """

        self.order_date = datetime.now()
        new_order = Order.objects.create(customer=self.customer, order_date=self.order_date)
        new_order.save()
        cart_entries = CartEntry.objects.filter(cart=self)
        # Populate the new order with its order items, and destroy all the cart items so it can be used again
        for cart_entry in cart_entries:
            new_order_item = OrderItem.objects.create(order=new_order, quantity=cart_entry.quantity,
                                                      menu_item=cart_entry.menu_item)
            cart_entry.delete()
