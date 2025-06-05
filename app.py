from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from bible_chat import initialize_chat, get_bible_response

# Initialisation de Flask
app = Flask(__name__)

# Charger les variables d'environnement
load_dotenv()

# Initialiser le chat
chat = initialize_chat()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/process_audio", methods=["POST"])
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

        # Obtenir une réponse du chat biblique
        response = get_bible_response(text, chat)

        return jsonify({"response": response, "success": True})

    except Exception as e:
        print(f"Erreur serveur: {e}")
        return jsonify({"error": "Erreur serveur interne"}), 500


# Point de terminaison pour vérifier l'état de l'API
@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy", "service": "assistant-biblique"})  # , 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
