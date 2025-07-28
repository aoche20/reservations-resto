from django.shortcuts import get_object_or_404
from .models import Restaurant

class RestaurantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        slug = request.GET.get('slug')
        if slug:
            request.restaurant = get_object_or_404(Restaurant, slug=slug)
        else:
            request.restaurant = None  # ou un restaurant par défaut si tu préfères
        return self.get_response(request)
