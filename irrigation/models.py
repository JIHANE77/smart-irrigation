import math
from django.db import models


class Parcelle(models.Model):
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    surface = models.FloatField()  # en hectares
    type_sol = models.CharField(max_length=50)
    reserve_max = models.FloatField()
    reserve_actuelle = models.FloatField()
    seuil_minimum = models.FloatField()
    localisation = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Culture(models.Model):
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    date_plantation = models.DateField()
    stade = models.CharField(max_length=50)
    kc = models.FloatField()

    def __str__(self):
        return self.nom


class Meteo(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    humidite = models.FloatField()
    vent = models.FloatField()
    rayonnement = models.FloatField()
    precipitation = models.FloatField()
    eto = models.FloatField(editable=False, blank=True, default=0)

    def calculer_eto(self):
        T = self.temperature
        RH = self.humidite
        u2 = self.vent
        Rs = self.rayonnement  # MJ/m²/jour

        es = 0.6108 * math.exp((17.27 * T) / (T + 237.3))   # pression de vapeur saturante
        ea = es * (RH / 100)                                  # pression de vapeur réelle
        delta = (4098 * es) / ((T + 237.3) ** 2)              # pente courbe de vapeur
        gamma = 0.067                                          # constante psychrométrique (niveau mer)
        Rn = 0.75 * Rs                                         # estimation rayonnement net

        numerateur = (0.408 * delta * Rn) + (gamma * (900 / (T + 273)) * u2 * (es - ea))
        denominateur = delta + gamma * (1 + 0.34 * u2)

        eto = numerateur / denominateur
        return round(max(eto, 0), 2)

    def save(self, *args, **kwargs):
        self.eto = self.calculer_eto()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.date)


class Irrigation(models.Model):
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    date = models.DateField()
    volume = models.FloatField()
    duree = models.FloatField()
    commentaire = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.parcelle.reserve_actuelle = min(
            self.parcelle.reserve_actuelle + self.volume,
            self.parcelle.reserve_max
        )
        self.parcelle.save()

    def __str__(self):
        return f"{self.parcelle.nom} - {self.date}"


class Recommandation(models.Model):
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    meteo = models.ForeignKey(Meteo, on_delete=models.CASCADE)
    etc = models.FloatField(editable=False, default=0)
    besoin_eau = models.FloatField(editable=False, default=0)
    volume_recommande = models.FloatField(editable=False, default=0)
    irrigation_necessaire = models.BooleanField(editable=False, default=False)
    date_calcul = models.DateField(auto_now_add=True)

    def calculer(self):
        self.etc = round(self.meteo.eto * self.culture.kc, 2)
        self.besoin_eau = round(max(self.etc - self.meteo.precipitation, 0), 2)
        self.irrigation_necessaire = self.parcelle.reserve_actuelle <= self.parcelle.seuil_minimum
        self.volume_recommande = round(
            self.parcelle.surface * self.besoin_eau * 10, 2
        ) if self.irrigation_necessaire else 0

    def save(self, *args, **kwargs):
        self.calculer()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reco {self.parcelle.nom} - {self.date_calcul}"