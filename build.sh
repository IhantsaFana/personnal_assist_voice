#!/bin/bash

# Exit on error
set -o errexit

# Mettre à jour le système et installer les dépendances système
apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    portaudio19-dev \
    python3-pyaudio \
    libespeak1 \
    espeak \
    libespeak-dev \
    gcc \
    g++

# Installer les dépendances Python
python -m pip install --upgrade pip
pip install wheel setuptools
pip install -r requirements.txt

# Configuration d'espeak
ln -s /usr/lib/x86_64-linux-gnu/libespeak.so.1 /usr/lib/x86_64-linux-gnu/libespeak.so

# Création des dossiers nécessaires
mkdir -p static/uploads

# Donner les permissions nécessaires
chmod -R 755 static/uploads

# Vérifier l'installation d'espeak
echo "Vérification de l'installation d'espeak..."
espeak --version

# Vérifier Python et pip
echo "Versions des outils Python :"
python --version
pip --version
