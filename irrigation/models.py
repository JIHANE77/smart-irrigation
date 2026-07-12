from django.db import models

class Parcelle(models.Model):
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    surface = models.FloatField()
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
    eto = models.FloatField()

    def __str__(self):
        return str(self.date)
class Irrigation(models.Model):
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    date = models.DateField()
    volume = models.FloatField()
    duree = models.FloatField()
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.parcelle.nom} - {self.date}"
