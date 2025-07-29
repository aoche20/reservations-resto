 
from django.shortcuts import render, get_object_or_404
from core.models import Restaurant
from core.forms import ReservationForm

from core.choices import VILLE_CHOICES, SPECIALITE_CHOICES


def accueil(request):
    restaurants = Restaurant.objects.all()[:6]  # Limite à 6
    specialites = Restaurant.objects.values_list('specialite', flat=True).distinct()

    return render(request, 'client/accueil.html', {
        'restaurants': restaurants,
        'specialites': specialites,
    })


def restaurant_detail(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, restaurant=restaurant)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            selected_time = form.cleaned_data['time']
            selected_table = form.cleaned_data['table']

            # Vérifier si la table est déjà réservée à cette date et heure
            if Reservation.objects.filter(date=selected_date, time=selected_time, table=selected_table).exists():
                form.add_error('table', 'Cette table est déjà réservée à cette heure.')
            else:
                reservation = form.save(commit=False)
                reservation.restaurant = restaurant
                reservation.save()
                return redirect('confirmation_reservation')
    else:
        form = ReservationForm(restaurant=restaurant)

    return render(request, 'client/restaurant_detail.html', {
        'restaurant': restaurant,
        'form': form
    })


def liste_restaurants(request):
    restaurants = Restaurant.objects.filter(est_disponible=True)
    ville = request.GET.get('ville')
    specialite = request.GET.get('specialite')
    villes = Restaurant.objects.values_list('ville', flat=True).distinct()

    if ville:
        restaurants = restaurants.filter(ville=ville)
    if specialite:
        restaurants = restaurants.filter(specialite=specialite)

    context = {
        'restaurants': restaurants,
        'ville': ville,
        'specialite': specialite,
        'villes': [v[0] for v in VILLE_CHOICES],
        'specialites': [s[0] for s in SPECIALITE_CHOICES],
    }
    return render(request, 'client/liste_restaurants.html', context)


def confirmation_reservation(request):
    return render(request, 'confirmation_reservation.html')