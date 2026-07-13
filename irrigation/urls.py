from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parcelles/', views.parcelles, name='parcelles'),
    path('ajouter-parcelle/', views.ajouter_parcelle, name='ajouter_parcelle'),
    path('modifier-parcelle/<int:id>/', views.modifier_parcelle, name='modifier_parcelle'),
    path('supprimer-parcelle/<int:id>/', views.supprimer_parcelle, name='supprimer_parcelle'),

    path('cultures/', views.cultures, name='cultures'),
    path('ajouter-culture/', views.ajouter_culture, name='ajouter_culture'),
    path('modifier-culture/<int:id>/', views.modifier_culture, name='modifier_culture'),
    path('supprimer-culture/<int:id>/', views.supprimer_culture, name='supprimer_culture'),

    path('meteos/', views.meteos, name='meteos'),
    path('ajouter-meteo/', views.ajouter_meteo, name='ajouter_meteo'),
    path('modifier-meteo/<int:id>/', views.modifier_meteo, name='modifier_meteo'),
    path('supprimer-meteo/<int:id>/', views.supprimer_meteo, name='supprimer_meteo'),
]