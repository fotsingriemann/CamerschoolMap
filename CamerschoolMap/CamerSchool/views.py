from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Avis_views
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from add_school.models import Etablissement
from CamerschoolMap.decorators import login_required_message

# Create your views here.
def index(request):
    etablissements = Etablissement.objects.all().order_by('-date_creation')
    # Pagination (30 avis par page)
    paginator = Paginator(etablissements, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'fontend/index.html', {'etablissements': etablissements, 'page_obj': page_obj})


def blog(request):
    return render(request, 'fontend/autres/blog.html')


@login_required_message
def contact(request):
    if not request.user.is_authenticated:
        messages.info(request, "Vous devez être connecté pour accéder à cette page.")
        return redirect('connexion')
    
    if request.method == 'POST':
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom", "")
        email = request.POST.get("email")
        phone = request.POST.get("phone", "Non fourni")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        
        # Sujet de l'email
        subject_mail = f"Nouveau message de {nom} {prenom} - {subject}"
        
        # Corps de l'email en HTML
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; }}
                .email-container {{ background-color: #f4f4f4; padding: 20px; border-radius: 8px; }}
                h2 {{ color: #333; font-size: 18px; font-weight: bold; }}
                p {{ font-size: 16px; line-height: 1.5; }}
                .highlight {{ font-weight: bold; color: #007BFF; }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <h2>Un nouveau message a été reçu via le formulaire de contact :</h2>
                <p><span class="highlight">Nom:</span> {nom}</p>
                <p><span class="highlight">Prénom:</span> {prenom}</p>
                <p><span class="highlight">Email:</span> {email}</p>
                <p><span class="highlight">Numéro de téléphone:</span> {phone}</p>
                <p><span class="highlight">Sujet:</span> {subject}</p>
                <p><span class="highlight">Message:</span> <br>{message}</p>
            </div>
        </body>
        </html>
        """

        # Envoi de l'email à l'admin (assure-toi que settings.EMAIL_HOST_USER est bien défini)
        send_mail(
            subject_mail,  
            message,  
            settings.EMAIL_HOST_USER,  # Utilise l'email défini dans les settings
            [settings.EMAIL_RECEIVER],  # Change cette ligne pour mettre ton email d'admin
            fail_silently=False,
            html_message=body  # Permet d'envoyer l'email en HTML
        )

        # Redirection vers la page de confirmation
        return redirect(reverse('confirmation') + f'?nom={nom}&email={email}')

    return render(request, 'fontend/autres/contact.html')


def confirmation(request):
    nom = request.GET.get('nom', '')  # Récupère le nom depuis l'URL (si envoyé via GET)
    email = request.GET.get('email', '')  # Récupère l'email

    # On passe les variables au template
    return render(request, 'fontend/autres/confirmation.html', {'nom': nom, 'email': email})

@login_required_message
def avis(request):
    if not request.user.is_authenticated:
        messages.info(request, "Vous devez être connecté pour accéder à cette page.")
        return redirect('connexion')
    # Vérifier si un avis concerne un établissement spécifique
    etab_id = request.GET.get('etablissement_id')
    etab_nom = request.GET.get('etablissement_nom')
    
    if etab_id:
        avis_list = Avis_views.objects.filter(etablissement__id=etab_id).order_by('-date')
    else:
        avis_list = Avis_views.objects.all().order_by('-date')

    # Gestion de la barre de recherche (le champ input devra avoir name="avis-search")
    avis_search = request.GET.get('avis-search')
    if avis_search and avis_search.strip():
        avis_list = avis_list.filter(nom__icontains=avis_search) | avis_list.filter(contenu__icontains=avis_search)

    # Pagination (30 avis par page)
    paginator = Paginator(avis_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        # Récupération des données du formulaire
        type_avis = request.POST.get('typeAvis')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        contenu = request.POST.get('contenu')
        etablissement_id = request.POST.get('etablissement_id')


        try:
            # Création d'un nouvel avis
            Avis_views.objects.create(
                type_avis=type_avis,
                rating=rating,
                nom=nom,
                email=email,
                contenu=contenu,
                etablissement=Etablissement.objects.get(id=etablissement_id) if etablissement_id else None
            )
            messages.success(request, "Avis enregistré avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement de l'avis : {str(e)}")
            

        return redirect('avis')  # redirige pour éviter le re-post du formulaire

    return render(request, 'fontend/autres/avis.html', {'page_obj': page_obj})




# ============== fonction de suppression d'un avis ==========
def delete_avis(request, avis_id):
    avis_obj = get_object_or_404(Avis_views, id=avis_id)
    if request.method == 'POST':
        avis_obj.delete()
        messages.success(request, "Avis supprimé avec succès.")
    else:
        messages.error(request, "Méthode invalide pour la suppression.")
    return redirect('avis')

def documentation(request):
    return render(request, 'backend/autres/doc.html')


def camer(request):
    
    villes = [
        {"name": "Ouest", "image": "fontend/images/bafoussam-ville.jpg.webp"},
        {"name": "Adamawa", "image": "fontend/images/adamawa.jpg"},
        {"name": "Nord-Ouest", "image": "fontend/images/Bamenda.jpg"},
        {"name": "Centre", "image": "fontend/images/Yaounde.jpg"},
        {"name": "Littoral", "image": "fontend/images/douala.jpg"},
        {"name": "Sud-cameroun", "image": "fontend/images/ebolowa.jpg"},
        {"name": "Extrême-Nord", "image": "fontend/images/Maroua-Art.png"},
        {"name": "Nord-cameroun", "image": "fontend/images/GAROUA.jpg"},
        {"name": "sud-ouest", "image": "fontend/images/GAROUA.jpg"},
        {"name": "Est-cameroun", "image": "fontend/images/GAROUA.jpg"},
        
    ]
    
    
     # Pagination
    paginator = Paginator(villes, 2)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)
    return render(request, 'fontend/villes/camer.html', {  'page_obj': page_obj})