from django.db import models

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
    #TODO Opening Time
    #TODO Closing Time

class Address(models.Model):
    address_name = models.CharField(max_length=50,unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=5)

class City(models.Model):
    city_name = models.CharField(max_length=50,unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE())

class State(models.Model):
    state_name = models.CharField(max_length=25,unique=True)

class RatingChoices(models.IntegerChoices):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class Rating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ontime = models.IntegerField(choices=RatingChoices.choices)
    quality = models.IntegerField(choices=RatingChoices.choices)

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=140)
    price = models.DecimalField(max_digits=7, decimal_places=2)

class ProductDetails(models.Model):

class Order(models.Model):

class OrderItem(models.Model):