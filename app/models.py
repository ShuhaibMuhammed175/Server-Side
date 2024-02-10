from accounts.models import User
from django.db import models


class Restaurant_location(models.Model):
    location = models.TextField(max_length=100)

    def __str__(self):
        return self.location


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    location = models.ForeignKey(Restaurant_location, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField()
    email = models.EmailField()
    description = models.TextField()
    address = models.CharField(max_length=100)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return self.name


class Restaurant_image(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images/')

    def __str__(self):
        return f"image of {self.restaurant}"


class MenuItems(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items', null=True, blank=True)

    def __str__(self):
        return f'{self.restaurant.name}-{self.name}'


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table_no = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    reservation_fee = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.restaurant.name}- table{self.table_no}'


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    menu_items = models.ManyToManyField(MenuItems, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}-{self.date}-{self.time}-{self.table.table_no}-{self.total}'


class ReservationMenuItem(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return (f"{self.reservation.user.username}'s reservation-{self.reservation.table.restaurant.name}"
                f"-{self.reservation.date}-{self.reservation.time}-{self.menu_item.name}-{self.quantity}")
