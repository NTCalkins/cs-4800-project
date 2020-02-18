from django.db import models

class State(models.Model):
    state_name = models.CharField(max_length=25,unique=True)

class City(models.Model):
    city_name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

class Address(models.Model):
    address_name = models.CharField(max_length=50,unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=5)

class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50,unique=True)
    phone = models.CharField(max_length=10,unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Driver(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50,unique=True)
    phone = models.CharField(max_length=10,unique=True)

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    email = models.CharField(max_length=50,unique=True)
    phone = models.CharField(max_length=10,unique=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

class Delivery(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    is_fulfilled = models.BooleanField(default=False)
    amount_payable = models.DecimalField(max_digits=8, decimal_places=2)

class FoodItem(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=140)
    more_description = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    #TODO Image
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)

class FoodOrder(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class RatingChoices(models.IntegerChoices):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class Rating(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    driver_ontime = models.IntegerField(choices=RatingChoices.choices)
    driver_quality = models.IntegerField(choices=RatingChoices.choices)
    restaurant_ontime = models.IntegerField(choices=RatingChoices.choices)
    restaurant_quality = models.IntegerField(choices=RatingChoices.choices)