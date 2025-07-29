from django.urls import path
from .views import reservations, dashboard, signup, supprimer_compte, ajouter_table, modifier_table, supprimer_table
from django.contrib.auth import views as auth_views

urlpatterns = [
  
    path('reservations/', reservations, name='reservations'),
    path('dashboard/', dashboard, name='dashboard'),
    path('signup/', signup, name='signup'),
    
    path('supprimer-compte/', supprimer_compte, name='supprimer_compte'),

    path('table/ajouter/', ajouter_table, name='ajouter_table'),
    path('table/<int:pk>/modifier/', modifier_table, name='modifier_table'),
    path('table/<int:pk>/supprimer/', supprimer_table, name='supprimer_table'),


    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
