from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from add_school import views

urlpatterns = [
    
    
    path('school/', views.ajouter_etablissement, name='school'),
    path('erreur_403/', views.erreur_403, name='erreur_403'),
    path('historique_ecole/', views.historique_ecole, name='historique_ecole'),
    path('detail/', views.detail, name='detail'),
    path('detail_users/', views.detail_users, name='detail_users'),
    path('sucess_page/', views.succes_page, name='succes_page'),
    path('echecs/', views.echecs, name='echecs'),
    path('etablissement/<int:etablissement_id>/', views.detail_etablissement, name='detail_etablissement'),
    path("supprimer-etablissement/<int:etablissement_id>/", views.supprimer_etablissement, name="supprimer_etablissement"),
    path("modifier_etablissement/<int:etablissement_id>/", views.modifier_etablissement, name="modifier_etablissement"),
    path('autocomplete-etablissements/', views.autocomplete_etablissements, name='autocomplete-etablissements'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
