from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('parcelles/', views.parcelles, name='parcelles'),
    path('ajouter-parcelle/', views.ajouter_parcelle, name='ajouter_parcelle'),
    path('modifier-parcelle/<int:id>/', views.modifier_parcelle, name='modifier_parcelle'),
    path('supprimer-parcelle/<int:id>/', views.supprimer_parcelle, name='supprimer_parcelle'),
    path('meteo/', views.meteo_auto, name='meteo'),


    path('cultures/', views.cultures, name='cultures'),
    path('ajouter-culture/', views.ajouter_culture, name='ajouter_culture'),
    path('modifier-culture/<int:id>/', views.modifier_culture, name='modifier_culture'),
    path('supprimer-culture/<int:id>/', views.supprimer_culture, name='supprimer_culture'),

    path('meteos/', views.meteos, name='meteos'),
    path('ajouter-meteo/', views.ajouter_meteo, name='ajouter_meteo'),
    path('modifier-meteo/<int:id>/', views.modifier_meteo, name='modifier_meteo'),
    path('supprimer-meteo/<int:id>/', views.supprimer_meteo, name='supprimer_meteo'),

    path('irrigations/', views.irrigations, name='irrigations'),
    path('ajouter-irrigation/', views.ajouter_irrigation, name='ajouter_irrigation'),
    path('modifier-irrigation/<int:id>/', views.modifier_irrigation, name='modifier_irrigation'),
    path('supprimer-irrigation/<int:id>/', views.supprimer_irrigation, name='supprimer_irrigation'),

    path('recommandations/', views.recommandations, name='recommandations'),

    path('export-pdf/', views.exporter_pdf, name='export_pdf'),

    path('cron/fetch-meteo/', views.cron_fetch_meteo, name='cron_fetch_meteo'),
]