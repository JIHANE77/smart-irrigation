from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parcelles/', views.parcelles, name='parcelles'),
    path('ajouter-parcelle/', views.ajouter_parcelle, name='ajouter_parcelle'),
    path('modifier-parcelle/<int:id>/', views.modifier_parcelle, name='modifier_parcelle'),
    path('supprimer-parcelle/<int:id>/', views.supprimer_parcelle, name='supprimer_parcelle'),
]