# Generated by Django 4.2.17 on 2025-03-17 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('add_school', '0003_etablissement_photoetablissement_delete_add_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='etablissement',
            name='ajoute_par',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='etablissements_ajoutes', to=settings.AUTH_USER_MODEL),
        ),
    ]
