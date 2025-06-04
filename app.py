from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
from bible_chat import initialize_chat, get_bible_response

app = Flask(__name__)

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialiser le chat
chat = initialize_chat()


@app.route("/health")
def health_check():
    """Route de vérification de santé pour Render.com"""
    return jsonify({"status": "healthy", "service": "assistant-biblique"}), 200


@app.route("/")
def index():
    return render_template("index.html")


# Fonction pour faire parler l'assistant à partir d'un texte
def speak(text):
    try:
        engine = pyttsx3.init("espeak")  # Utiliser espeak sur Linux
        # Configuration de la voix en français
        engine.setProperty("voice", "fr")
        engine.setProperty("rate", 150)  # Vitesse un peu plus lente pour plus de clarté

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
    if not isinstance(command, str):
        return "Je suis désolé, je n'ai pas compris votre question. Pouvez-vous la reformuler ?"

    command = command.strip()
    if not command:
        return "Je n'ai pas reçu de question. Pouvez-vous répéter s'il vous plaît ?"

    try:
        # Obtenir une réponse du chat biblique
        response = get_bible_response(command, chat)
        return response
    except Exception as e:
        print(f"Erreur lors du traitement de la commande: {e}")
        return "Je suis désolé, j'ai rencontré une erreur. Pouvez-vous reformuler votre question ?"


@app.route("/process_audio", methods=["POST"])
def process_audio():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type doit être application/json"}), 415

        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Le champ 'text' est requis"}), 400

        text = data["text"]

        if not isinstance(text, str):
            return (
                jsonify(
                    {"error": "Le champ 'text' doit être une chaîne de caractères"}
                ),
                400,
            )

        # Traiter la commande
        response = process_command(text)
        # Synthèse vocale de la réponse
        speak_success = speak(response)

        return jsonify({"response": response, "voice_output": speak_success})

    except Exception as e:
        print(f"Erreur serveur: {e}")
        return jsonify({"error": "Erreur serveur interne"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
