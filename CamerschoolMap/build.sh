#!/usr/bin/env bash

# Stop the script if any command fails
set -o errexit

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin', 'lucas@gmail.com', 'Lucas1lucas')" \
| python manage.py shell

# Collecter les fichiers statiques (dans /staticfiles pour Render)
python manage.py collectstatic --noinput
