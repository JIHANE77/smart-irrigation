from django.shortcuts import render, redirect, get_object_or_404
from .models import Parcelle, Culture, Meteo, Irrigation
from .forms import ParcelleForm
def home(request):
    context = {
        'parcelles': Parcelle.objects.count(),
        'cultures': Culture.objects.count(),
        'meteo': Meteo.objects.count(),
        'irrigations': Irrigation.objects.count(),
    }

    return render(request, 'irrigation/home.html', context)


def parcelles(request):
    liste_parcelles = Parcelle.objects.all()

    return render(
        request,
        'irrigation/parcelles.html',
        {'parcelles': liste_parcelles}
    )
from .forms import ParcelleForm
from django.shortcuts import redirect

def ajouter_parcelle(request):
    if request.method == 'POST':
        form = ParcelleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('parcelles')

    else:
        form = ParcelleForm()

    return render(
        request,
        'irrigation/ajouter_parcelle.html',
        {'form': form}
    )
def modifier_parcelle(request, id):
    parcelle = Parcelle.objects.get(id=id)

    if request.method == 'POST':
        form = ParcelleForm(request.POST, instance=parcelle)

        if form.is_valid():
            form.save()
            return redirect('parcelles')

    else:
        form = ParcelleForm(instance=parcelle)

    return render(
        request,
        'irrigation/modifier_parcelle.html',
        {'form': form}
    )
def supprimer_parcelle(request, id):
    parcelle = get_object_or_404(Parcelle, id=id)

    parcelle.delete()

    return redirect('parcelles')