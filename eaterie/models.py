from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


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

    def __str__(self):
        return self.user.email


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
        return self.item_name

# class Driver(models.Model):
#     phone_number = models.CharField(max_length=10)
#     zip_code = models.ForeignKey(ZipCode, on_delete=models.SET_NULL, blank=True, null=True)
#     user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.email
