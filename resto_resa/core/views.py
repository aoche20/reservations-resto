
from django.shortcuts import render, redirect
from .forms import ReservationForm
from .models import Table
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import UserRestaurantSignUpForm

from .models import RestaurantUser
from .forms import RestaurantForm

from django.contrib.auth import login


def accueil(request):
    restaurant = request.restaurant
    return render(request, 'core/accueil.html', {'restaurant': restaurant})




def accueil(request):
    restaurant = request.restaurant

    if not restaurant:
        return render(request, 'core/no_restaurant.html')

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.restaurant = restaurant
            reservation.save()
            return redirect(f"/?slug={restaurant.slug}&success=1")
    else:
        form = ReservationForm()

    # Filtrer les tables du restaurant actif
    form.fields['table'].queryset = Table.objects.filter(restaurant=restaurant)

    return render(request, 'core/accueil.html', {
        'restaurant': restaurant,
        'form': form,
        'success': request.GET.get('success'),
    })


@login_required
def reservations(request):
    restaurant = request.restaurant
    if not restaurant:
        return render(request, 'core/no_restaurant.html')

    reservations = restaurant.reservations.order_by('-date', '-time')

    return render(request, 'core/reservations.html', {
        'restaurant': restaurant,
        'reservations': reservations,
    })

from django.http import HttpResponseForbidden

@login_required
def dashboard(request):
    try:
        restaurant_user = request.user.restaurantuser
    except RestaurantUser.DoesNotExist:
        return HttpResponseForbidden("Vous n'êtes pas associé à un restaurant.")

    restaurant = restaurant_user.restaurant
    form = RestaurantForm(request.POST , request.FILES , instance=restaurant)
    tables = restaurant.tables.all()
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')  

    reservations = restaurant.reservations.order_by('-date', '-time')
    add_table_form = TableForm()

    return render(request, 'core/dashboard.html', {
        'restaurant': restaurant,
        'reservations': reservations,
        'tables': tables,
        'add_table_form': add_table_form,
        'form': form,
    })



def signup(request):
    if request.method == 'POST':
        form = UserRestaurantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # ou page d’accueil
    else:
        form = UserRestaurantSignUpForm()

    return render(request, 'core/signup.html', {'form': form})




@login_required
def supprimer_compte(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('accueil')  # ou page d'accueil publique
    return render(request, 'core/supprimer_compte.html')


from .forms import TableForm
from django.shortcuts import get_object_or_404

@login_required
def ajouter_table(request):
    restaurant = request.user.restaurantuser.restaurant
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save(commit=False)
            table.restaurant = restaurant
            table.save()
    return redirect('dashboard')


@login_required
def modifier_table(request, pk):
    restaurant = request.user.restaurantuser.restaurant
    table = get_object_or_404(Table, pk=pk, restaurant=restaurant)

    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('dashboard')



@login_required
def supprimer_table(request, pk):
    restaurant = request.user.restaurantuser.restaurant
    table = get_object_or_404(Table, pk=pk, restaurant=restaurant)

    if request.method == 'POST':
        table.delete()
        return redirect('dashboard')

    
