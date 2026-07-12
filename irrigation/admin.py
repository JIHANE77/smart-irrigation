from django.contrib import admin
from .models import Parcelle, Culture, Meteo, Irrigation

admin.site.register(Parcelle)
admin.site.register(Culture)
admin.site.register(Meteo)
admin.site.register(Irrigation)
