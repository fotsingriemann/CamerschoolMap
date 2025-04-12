from django.urls import path
from CamerSchool import views

urlpatterns  = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('documentation/', views.documentation, name='documentation'),
    path('avis', views.avis, name='avis'),
    path('camer', views.camer, name='camer'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('delete_avis/<int:avis_id>/', views.delete_avis, name='delete_avis'),
]