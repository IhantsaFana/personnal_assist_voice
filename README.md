# Assistant Vocal Biblique

Un assistant vocal intelligent spécialisé dans l'enseignement de la Bible et la théologie chrétienne. Utilise l'API Gemini pour des réponses contextuelles et pertinentes sur les questions bibliques et spirituelles.

![Statut des Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Version Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)
![Licence](https://img.shields.io/badge/license-MIT-green)

<img src="Messenger_creation_F270C9DC-51A3-48DB-A27F-7AAA0A842BFC.jpeg" alt="Capture d'écran" />

## 🌟 Caractéristiques

- 🎤 Interface vocale en français avec reconnaissance naturelle
- 📖 Réponses basées sur la Bible et la théologie
- 🔊 Synthèse vocale des réponses
- 💬 Conversation naturelle et contextualisée
- ✝️ Citations bibliques pertinentes
- 📜 Interface utilisateur inspirée des parchemins bibliques
- ♿ Design accessible et responsive
- 🌐 Support multilingue (en développement)

### Exemples de Questions
- "Pouvez-vous m'expliquer la parabole du fils prodigue ?"
- "Que dit la Bible sur le pardon ?"
- "Expliquez-moi l'importance de la prière"
- "Quel est le message principal de l'évangile ?"

## 🔧 Prérequis Techniques

- Python 3.8 ou supérieur
- Un navigateur web moderne supportant l'API Web Speech
- `espeak` pour la synthèse vocale sur Linux
- Une clé API Gemini valide

## 📥 Installation

### Linux
```bash
# 1. Installation des dépendances système
sudo apt-get update
sudo apt-get install python3-pip python3-venv espeak

# 2. Configuration de l'environnement Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configuration des variables d'environnement
cp .env.example .env
# Éditer .env et ajouter votre clé API Gemini
```

### Windows
```powershell
# 1. Installation de Python et création de l'environnement virtuel
python -m venv venv
.\venv\Scripts\activate

# 2. Installation des dépendances
pip install -r requirements.txt

# 3. Configuration
copy .env.example .env
# Éditer .env et ajouter votre clé API Gemini
```

## 🚀 Démarrage

1. Activer l'environnement virtuel :
   ```bash
   source venv/bin/activate  # Linux
   .\venv\Scripts\activate   # Windows
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

## 🧪 Tests

Le projet inclut une suite de tests complète :

```bash
# Exécuter tous les tests
python -m pytest

# Tests avec couverture
python -m pytest --cov=. tests/

# Tests spécifiques
python -m pytest test_bible_assistant.py
python -m pytest test_voice_integration.py
```

## 📚 Documentation Technique

### Architecture

```plaintext
assistant-vocal-biblique/
├── api/                # Endpoints API
├── static/            # Assets statiques
│   ├── css/           # Styles
│   └── js/            # Scripts client
├── templates/         # Templates HTML
└── tests/             # Tests unitaires
```

### Stack Technique

- **Backend** : Flask (Python)
- **Frontend** : JavaScript natif, API Web Speech
- **API IA** : Google Gemini
- **Tests** : pytest
- **CI/CD** : GitHub Actions

## 📖 Ressources

- [Documentation API Gemini](https://ai.google.dev/docs)
- [API Web Speech](https://developer.mozilla.org/fr/docs/Web/API/Web_Speech_API)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 🐛 Support et Bugs

Pour signaler un bug ou demander une fonctionnalité :

1. Vérifiez les issues existantes
2. Consultez la documentation
3. Ouvrez une nouvelle issue avec une description détaillée

## 📝 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.
