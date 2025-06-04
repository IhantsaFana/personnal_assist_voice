# Assistant Vocal Biblique

Un assistant vocal intelligent spécialisé dans l'enseignement de la Bible et la théologie chrétienne. Utilise l'API Gemini pour des réponses contextuelles et pertinentes sur les questions bibliques et spirituelles.

## Fonctionnalités

- Interface vocale en français
- Réponses basées sur la Bible et la théologie
- Synthèse vocale des réponses
- Conversation naturelle et contextualisée
- Citations bibliques pertinentes
- Interface utilisateur inspirée des parchemins bibliques
- Exemples de questions :
  - "Pouvez-vous m'expliquer la parabole du fils prodigue ?"
  - "Que dit la Bible sur le pardon ?"
  - "Expliquez-moi l'importance de la prière"
  - "Quel est le message principal de l'évangile ?"

## Prérequis

- Python 3.8 ou supérieur
- Un navigateur web moderne supportant l'API Web Speech
- `espeak` pour la synthèse vocale sur Linux
- Une clé API Gemini valide

## Installation sur Linux

1. Installation des dépendances système :

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv espeak
```

2. Configuration de l'environnement Python :

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configuration des variables d'environnement :

```bash
cp .env.example .env
# Éditer .env et ajouter votre clé API Gemini
```

## Démarrage

1. Activer l'environnement virtuel :

```bash
source venv/bin/activate
```

2. Lancer l'application :

```bash
python app.py
```

3. Ouvrir dans le navigateur : http://localhost:5000

## Utilisation de l'API

### Exemple d'intégration Python

```python
from bible_chat import initialize_chat, get_bible_response

# Initialiser le chat
chat = initialize_chat()

# Poser une question
response = get_bible_response("Que dit la Bible sur l'amour ?", chat)
print(response)
```

### Exemple d'appel API REST

```bash
curl -X POST http://localhost:5000/process_audio \
  -H "Content-Type: application/json" \
  -d '{"text":"Que dit la Bible sur la foi ?"}'
```

## Tests

Pour exécuter les tests unitaires :

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Exécuter les tests
venv/bin/python -m unittest test_bible_assistant.py
venv/bin/python -m unittest test_voice_integration.py
```

## Personnalisation

### Thèmes visuels

Le fichier `static/css/styles.css` contient des variables CSS personnalisables :

```css
:root {
  --copilot-primary: #8b4513; /* Couleur principale */
  --copilot-accent: #daa520; /* Accent doré */
  --copilot-purple: #4b0082; /* Accent violet */
}
```

### Contexte biblique

Le contexte du système peut être modifié dans `bible_chat.py` pour ajuster le style et la profondeur des réponses.

## Ressources

- [Documentation de l'API Gemini](https://ai.google.dev/docs)
- [API Web Speech](https://developer.mozilla.org/fr/docs/Web/API/Web_Speech_API)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Support

Pour toute question ou problème :

1. Vérifiez les problèmes connus dans l'onglet Issues
2. Consultez la documentation ci-dessus
3. Ouvrez une nouvelle issue avec une description détaillée
