from django.shortcuts import render, redirect, get_object_or_404
from .models import Parcelle, Culture, Meteo, Irrigation
from .forms import ParcelleForm ,CultureForm,  MeteoForm , IrrigationForm
from django.http import HttpResponse
from reportlab.pdfgen import canvas
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
def recommandations(request):
    parcelles = Parcelle.objects.all()
    cultures = Culture.objects.all()
    meteos = Meteo.objects.all()

    resultats = []

    if cultures.exists() and meteos.exists():
        meteo = meteos.last()

        for culture in cultures:
            etc = meteo.eto * culture.kc

            besoin = etc - meteo.precipitation
            if besoin < 0:
                besoin = 0

            volume = culture.parcelle.surface * besoin * 10

            decision = "✅ Pas d'irrigation nécessaire"
            if besoin > 0:
                decision = "⚠️ Irrigation recommandée"

            resultats.append({
                'parcelle': culture.parcelle.nom,
                'eto': meteo.eto,
                'kc': culture.kc,
                'etc': round(etc, 2),
                'besoin': round(besoin, 2),
                'volume': round(volume, 2),
                'decision': decision,
            })

    return render(
        request,
        'irrigation/recommandations.html',
        {'resultats': resultats}
    )
def exporter_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_irrigation.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, "Rapport Smart Irrigation")
    p.drawString(100, 770, "Projet de gestion intelligente de l'irrigation")

    y = 730

    cultures = Culture.objects.all()
    meteo = Meteo.objects.last()

    if meteo:
        for culture in cultures:
            etc = meteo.eto * culture.kc
            besoin = max(0, etc - meteo.precipitation)
            volume = culture.parcelle.surface * besoin * 10

            texte = (
                f"{culture.parcelle.nom} | "
                f"ET0={meteo.eto} | "
                f"Kc={culture.kc} | "
                f"Besoin={round(besoin,2)} | "
                f"Volume={round(volume,2)}"
            )

            p.drawString(50, y, texte)
            y -= 25

    p.save()
    return response