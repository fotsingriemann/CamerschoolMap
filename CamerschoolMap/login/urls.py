from django.urls import path
from login import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('connexion/', views.connexion, name='connexion'),
    path('conf', views.conf, name='conf'),
    path('baf', views.baf, name='baf'),
    path('register', views.register, name='register'),
    path('error', views.error, name='error-404'),
    path('deconnexion', views.deconnexion, name='deconnexion'),
    path('dashbord', views.dashboard, name='dashbord'),
    path('historique/', views.historique, name='historique'),
    path('setting/', views.setting, name='setting'),  
    path('user/modifier/<int:user_id>/', views.modifier_user, name='modifieruser'),
    path('historique/supprimeruser/', views.supprimer_user, name='supprimeruser'),
    path('erreur_403/', views.erreur_403, name='erreur_403'),
]



    