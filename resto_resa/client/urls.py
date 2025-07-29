from django.urls import path
from .views import accueil, restaurant_detail, liste_restaurants, confirmation_reservation


urlpatterns = [
    path('', accueil, name='accueil'),
    path('restaurant/<slug:slug>/', restaurant_detail, name='restaurant_detail'),
    path('restaurants/',liste_restaurants, name='liste_restaurants'),
    path('confirmation/', confirmation_reservation, name='confirmation_reservation'),



  
]
