from django.db import models
from add_school.models import Etablissement

class Avis_views(models.Model):
    TYPE_CHOICES = [
        ('site', 'Site en général'),
        ('etablissement', 'Établissement spécifique'),
    ]
    
    type_avis = models.CharField(max_length=20, choices=TYPE_CHOICES)
    rating = models.PositiveSmallIntegerField(default=1)  # Note de 1 à 5
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    etablissement = models.ForeignKey(Etablissement, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.nom} - {self.type_avis}"

