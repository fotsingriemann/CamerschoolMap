from django.contrib import admin
from .models import Avis_views

class AvisViewAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'type_avis', 'date')  
    search_fields = ('nom', 'email', 'subject')  
    list_filter = ('type_avis', 'date')  
    ordering = ('-date',)  

admin.site.register(Avis_views, AvisViewAdmin) 

