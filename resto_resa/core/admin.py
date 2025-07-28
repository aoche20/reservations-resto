from django.contrib import admin
from .models import Restaurant
from .models import Table, Reservation,  RestaurantUser


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'domain', 'logo', 'couverture']
    prepopulated_fields = {'slug': ('name',)}




@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'seats', 'restaurant']
    list_filter = ['restaurant']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'restaurant', 'table', 'date', 'time']
    list_filter = ['restaurant', 'date']



@admin.register(RestaurantUser)
class RestaurantUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'restaurant']