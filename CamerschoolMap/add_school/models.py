from django.db import models
from django.contrib.auth import get_user_model

class Etablissement(models.Model):
    TYPE_CHOICES = [
        ('public', 'Public'),
        ('privé', 'Privé'),
    ]

    CATEGORIE_CHOICES = [
        ('primaire', 'Primaire'),
        ('secondaire', 'Secondaire'),
    ]

    nom = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    departement = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    categorie = models.CharField(max_length=10, choices=CATEGORIE_CHOICES)
    description = models.TextField(blank=True, null=True)
    adresse = models.CharField(max_length=255)
    contact = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    image_profil = models.ImageField(upload_to='etablissements/profil/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
     # Ajoute le champ pour savoir qui a ajouté l'établissement
    ajoute_par = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name="etablissements_ajoutes")

    def __str__(self):
        return self.nom

class PhotoEtablissement(models.Model):
    etablissement = models.ForeignKey(Etablissement, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='etablissements/photos/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo de {self.etablissement.nom}"
