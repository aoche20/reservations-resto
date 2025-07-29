
from .models import Reservation
from .models import Table
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Restaurant
from django.utils.text import slugify
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'table', 'date', 'time']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'w-full border px-3 py-2 rounded'}),
            'table': forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border px-3 py-2 rounded'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full border px-3 py-2 rounded'}),
        }
        
    def __init__(self, *args, **kwargs):
        restaurant = kwargs.pop('restaurant', None)
        super().__init__(*args, **kwargs)
        if restaurant:
            self.fields['table'].queryset = Table.objects.filter(restaurant=restaurant)





class UserRestaurantSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    restaurant_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "restaurant_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        restaurant_name = self.cleaned_data['restaurant_name']

        if commit:
            user.save()

            # Générer slug et domaine automatiquement
            slug = slugify(restaurant_name)
            domain = f"{slug}.example.com"

            # Éviter les doublons de slug
            original_slug = slug
            counter = 1
            while Restaurant.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                domain = f"{slug}.example.com"
                counter += 1

            restaurant = Restaurant.objects.create(
                name=restaurant_name,
                slug=slug,
                domain=domain
            )

            from .models import RestaurantUser
            RestaurantUser.objects.create(user=user, restaurant=restaurant)

        return user


from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full border px-3 py-2 rounded',
            'accept': 'image/*'
        })
    )
    
    couverture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full border px-3 py-2 rounded',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Restaurant
        fields = ['logo', 'couverture']




class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'seats']
        labels = {
            'number': 'Numéro de table',
            'seats': 'Nombre de places',
        }
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'w-full border px-3 py-2 rounded'}),
            'seats': forms.NumberInput(attrs={'class': 'w-full border px-3 py-2 rounded'}),
        }


 