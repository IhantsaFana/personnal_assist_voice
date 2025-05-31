# Assistant Vocal Personnel

Un assistant vocal web capable de comprendre et d'exécuter des commandes vocales en français.

## Fonctionnalités

- Reconnaissance vocale en français
- Synthèse vocale pour les réponses
- Commandes disponibles :
  - Météo (ex: "Quelle est la météo à Paris ?")
  - Définitions Wikipedia (ex: "C'est quoi l'intelligence artificielle ?")
  - Date et heure (ex: "Quel jour sommes-nous ?", "Quelle heure est-il ?")
  - Ouverture de sites web (ex: "Ouvre YouTube")

## Prérequis

- Python 3.7 ou supérieur
- Un navigateur web moderne supportant l'API Web Speech
- Une connexion Internet
- Windows (pour pyttsx3)

## Installation

1. Clonez le dépôt :
```bash
git clone [url-du-repo]
cd personnal_assist_voice
```

2. Créez un environnement virtuel et activez-le :
```bash
python -m venv venv
.\venv\Scripts\Activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

La clé API OpenWeatherMap est déjà configurée dans le fichier `app.py`.

## Utilisation

1. Démarrez le serveur Flask :
```bash
python app.py
```

2. Ouvrez votre navigateur et accédez à :
```
http://localhost:5000
```

3. Cliquez sur le bouton "Parler" et énoncez votre commande.

## Dépannage

### Problèmes courants :

1. Si la reconnaissance vocale ne fonctionne pas :
   - Vérifiez que votre navigateur est à jour
   - Assurez-vous d'avoir autorisé l'accès au microphone

2. Si la synthèse vocale ne fonctionne pas :
   - Vérifiez que pyttsx3 est correctement installé
   - Sur Windows, vérifiez que les voix SAPI5 sont installées

3. Si les requêtes API échouent :
   - Vérifiez votre connexion Internet
   - Vérifiez que la clé API OpenWeatherMap est valide

## Technologies utilisées

- Flask (Backend)
- Web Speech API (Reconnaissance vocale)
- pyttsx3 (Synthèse vocale)
- OpenWeatherMap API (Météo)
- Wikipedia API (Recherche d'informations)
