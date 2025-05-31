import os
import re
import json
import datetime
import requests
import wikipedia
import speech_recognition as sr
import pyttsx3
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

app = Flask(__name__)

# Configurer la langue pour Wikipedia
wikipedia.set_lang("fr")

# Clé API OpenWeatherMap (à configurer dans un fichier .env)
OWM_API_KEY = os.getenv("OWM_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    # Récupérer le texte transcrit depuis la requête
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'Aucun texte reçu'})
    
    # Traiter la requête et générer une réponse
    response = generate_response(text)
    
    return jsonify({
        'text': text,
        'response': response
    })

def generate_response(text):
    """Génère une réponse en fonction du texte de la requête."""
    text = text.lower()
    
    # Salutations
    if any(word in text for word in ['bonjour', 'salut', 'hello', 'coucou']):
        return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    
    # Identité
    if any(phrase in text for phrase in ['qui es-tu', 'qui es tu', 'ton nom', 'présente-toi', 'présente toi']):
        return "Je suis votre assistant vocal personnel. Je peux vous donner l'heure, la météo, répondre à des questions générales ou faire des calculs simples."
    
    # Heure et date
    if any(phrase in text for phrase in ['quelle heure', "l'heure", 'heure actuelle', 'date', 'jour']):
        now = datetime.datetime.now()
        if 'heure' in text:
            return f"Il est actuellement {now.strftime('%H heures %M')}"
        else:
            return f"Nous sommes le {now.strftime('%A %d %B %Y')}"
    
    # Météo
    if 'météo' in text:
        # Extraire le nom de la ville
        match = re.search(r'météo\s+(?:à|a|de|pour)?\s+([\w\s-]+)', text)
        if match:
            city = match.group(1).strip()
            return get_weather(city)
        else:
            return "Pour quelle ville souhaitez-vous connaître la météo ?"
    
    # Calculs
    if any(word in text for word in ['calcul', 'calculer', 'combien font', 'combien font']):
        return calculate(text)
    
    # Recherche Wikipedia
    if any(phrase in text for phrase in ['qui est', 'qu\'est-ce que', 'qu\'est ce que', 'c\'est quoi', 'définis', 'définition']):
        return search_wikipedia(text)
    
    # Réponse par défaut
    return "Je n'ai pas compris votre demande. Pouvez-vous reformuler ?"

def get_weather(city):
    """Récupère les informations météo pour une ville donnée."""
    if not OWM_API_KEY:
        return "La clé API OpenWeatherMap n'est pas configurée. Veuillez créer un fichier .env avec votre clé."
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units=metric&lang=fr"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"À {city}, il fait {temp:.1f}°C avec {description}."
        else:
            return f"Je n'ai pas pu trouver la météo pour {city}. Veuillez vérifier le nom de la ville."
    except Exception as e:
        return f"Une erreur s'est produite lors de la récupération de la météo : {str(e)}"

def calculate(text):
    """Effectue des calculs simples à partir du texte."""
    # Remplacer les mots par des symboles mathématiques
    text = text.replace('plus', '+')
    text = text.replace('moins', '-')
    text = text.replace('fois', '*')
    text = text.replace('multiplié par', '*')
    text = text.replace('divisé par', '/')
    text = text.replace('×', '*')
    text = text.replace('÷', '/')
    
    # Extraire l'expression mathématique
    expression = re.search(r'([\d\s\+\-\*\/\(\)\.]+)', text)
    if expression:
        try:
            # Nettoyer l'expression et évaluer
            expr = expression.group(1).strip()
            result = eval(expr)
            return f"Le résultat est {result}"
        except Exception as e:
            return f"Je n'ai pas pu effectuer ce calcul. Erreur: {str(e)}"
    else:
        return "Je n'ai pas pu identifier l'expression mathématique."

def search_wikipedia(text):
    """Recherche des informations sur Wikipedia."""
    # Extraire le sujet de recherche
    patterns = [
        r'qui est ([\w\s]+)', 
        r'qu\'est[\-\s]ce que ([\w\s]+)', 
        r'c\'est quoi ([\w\s]+)',
        r'définis ([\w\s]+)',
        r'définition de ([\w\s]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            query = match.group(1).strip()
            try:
                # Rechercher sur Wikipedia
                results = wikipedia.search(query)
                if results:
                    # Obtenir un résumé du premier résultat
                    summary = wikipedia.summary(results[0], sentences=2)
                    return summary
                else:
                    return f"Je n'ai pas trouvé d'informations sur {query}."
            except Exception as e:
                return f"Une erreur s'est produite lors de la recherche : {str(e)}"
    
    return "Je n'ai pas pu identifier le sujet de votre recherche."

if __name__ == '__main__':
    app.run(debug=True)