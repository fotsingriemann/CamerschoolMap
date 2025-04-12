#!/usr/bin/env bash

# Stop the script if any command fails
set -o errexit

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques (dans /staticfiles pour Render)
python manage.py collectstatic --noinput
