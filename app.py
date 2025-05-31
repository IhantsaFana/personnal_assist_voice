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
    weather_match = re.search(r"météo (?:à|de|pour|dans|en) ([a-zA-ZÀ-ÿ\s-]+)", command)
    if weather_match:
        city = weather_match.group(1).strip()
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
    open_commands = ["ouvre", "va sur", "lance", "démarre", "navigue sur", "accède à"]
    for cmd in open_commands:
        if cmd in command:
            for site, url in WEBSITES.items():
                if site in command.lower():
                    return {"type": "redirect", "url": url, "message": f"J'ouvre {site} pour vous."}
            # Si aucun site connu n'est trouvé, mais qu'il y a une commande d'ouverture
            unknown_site_match = re.search(f"{cmd}\\s+([a-zA-Z0-9-]+)", command)
            if unknown_site_match:
                site = unknown_site_match.group(1).lower()
                return {"type": "redirect", "url": f"https://www.{site}.com", "message": f"J'ouvre {site} pour vous."}
    # Cas 5: Recherche Wikipedia pour les questions générales
    try:
    # Patterns de questions dynamiques
        question_patterns = [
            (r"(qu[i']|quel|quels?|quelles?) (?:sont|est).*?(?:droits?|lois?|règles?|législation)", "droit"),
            (r"(qu[i']|quel|quels?|quelles?) (?:sont|est).*?(?:éthique|moral|déontologie)", "éthique"),
            (r"(comment|quelles?) (?:sont|est).*?(?:règles?|normes?|standards?)", "normes"),
            (r"(qu[i']|quel|quels?|quelles?) (?:sont|est).*?(?:obligations?|devoirs?)", "obligations légales"),
            (r"(qu[i']|quel|quels?|quelles?) (?:est|sont).*?(?:président|ministre|gouvernement)", "politique"),
            (r"(?:parle|dis).*?(?:moi|nous).*?(de|sur|à propos)", "information générale"),
            (r"(?:c'est|qu'est[- ]ce que|qu'est ce qu).*?((?:[a-zA-Z]+))", "définition"),
            (r"(?:explique|définis).*?((?:[a-zA-Z]+))", "explication")
        ]
        
        # Questions spécifiques pré-formatées pour certains sujets importants
        specific_queries = {
            "président": {
                "pattern": r"(qui|quel) est le président (de la )?république( française)?( actuel)?",
                "query": "Président de la République française actuel"
            },
            "premier ministre": {
                "pattern": r"(qui|quel) est le premier ministre( français)?( actuel)?",
                "query": "Premier ministre français actuel"
            },
            "gouvernement": {
                "pattern": r"(qui|quels?) (est|sont) les? membres? du gouvernement( français)?( actuel)?",
                "query": "Gouvernement français actuel"
            }
        }

        # Vérifier les questions spécifiques d'abord
        for key, info in specific_queries.items():
            if re.search(info["pattern"], command, re.IGNORECASE):
                search_query = info["query"]
                break
        else:        # Si aucune question spécifique ne correspond, analyser le type de question
            search_query = command
        question_type = None
        extracted_subject = None

        # Détecter le type de question et extraire le sujet
        for pattern, q_type in question_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                question_type = q_type
                # Tenter d'extraire le sujet principal
                if len(match.groups()) > 0:
                    extracted_subject = match.group(1)
                break

        # Liste dynamique de mots à supprimer basée sur le type de question
        words_to_remove = {
            "mots_interrogatifs": [
                "qu'est-ce que", "qui est", "qu'est ce que", "c'est quoi",
                "définis", "explique", "parle-moi de", "dis-moi qui est",
                "peux-tu me dire", "je veux savoir", "peux-tu m'expliquer",
                "qu'est ce qu'", "c'est", "qu'est", "que", "quoi", "qui"
            ],
            "articles": ["le", "la", "les", "du", "de", "des", "un", "une"],
            "verbes_communs": ["être", "avoir", "faire", "dire", "aller", "voir", "savoir", "pouvoir"],
            "prepositions": ["à", "dans", "par", "pour", "en", "vers", "avec", "sans", "sous", "sur"]
        }
          # Nettoyage intelligent basé sur le type de question
        for category, words in words_to_remove.items():
            if question_type != "définition" or category != "articles":  # Garder les articles pour les définitions
                for word in words:
                    search_query = re.sub(r'\b' + re.escape(word) + r'\b', '', search_query, flags=re.IGNORECASE)
        
        # Enrichissement de la recherche selon le type de question
        if question_type:
            if question_type == "droit":
                search_query += " législation droit loi"
            elif question_type == "éthique":
                search_query += " éthique morale principes"
            elif question_type == "politique":
                search_query += " politique actuel"
            elif question_type == "définition":
                search_query = f"définition {extracted_subject if extracted_subject else search_query}"
        search_query = search_query.strip()
        if len(search_query) > 2:  # Réduire la limite minimale pour les recherches courtes mais pertinentes
            try:
                # Recherche avec mots-clés spécifiques pour les frameworks/technologies
                if re.search(r"(framework|technologie|langage|programmation|développement|logiciel)", command, re.IGNORECASE):
                    search_query = search_query + " (informatique)"
                elif re.search(r"(outil|application|app|software)", command, re.IGNORECASE):
                    search_query = search_query + " (logiciel)"
                  # Recherche des pages correspondantes avec un contexte enrichi
                search_results = wikipedia.search(search_query, results=5)  # Augmenté à 5 résultats
                if search_results:
                    best_summary = None
                    max_relevance = 0
                    
                    for result in search_results:
                        try:
                            page = wikipedia.page(result)
                            summary = wikipedia.summary(result, sentences=4)  # Augmenté à 4 phrases
                            
                            # Calcul de la pertinence
                            relevance = 0
                            if question_type:
                                if question_type in page.content.lower():
                                    relevance += 2
                                if extracted_subject and extracted_subject.lower() in page.content.lower():
                                    relevance += 3
                            
                            # Vérifier la longueur et la qualité du résumé
                            if len(summary) > 50 and summary.count('.') >= 2:
                                relevance += 1
                            
                            if relevance > max_relevance:
                                max_relevance = relevance
                                best_summary = summary
                            
                            if max_relevance >= 4:  # Seuil de pertinence élevé atteint
                                break
                        except Exception as e:
                            print(f"Erreur lors de la récupération de la page Wikipedia: {e}")
                            continue
                                
                    if best_summary:
                        return best_summary
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