"""
Module principal de l'Assistant Vocal Biblique.
Gère les routes Flask et l'intégration avec le chat biblique.
"""

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from bible_chat import initialize_chat, get_bible_response
import logging
from typing import Tuple, Dict, Union, Any
from functools import wraps
from http import HTTPStatus

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialisation de Flask
app = Flask(__name__)

# Charger les variables d'environnement
load_dotenv()

# Configuration pour la production
app.config.update(
    DEBUG=False,
    PROPAGATE_EXCEPTIONS=True,
    JSON_SORT_KEYS=False,  # Préserve l'ordre des clés JSON
    MAX_CONTENT_LENGTH=16 * 1024 * 1024  # Limite à 16MB
)

def handle_error(error: Exception) -> Tuple[Dict[str, str], int]:
    """
    Gère les erreurs de manière uniforme.
    
    Args:
        error: L'exception à gérer
        
    Returns:
        Tuple contenant la réponse JSON et le code HTTP
    """
    logger.error(f"Error occurred: {str(error)}", exc_info=True)
    
    if isinstance(error, ValueError):
        return {"error": "Invalid input", "message": str(error)}, HTTPStatus.BAD_REQUEST
    
    return {
        "error": "Internal Server Error",
        "message": str(error)
    }, HTTPStatus.INTERNAL_SERVER_ERROR

def validate_json_input(f):
    """Décorateur pour valider les entrées JSON."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json"
            }), HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            
        try:
            data = request.get_json()
            if not data:
                raise ValueError("Empty JSON body")
        except Exception as e:
            return jsonify({
                "error": "Invalid JSON",
                "message": str(e)
            }), HTTPStatus.BAD_REQUEST
            
        return f(*args, **kwargs)
    return decorated_function

# Initialiser le chat
try:
    chat = initialize_chat()
    logger.info("Chat system initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize chat: {str(e)}")
    chat = None

@app.errorhandler(Exception)
def handle_error_response(error: Exception) -> Tuple[Dict[str, str], int]:
    """Gestionnaire global des erreurs."""
    response, status_code = handle_error(error)
    return jsonify(response), status_code

@app.route("/")
def index() -> str:
    """Route principale servant l'interface utilisateur."""
    return render_template("index.html")

@app.route("/api/process_audio", methods=["POST"])
@validate_json_input
def process_audio() -> Tuple[Dict[str, Any], int]:
    """
    Traite les requêtes audio/texte et retourne une réponse biblique.
    
    Returns:
        Tuple contenant la réponse JSON et le code HTTP
    """
    try:
        data = request.get_json()
        text = data.get("text")

        if not isinstance(text, str):
            raise ValueError("Le champ 'text' doit être une chaîne de caractères")

        if not text.strip():
            raise ValueError("Le champ 'text' ne peut pas être vide")

        if not chat:
            raise RuntimeError("Le système de chat n'est pas initialisé")

        # Obtenir une réponse du chat biblique
        response = get_bible_response(text, chat)
        logger.info(f"Successfully processed request for text: {text[:50]}...")

        return jsonify({
            "response": response,
            "success": True
        }), HTTPStatus.OK

    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        return jsonify({
            "error": "Invalid input",
            "message": str(ve)
        }), HTTPStatus.BAD_REQUEST
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal Server Error",
            "message": "Une erreur est survenue lors du traitement de votre demande"
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route("/api/health")
def health_check() -> Tuple[Dict[str, str], int]:
    """
    Vérifie l'état de santé de l'application.
    
    Returns:
        Tuple contenant la réponse JSON et le code HTTP
    """
    status = "healthy" if chat is not None else "degraded"
    return jsonify({
        "status": status,
        "service": "assistant-biblique",
        "version": os.getenv("APP_VERSION", "1.0.0")
    }), HTTPStatus.OK

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
