from django.shortcuts import render
from .models import Parcelle, Culture, Meteo, Irrigation

def home(request):
    context = {
        'parcelles': Parcelle.objects.count(),
        'cultures': Culture.objects.count(),
        'meteo': Meteo.objects.count(),
        'irrigations': Irrigation.objects.count(),
    }

    return render(request, 'irrigation/home.html', context)