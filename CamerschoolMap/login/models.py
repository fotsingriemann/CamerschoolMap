from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Utilisateur', 'Utilisateur'),
        ('Chef d\'établissement', 'Chef d\'établissement'),
        ('Administrateur', 'Administrateur'),
    ]
    
    PROFESSION_CHOICES = [
        ('Parent', 'Parent'),
        ('Chef d\'établissement', 'Chef d\'établissement'),
        ('Étudiant/Élève', 'Étudiant/Élève'),
    ]
    
    role = models.CharField(max_length=200, choices=ROLE_CHOICES, default='Utilisateur')
    phone = models.CharField(max_length=20, unique=True, null=True)
    
    # Nouveaux champs
    biography = models.TextField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    profession = models.CharField(max_length=50, choices=PROFESSION_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Champ pour savoir qui a créé cet utilisateur
    ajoute_par = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="utilisateurs_ajoutes")
    
    def __str__(self):
        return f"{self.username} - {self.role}"
    
    def save(self, *args, **kwargs):
        """ Associe automatiquement l'utilisateur à un groupe selon son rôle """
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name=self.role)
        self.groups.add(group)

    
    
    def get_role_color(self):
        # Retourne une couleur en fonction du rôle
        if self.role == 'Administrateur':
            return 'success'  # Rouge
        elif self.role == 'Chef d\'établissement':
            return 'primary'  # Jaune
        else:
            return 'primary'  # Vert
    
    