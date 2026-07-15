from django.core.management.base import BaseCommand
from irrigation.models import Meteo
import requests
from datetime import date


class Command(BaseCommand):
    help = "Récupère la météo du jour via Open-Meteo et l'enregistre automatiquement"

    def handle(self, *args, **options):
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=34.26&longitude=-6.58"
            "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,"
            "precipitation,shortwave_radiation"
        )
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()["current"]
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erreur API météo : {e}"))
            return

        meteo = Meteo.objects.create(
            date=date.today(),
            temperature=data["temperature_2m"],
            humidite=data["relative_humidity_2m"],
            vent=data["wind_speed_10m"],
            rayonnement=data.get("shortwave_radiation", 0) * 0.0864,
            precipitation=data["precipitation"],
        )
        self.stdout.write(self.style.SUCCESS(
            f"✅ Météo enregistrée pour {meteo.date} — ETo={meteo.eto} mm/jour"
        ))