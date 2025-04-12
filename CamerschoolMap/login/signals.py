from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import CustomUser

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    if sender.name == 'users':  # Assurez-vous que ça ne s'exécute que pour votre app "users"
        roles_permissions = {
            'Administrateur': ['add_user', 'change_user', 'delete_user', 'view_user'],
            'Chef d\'établissement': ['view_user'],
            'Utilisateur': []
        }

        for role, perms in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role)
            for perm in perms:
                try:
                    permission = Permission.objects.get(codename=perm, content_type=ContentType.objects.get_for_model(CustomUser))
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    pass
