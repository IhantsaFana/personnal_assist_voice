#!/bin/bash

# Exit on error
set -o errexit

# Installer les bibliothèques système nécessaires à PyAudio et espeak
apt-get update && apt-get install -y \
    portaudio19-dev \
    libespeak-dev \
    espeak \
    gcc \
    g++ \
    python3-dev

# Installer les dépendances Python
pip install --upgrade pip
pip install -r requirements.txt

# Création des dossiers nécessaires
mkdir -p static/uploads
