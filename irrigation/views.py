from django.shortcuts import render, redirect, get_object_or_404
from .models import Parcelle, Culture, Meteo, Irrigation
from .forms import ParcelleForm ,CultureForm,  MeteoForm , IrrigationForm
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

def meteos(request):
    liste_meteos = Meteo.objects.all()

    return render(
        request,
        'irrigation/meteos.html',
        {'meteos': liste_meteos}
    )


def ajouter_meteo(request):
    if request.method == 'POST':
        form = MeteoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('meteos')

    else:
        form = MeteoForm()

    return render(
        request,
        'irrigation/ajouter_meteo.html',
        {'form': form}
    )


def modifier_meteo(request, id):
    meteo = get_object_or_404(Meteo, id=id)

    if request.method == 'POST':
        form = MeteoForm(request.POST, instance=meteo)

        if form.is_valid():
            form.save()
            return redirect('meteos')

    else:
        form = MeteoForm(instance=meteo)

    return render(
        request,
        'irrigation/modifier_meteo.html',
        {'form': form}
    )


def supprimer_meteo(request, id):
    meteo = get_object_or_404(Meteo, id=id)

    meteo.delete()

    return redirect('meteos')
def irrigations(request):
    liste_irrigations = Irrigation.objects.all()

    return render(
        request,
        'irrigation/irrigations.html',
        {'irrigations': liste_irrigations}
    )


def ajouter_irrigation(request):
    if request.method == 'POST':
        form = IrrigationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('irrigations')

    else:
        form = IrrigationForm()

    return render(
        request,
        'irrigation/ajouter_irrigation.html',
        {'form': form}
    )


def modifier_irrigation(request, id):
    irrigation = get_object_or_404(Irrigation, id=id)

    if request.method == 'POST':
        form = IrrigationForm(request.POST, instance=irrigation)

        if form.is_valid():
            form.save()
            return redirect('irrigations')

    else:
        form = IrrigationForm(instance=irrigation)

    return render(
        request,
        'irrigation/modifier_irrigation.html',
        {'form': form}
    )


def supprimer_irrigation(request, id):
    irrigation = get_object_or_404(Irrigation, id=id)

    irrigation.delete()

    return redirect('irrigations')