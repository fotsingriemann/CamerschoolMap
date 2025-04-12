from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import re
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from add_school.views import Etablissement


def is_admin(user):
    return user.groups.filter(name='Administrateur').exists()

def is_chef(user):
    return user.groups.filter(name="Chef d'établissement").exists()


def erreur_403(request):
    return render(request, 'backend/autres/error-404.html', status=403)



User = get_user_model()
# Fonction de D'INSCRIPTION
def inscription(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        errors = []
        
        # Vérification des formats
        if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password):
            errors.append("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")
        if not re.match(r'^\+237\d{9}$', phone):
            errors.append("Le numéro de téléphone doit être au format +237XXXXXXXXX.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append("Format d'email invalide.")
        
        # Vérification unicité de l'email
        if User.objects.filter(email=email).exists():
            errors.append("L'email existe déjà.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'fontend/autres/inscription.html')

        # Création de l'utilisateur (NE PAS HACHER LE MOT DE PASSE MANUELLEMENT)
        user = User.objects.create_user(username=nom, email=email, password=password)
        
        # Génération de l'URL de connexion
        login_url = request.build_absolute_uri(reverse('connexion'))
        
        # Envoi de l'email de confirmation
        subject = "Inscription réussie sur CamerschoolMap"
        message = (
            f"Bonjour {user.username},\n\n"
            "Votre inscription sur CamerschoolMap a été réalisée avec succès.\n\n"
            f"Vous pouvez vous connecter en utilisant vos identifiants en cliquant sur le lien suivant : {login_url}\n\n"
            "Merci et bienvenue sur CamerschoolMap !"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        messages.success(request, "Inscription reussite! Vous pouvez maintenant vous connecter a votre compte😊")
        return redirect('connexion')
    
    return render(request, 'fontend/autres/inscription.html')















# Fonction de connexion
@csrf_exempt
def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return redirect('connexion')

        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                messages.success(request, f"Connexion réussie. Bienvenue, {auth_user.username} !")
                
                next_url = request.GET.get('next') or ('dashbord' if auth_user.role != 'Utilisateur' else 'detail_users')
                return redirect(next_url)

        messages.error(request, "Email ou mot de passe incorrect.")

    # Afficher les messages dans le template
    return render(request, 'fontend/autres/connexion.html', {
        'messages': messages.get_messages(request)
    })


















# FOCTION DE DECONNEXION 
@login_required(login_url='connexion')
def deconnexion(request):
    if request.method == "POST":
        logout(request)
        request.session.flush()
        print("Déconnexion effectuée et session supprimée.")
        return JsonResponse({"message": "Vous avez été déconnecté avec succès."})
    
    return JsonResponse({"error": "Méthode non autorisée."}, status=400)









@login_required(login_url='connexion')
def historique(request):
    users = User.objects.all().order_by('-id')
    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'backend/autres/historique.html', {'users': users})













# FONCTION POUR SUPPRIMER UN UTLISATEUR 
@login_required(login_url='connexion')
def supprimer_user(request):
    if request.method == 'POST':
        try:
            # Récupérer les données JSON de la requête
            data = json.loads(request.body)
            user_id = data.get('user_id')  # Récupérer l'ID de l'utilisateur

            # Vérifier si l'utilisateur existe
            utilisateur = User.objects.get(id=user_id)
            utilisateur.delete()
            return JsonResponse({'status': 'success', 'message': 'Utilisateur supprimé avec succès.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "L'utilisateur n'existe pas."})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Requête invalide.'})







# FONCTION POUR MODIFIER UN UTILISATEUR
@login_required(login_url='connexion')
def modifier_user(request, user_id):
    User = get_user_model()  # Récupérer le modèle utilisateur (CustomUser)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "L'utilisateur demandé n'existe pas.")
        return redirect('historique')  # Redirige vers la liste des utilisateurs

    if request.method == 'POST':
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        role = request.POST.get('role', '').strip()
        password = request.POST.get('password', '').strip()
        
        errors = []

        # Vérifications des champs obligatoires
        if not nom or not email or not phone or not role:
            errors.append("Tous les champs doivent être remplis.")

        # Vérification des formats
        if not re.match(r'^[a-zA-Z0-9_]+$', nom):
            errors.append("Le nom ne doit contenir que des lettres, chiffres et underscore.")
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append("Format d'email invalide.")
        if not re.match(r'^\+237\d{9}$', phone):
            errors.append("Le numéro de téléphone doit être au format +237XXXXXXXXX.")

        # Vérification unicité de l'email (si changé)
        if email != user.email and User.objects.filter(email=email).exists():
            errors.append("L'email existe déjà.")

        # Vérification unicité du numéro de téléphone (si changé)
        if phone != user.phone and User.objects.filter(phone=phone).exists():
            errors.append("Le numéro de téléphone est déjà utilisé.")

        # Vérification du mot de passe si fourni
        if password:
            if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password):
                errors.append("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")

        # Gestion des erreurs
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'backend/autres/modifieruser.html', {'user': user})

        # Mise à jour des données
        user.username = nom
        user.email = email
        user.phone = phone
        user.role = role
        if password:
            user.password = make_password(password)  # Hachage du mot de passe

        user.save()
        
        messages.success(request, "Utilisateur modifié avec succès !")
        return redirect('historique')

    return render(request, 'backend/autres/modifieruser.html', {'user': user})

    
    
# FONCTION QUI PERMET A L'AMINISTRATEUR D'AJOUTER DES NEMBRES
@login_required(login_url='connexion')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        role = request.POST.get('role', 'Utilisateur') 
        
        errors = []

        # Vérifier si les valeurs ne sont pas vides
        if not username or not phone or not password or not email:
            errors.append("Tous les champs doivent être remplis.")

        # Vérifications de la validité des champs (uniquement si les valeurs ne sont pas None)
        if username and not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append("Le nom d'utilisateur ne doit contenir que des lettres, chiffres et underscore.")
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors.append("Format d'email invalide.")
        if phone and not re.match(r'^\+237\d{9}$', phone):
            errors.append("Le numéro de téléphone doit être au format +237XXXXXXXXX.")
        if password and not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', password):
            errors.append("Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre.")

        # Vérification unicité des données
        if CustomUser.objects.filter(email=email).exists():
            errors.append("L'email existe déjà.")
        if CustomUser.objects.filter(phone=phone).exists():
            errors.append("Le numéro de téléphone est déjà utilisé.")

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'backend/autres/register.html')

        # Création de l'utilisateur
        user = CustomUser.objects.create(
            username=username,
            email=email,
            role=role,
            phone=phone,
            password=make_password(password)
        )

        # Génération de l'URL de connexion
        login_url = request.build_absolute_uri(reverse('connexion'))
        
        # Envoi de l'email de confirmation avec identifiants
        subject = "Vous avez été inscrit sur CamerschoolMap"
        message = (
            f"Bonjour {username},\n\n"
            "Vous avez été ajouté avec succès à CamerschoolMap.\n\n"
            f"Voici vos identifiants :\n"
            f"Nom d'utilisateur : {username}\n"
            f"Email : {email}\n"
            f"Mot de passe : {password}\n\n"
            f"Pour vous connecter, veuillez cliquer sur le lien suivant : {login_url}\n\n"
            "Merci et bienvenue sur CamerschoolMap !"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        messages.success(request, "Utilisateur ajouté avec succès !")
        return redirect('historique')

    return render(request, 'backend/autres/register.html')

# FONCTION POUR AFFICHER LES UTILISATEURS ET GERER LA PAGINATION

@login_required(login_url='connexion')
def dashboard(request):
    user = request.user
    
    if user.role == "Administrateur":
        total_utilisateurs = CustomUser.objects.count()
        total_chefs = CustomUser.objects.filter(role="Chef d'établissement").count()
        total_etablissements = Etablissement.objects.count()
        users_list = CustomUser.objects.exclude(id=user.id).order_by('-id')
    else:
        total_utilisateurs = user.utilisateurs_ajoutes.count()
        total_chefs = 0  
        total_etablissements = user.etablissements_ajoutes.count()
        users_list = user.utilisateurs_ajoutes.all()
    
    # Pagination : 8 utilisateurs par page
    paginator = Paginator(users_list, 8)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    
    context = {
        'total_utilisateurs': total_utilisateurs,
        'total_chefs': total_chefs,
        'users_page': users_page,  # Utilisation de 'users_page' au lieu de 'etablissements'
        'total_etablissements': total_etablissements
    }
    
    return render(request, 'backend/dashbord.html', context)



@login_required(login_url='connexion')
def setting(request):
    user = request.user
    
    if request.method == 'POST':
        # Récupération des données
        nom = request.POST.get('fullName')
        phone = request.POST.get('phoneNumber')
        bio = request.POST.get('bio')
        facebook = request.POST.get('facebook')
        twitter = request.POST.get('twitter')
        linkedin = request.POST.get('linkedin')
        instagram = request.POST.get('instagram')
        profession = request.POST.get('profession')
        new_password = request.POST.get('password')
        
        errors = []
        
        # Validation du téléphone
        if not re.match(r'^\+237\d{9}$', phone):
            errors.append("Le numéro de téléphone doit être au format +237XXXXXXXXX.")
        
        if CustomUser.objects.filter(phone=phone).exclude(id=user.id).exists():
            errors.append("Ce numéro est déjà utilisé.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('setting')
        
        # Mise à jour des champs
        user.username = nom
        user.phone = phone
        user.biography = bio
        user.facebook_link = facebook
        user.twitter_link = twitter
        user.linkedin_link = linkedin
        user.instagram_link = instagram
        user.profession = profession
        
        # Gestion du mot de passe
        if new_password:
            if not re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', new_password):
                messages.error(request, "Le mot de passe doit contenir 8 caractères, une majuscule et un chiffre.")
                return redirect('setting')
            user.set_password(new_password)
        
        # Gestion de l'image
        if 'uploadPhoto' in request.FILES:
            user.image = request.FILES['uploadPhoto']
        
        user.save()
        messages.success(request, "Paramètres mis à jour avec succès!")
        return redirect('setting')

        return redirect('settings')  # Rediriger vers la même page après mise à jour
    return render(request, 'backend/autres/settings.html', {'user': user})










def modifieruser(request):
    return render(request, 'backend/autres/modifieruser.html')





def conf(request):
    return render(request, 'fontend/autres/conf.html')








def error(request):
    return render(request, 'backend/autres/error-404.html')

def confirmation(request):
    return render(request, 'fontend/autres/confirmation.html')



def baf(request):
    return render(request, 'fontend/villes/baf.html')




@login_required(login_url='connexion')
def confirmation_deconnexion(request):
    return render(request, 'fontend/autres/confirmation_deconnexion.html')


