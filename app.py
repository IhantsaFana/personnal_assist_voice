from flask import Flask, render_template, request, jsonify, redirect
import speech_recognition as sr
import pyttsx3
import datetime
import re
import requests
import wikipedia
import webbrowser
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration de Wikipedia en français
wikipedia.set_lang("fr")

# Dictionnaire des sites web courants
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "linkedin": "https://www.linkedin.com",
    "github": "https://www.github.com",
    "amazon": "https://www.amazon.com",
    "netflix": "https://www.netflix.com",
}

# Clé API OpenWeatherMap
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

# Fonction pour reconnaître la parole à partir du microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("Écoutez...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            
            print("Reconnaissance en cours...")
            text = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Texte reconnu: {text}")
            return text
    except sr.UnknownValueError:
        print("Impossible de comprendre l'audio")
        return ""
    except sr.RequestError as e:
        print(f"Erreur lors de la requête au service de reconnaissance vocale: {e}")
        return ""
    except Exception as e:
        print(f"Erreur: {e}")
        return ""

# Fonction pour faire parler l'assistant à partir d'un texte
def speak(text):
    try:
        engine = pyttsx3.init()
        # Configuration de la voix (si disponible en français)
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'french' in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
        
        # Réglage de la vitesse de parole (valeur par défaut: 200)
        engine.setProperty('rate', 180)
        
        # Prononciation du texte
        print(f"Assistant: {text}")
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception as e:
        print(f"Erreur lors de la synthèse vocale: {e}")
        return False

# Fonction pour traiter les commandes textuelles
def process_command(command):
    command = command.lower()
    
    # Cas 1: Demande d'heure ou de date
    if "heure" in command or "date" in command:
        now = datetime.datetime.now()
        if "heure" in command:
            response = f"Il est actuellement {now.strftime('%H heures %M minutes')}."
        else:
            response = f"Nous sommes le {now.strftime('%d %B %Y')}."
        return response
    
    # Cas 2: Demande de météo
    weather_match = re.search(r"météo à (\w+)", command)
    if weather_match:
        city = weather_match.group(1)
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=fr"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                weather_desc = data['weather'][0]['description']
                temp = data['main']['temp']
                return f"À {city}, il fait {temp}°C avec {weather_desc}."
            else:
                return f"Je n'ai pas pu obtenir la météo pour {city}. Veuillez vérifier le nom de la ville."
        except Exception as e:
            print(f"Erreur lors de la requête météo: {e}")
            return f"Désolé, je n'ai pas pu obtenir les informations météo pour {city}."
    
    # Cas 3: Salutations ou présentation
    if "bonjour" in command or "salut" in command:
        return "Bonjour ! Je suis votre assistant vocal personnel. Comment puis-je vous aider aujourd'hui ?"
    
    if "qui es-tu" in command or "présente-toi" in command or "ton nom" in command:
        return "Je suis un assistant vocal personnel créé pour vous aider avec diverses tâches comme répondre à vos questions, vous donner l'heure, la météo et bien plus encore."
    
    # Cas 4: Ouverture de sites web
    open_commands = ["ouvre", "va sur", "lance", "démarre"]
    for cmd in open_commands:
        if cmd in command:
            for site, url in WEBSITES.items():
                if site in command:
                    return {"type": "redirect", "url": url, "message": f"J'ouvre {site} pour vous."}
    
    # Cas 5: Recherche Wikipedia pour les questions générales
    try:
        # Nettoyage de la commande pour la recherche
        search_query = command
        # Suppression des mots interrogatifs courants
        for word in ["qu'est-ce que", "qui est", "qu'est ce que", "c'est quoi", "définis", "explique", "parle-moi de"]:
            search_query = search_query.replace(word, "")
        
        search_query = search_query.strip()
        if len(search_query) > 3:  # Éviter les recherches trop courtes
            try:
                # Recherche des pages correspondantes
                search_results = wikipedia.search(search_query, results=1)
                if search_results:
                    # Obtention du résumé de la première page trouvée
                    page = wikipedia.page(search_results[0])
                    summary = wikipedia.summary(search_results[0], sentences=2)
                    return summary
            except wikipedia.exceptions.DisambiguationError as e:
                # En cas d'ambiguïté, prendre la première suggestion
                try:
                    summary = wikipedia.summary(e.options[0], sentences=2)
                    return summary
                except:
                    pass
            except wikipedia.exceptions.PageError:
                pass
            except Exception as e:
                print(f"Erreur lors de la recherche Wikipedia: {e}")
    except Exception as e:
        print(f"Erreur générale lors du traitement de la commande: {e}")
    
    # Réponse par défaut si aucune correspondance n'est trouvée
    return "Je ne suis pas sûr de comprendre votre demande. Pouvez-vous reformuler ou me poser une autre question ?"

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        if request.method == 'POST':
            # Si la requête contient un fichier audio
            if 'audio' in request.files:
                audio_file = request.files['audio']
                # Traitement du fichier audio (à implémenter)
                response_text = "Traitement audio simulé"
                speak(response_text)
                return jsonify({"success": True, "text": response_text})
            # Si la requête contient du texte
            elif request.json and 'text' in request.json:
                text = request.json['text']
                # Traitement intelligent du texte avec process_command
                response = process_command(text)
                
                # Vérifier si la réponse est une redirection
                if isinstance(response, dict) and response.get('type') == 'redirect':
                    speak(response['message'])
                    return jsonify({
                        "success": True,
                        "text": response['message'],
                        "redirect": response['url']
                    })
                
                # Réponse normale
                speak(response)
                return jsonify({"success": True, "text": response})
            else:
                return jsonify({"success": False, "error": "Aucune donnée audio ou texte fournie"})
    except Exception as e:
        print(f"Erreur serveur: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Une erreur est survenue lors du traitement de votre demande"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)