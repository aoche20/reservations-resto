from django.db import models
from django.contrib.auth.models import User
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    domain = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    couverture = models.ImageField(upload_to='couvertures/', blank=True, null=True)


    def __str__(self):
        return self.name

class Table(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='tables')
    number = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.number} ({self.seats} places) - {self.restaurant.name}"

class Reservation(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey('Table', on_delete=models.CASCADE, related_name='reservations')
    customer_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.date} à {self.time} - {self.table}"



class RestaurantUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurantuser')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return f"{self.user.username} — {self.restaurant.name}"

    
