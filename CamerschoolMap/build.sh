#!/usr/bin/env bash

# Stop le script si une commande échoue
set -o errexit

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer le superuser (non interactif)
DJANGO_SUPERUSER_USERNAME=camerschool \
DJANGO_SUPERUSER_EMAIL=camerschoolmap@gmail.com \
DJANGO_SUPERUSER_PASSWORD=camerschool \
python manage.py createsuperuser --noinput || echo "Superuser déjà existant"

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
