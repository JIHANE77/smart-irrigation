from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Parcelle, Culture, Meteo, Irrigation
from .forms import ParcelleForm, CultureForm, MeteoForm, IrrigationForm
from reportlab.pdfgen import canvas
import requests


# ---------- DASHBOARD ----------

def home(request):
    context = {
        'parcelles': Parcelle.objects.count(),
        'cultures': Culture.objects.count(),
        'meteo': Meteo.objects.count(),
        'irrigations': Irrigation.objects.count(),
    }
    return render(request, 'irrigation/home.html', context)


# ---------- PARCELLES ----------

def parcelles(request):
    return render(request, 'irrigation/parcelles.html', {'parcelles': Parcelle.objects.all()})


def ajouter_parcelle(request):
    if request.method == 'POST':
        form = ParcelleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parcelles')
    else:
        form = ParcelleForm()
    return render(request, 'irrigation/ajouter_parcelle.html', {'form': form})


def modifier_parcelle(request, id):
    parcelle = get_object_or_404(Parcelle, id=id)
    if request.method == 'POST':
        form = ParcelleForm(request.POST, instance=parcelle)
        if form.is_valid():
            form.save()
            return redirect('parcelles')
    else:
        form = ParcelleForm(instance=parcelle)
    return render(request, 'irrigation/modifier_parcelle.html', {'form': form})


def supprimer_parcelle(request, id):
    get_object_or_404(Parcelle, id=id).delete()
    return redirect('parcelles')


# ---------- CULTURES ----------

def cultures(request):
    return render(request, 'irrigation/cultures.html', {'cultures': Culture.objects.select_related('parcelle').all()})


def ajouter_culture(request):
    if request.method == 'POST':
        form = CultureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cultures')
    else:
        form = CultureForm()
    return render(request, 'irrigation/ajouter_culture.html', {'form': form})


def modifier_culture(request, id):
    culture = get_object_or_404(Culture, id=id)
    if request.method == 'POST':
        form = CultureForm(request.POST, instance=culture)
        if form.is_valid():
            form.save()
            return redirect('cultures')
    else:
        form = CultureForm(instance=culture)
    return render(request, 'irrigation/modifier_culture.html', {'form': form})


def supprimer_culture(request, id):
    get_object_or_404(Culture, id=id).delete()
    return redirect('cultures')


# ---------- METEO ----------

def meteos(request):
    return render(request, 'irrigation/meteos.html', {'meteos': Meteo.objects.all()})


def ajouter_meteo(request):
    if request.method == 'POST':
        form = MeteoForm(request.POST)
        if form.is_valid():
            form.save()  # eto calculé automatiquement dans Meteo.save()
            return redirect('meteos')
    else:
        form = MeteoForm()
    return render(request, 'irrigation/ajouter_meteo.html', {'form': form})


def modifier_meteo(request, id):
    meteo = get_object_or_404(Meteo, id=id)
    if request.method == 'POST':
        form = MeteoForm(request.POST, instance=meteo)
        if form.is_valid():
            form.save()
            return redirect('meteos')
    else:
        form = MeteoForm(instance=meteo)
    return render(request, 'irrigation/modifier_meteo.html', {'form': form})


def supprimer_meteo(request, id):
    get_object_or_404(Meteo, id=id).delete()
    return redirect('meteos')


def meteo_auto(request):
    """Récupère la météo actuelle via Open-Meteo et l'enregistre en base."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=34.26&longitude=-6.58"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,"
        "precipitation,shortwave_radiation"
    )
    response = requests.get(url)
    data = response.json()
    current = data["current"]

    meteo = Meteo(
        date=current["time"][:10],
        temperature=current["temperature_2m"],
        humidite=current["relative_humidity_2m"],
        vent=current["wind_speed_10m"],
        rayonnement=current.get("shortwave_radiation", 0) * 0.0864,  # W/m2 -> MJ/m2/jour
        precipitation=current["precipitation"],
    )
    meteo.save()  # eto calculé automatiquement

    return render(request, "irrigation/meteo.html", {"meteo": meteo})


# ---------- IRRIGATIONS ----------

def irrigations(request):
    return render(request, 'irrigation/irrigations.html', {'irrigations': Irrigation.objects.select_related('parcelle').all()})


def ajouter_irrigation(request):
    if request.method == 'POST':
        form = IrrigationForm(request.POST)
        if form.is_valid():
            form.save()  # réserve mise à jour automatiquement dans Irrigation.save()
            return redirect('irrigations')
    else:
        form = IrrigationForm()
    return render(request, 'irrigation/ajouter_irrigation.html', {'form': form})


def modifier_irrigation(request, id):
    irrigation = get_object_or_404(Irrigation, id=id)
    if request.method == 'POST':
        form = IrrigationForm(request.POST, instance=irrigation)
        if form.is_valid():
            form.save()
            return redirect('irrigations')
    else:
        form = IrrigationForm(instance=irrigation)
    return render(request, 'irrigation/modifier_irrigation.html', {'form': form})


def supprimer_irrigation(request, id):
    get_object_or_404(Irrigation, id=id).delete()
    return redirect('irrigations')


# ---------- RECOMMANDATIONS (logique centralisée) ----------

def calculer_recommandation(culture, meteo):
    """Calcule ETc, besoin, volume et décision pour une culture donnée."""
    parcelle = culture.parcelle

    etc = meteo.eto * culture.kc
    besoin = max(0, etc - meteo.precipitation)
    volume = parcelle.surface * besoin * 10

    reserve_basse = parcelle.reserve_actuelle <= parcelle.seuil_minimum

    if not reserve_basse:
        decision = "🟢 Pas d'irrigation nécessaire (réserve suffisante)"
        volume = 0
    elif besoin == 0:
        decision = "🟢 Pas d'irrigation nécessaire"
        volume = 0
    elif besoin < 3:
        decision = "🟡 Irrigation légère recommandée"
    elif besoin < 6:
        decision = "🟠 Irrigation recommandée"
    else:
        decision = "🔴 Irrigation urgente"

    return {
        'parcelle': parcelle.nom,
        'eto': meteo.eto,
        'kc': culture.kc,
        'etc': round(etc, 2),
        'besoin': round(besoin, 2),
        'reserve_actuelle': parcelle.reserve_actuelle,
        'seuil_minimum': parcelle.seuil_minimum,
        'volume': round(volume, 2),
        'decision': decision,
    }


def recommandations(request):
    cultures = Culture.objects.select_related('parcelle').all()
    meteo = Meteo.objects.last()

    resultats = []
    if meteo and cultures.exists():
        resultats = [calculer_recommandation(c, meteo) for c in cultures]

    return render(request, 'irrigation/recommandations.html', {'resultats': resultats})


def exporter_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_irrigation.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Rapport Smart Irrigation")
    p.drawString(100, 770, "Projet de gestion intelligente de l'irrigation")

    y = 730
    cultures = Culture.objects.select_related('parcelle').all()
    meteo = Meteo.objects.last()

    if meteo:
        for culture in cultures:
            r = calculer_recommandation(culture, meteo)
            texte = (
                f"{r['parcelle']} | ET0={r['eto']} | Kc={r['kc']} | "
                f"Besoin={r['besoin']} | Volume={r['volume']} | {r['decision']}"
            )
            p.drawString(50, y, texte)
            y -= 25

    p.save()
    return response