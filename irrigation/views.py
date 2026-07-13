from django.shortcuts import render, redirect, get_object_or_404
from .models import Parcelle, Culture, Meteo, Irrigation
from .forms import ParcelleForm ,CultureForm
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

def cultures(request):
    liste_cultures = Culture.objects.all()

    return render(
        request,
        'irrigation/cultures.html',
        {'cultures': liste_cultures}
    ) 
def ajouter_culture(request):
    if request.method == 'POST':
        form = CultureForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('cultures')

    else:
        form = CultureForm()

    return render(
        request,
        'irrigation/ajouter_culture.html',
        {'form': form}
    )
def cultures(request):
    liste_cultures = Culture.objects.all()

    return render(
        request,
        'irrigation/cultures.html',
        {'cultures': liste_cultures}
    )


def ajouter_culture(request):
    if request.method == 'POST':
        form = CultureForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('cultures')

    else:
        form = CultureForm()

    return render(
        request,
        'irrigation/ajouter_culture.html',
        {'form': form}
    )


def modifier_culture(request, id):
    culture = get_object_or_404(Culture, id=id)

    if request.method == 'POST':
        form = CultureForm(request.POST, instance=culture)

        if form.is_valid():
            form.save()
            return redirect('cultures')

    else:
        form = CultureForm(instance=culture)

    return render(
        request,
        'irrigation/modifier_culture.html',
        {'form': form}
    )


def supprimer_culture(request, id):
    culture = get_object_or_404(Culture, id=id)

    culture.delete()

    return redirect('cultures')