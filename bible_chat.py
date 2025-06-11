import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional, Any
import json
from unittest.mock import MagicMock
from logging import getLogger

# Configure logging
logger = getLogger(__name__)

load_dotenv()

class GeminiAPI:
    """
    Interface avec l'API Gemini pour la génération de réponses bibliques.
    
    Cette classe gère la communication avec l'API Gemini, y compris l'initialisation,
    la gestion des erreurs et le mode mock pour les tests.
    """
    
    def __init__(self):
        """Initialise l'API Gemini avec la clé d'API depuis les variables d'environnement."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            logger.error("API key not found")
            raise ValueError("API key not found. Please set GEMINI_API_KEY in .env file")
        
        try:
            genai.configure(api_key=self.api_key)
            self._model = None
            self.is_mock = False
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {str(e)}")
            raise RuntimeError(f"Failed to configure Gemini API: {str(e)}")

    @property
    def model(self) -> Any:
        """
        Initialise et retourne le modèle Gemini.
        
        Returns:
            Any: Instance du modèle Gemini ou un mock pour les tests
            
        Raises:
            RuntimeError: Si l'initialisation du modèle échoue
        """
        if self._model is None:
            try:
                self._model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                logger.warning(f"Using mock model due to initialization error: {str(e)}")
                self._model = self._create_mock_model()
                self.is_mock = True
        return self._model

    def _create_mock_model(self) -> MagicMock:
        """Crée un mock du modèle pour les tests."""
        mock = MagicMock()
        mock.start_chat.return_value = MagicMock()
        mock.start_chat.return_value.send_message.return_value = MagicMock(
            text="[TEST] Voici une réponse biblique de test. (Jean 3:16)"
        )
        return mock

# Instance globale de l'API
gemini_api = GeminiAPI()

class ConversationHistory:
    """
    Gère l'historique des conversations avec une fenêtre glissante.
    
    Attributes:
        max_history (int): Nombre maximum de messages à conserver
        messages (List[Dict[str, str]]): Liste des messages de l'historique
    """
    
    def __init__(self, max_history: int = 10):
        """
        Initialise l'historique des conversations.
        
        Args:
            max_history: Nombre maximum de messages à conserver
        """
        self.messages: List[Dict[str, str]] = []
        self.max_history = max_history

    def add_message(self, role: str, content: str) -> None:
        """
        Ajoute un message à l'historique.
        
        Args:
            role: Rôle de l'émetteur ('user', 'system', 'assistant')
            content: Contenu du message
            
        Note:
            Les messages les plus anciens sont supprimés si max_history est dépassé
        """
        if not content.strip():
            logger.warning("Attempted to add empty message")
            return
            
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

    def get_context_window(self, window_size: int = 5) -> List[Dict[str, str]]:
        """
        Obtient la fenêtre de contexte des derniers messages.
        
        Args:
            window_size: Nombre de messages à inclure dans la fenêtre
            
        Returns:
            Liste des derniers messages dans la limite de window_size
        """
        return self.messages[-window_size:] if self.messages else []

    def clear(self) -> None:
        """Efface l'historique des conversations."""
        self.messages = []
        logger.info("Conversation history cleared")

# Contexte initial pour orienter le modèle vers la théologie
SYSTEM_CONTEXT = """Tu es un expert en théologie chrétienne et en études bibliques, avec une profonde connaissance de la Bible, de son histoire et de son interprétation.

Ta mission principale est de :
1. Répondre aux questions sur la Bible et la foi chrétienne avec sagesse et bienveillance
2. Citer systématiquement des passages pertinents de la Bible (avec les références précises)
3. Expliquer les concepts théologiques de manière simple et accessible
4. Aider à appliquer les enseignements bibliques dans la vie quotidienne
5. Garder un ton pastoral et encourageant

Pour chaque réponse :
- Commence par répondre directement à la question
- Cite au moins un passage biblique pertinent avec sa référence
- Explique le contexte historique si nécessaire
- Termine par une application pratique ou une réflexion spirituelle

Utilise un langage respectueux et accessible, tout en restant fidèle aux enseignements bibliques.
Évite les controverses théologiques et concentre-toi sur les vérités fondamentales de la foi chrétienne."""

# Instance globale de l'historique des conversations
conversation_history = ConversationHistory()

def initialize_chat():
    """Initialise une nouvelle conversation avec le contexte système"""
    global conversation_history
    conversation_history.clear()
    try:
        chat = gemini_api.model.start_chat(history=[])
        conversation_history.add_message("system", SYSTEM_CONTEXT)
        return chat
    except Exception as e:
        print(f"Erreur lors de l'initialisation du chat: {str(e)}")
        return None

def get_bible_response(user_input: str, chat: Optional[any] = None) -> str:
    """
    Obtient une réponse biblique en utilisant l'historique des conversations
    pour maintenir le contexte
    """
    if not chat:
        chat = initialize_chat()
        if not chat:
            return "Désolé, je ne peux pas initialiser la conversation pour le moment."
    
    try:
        # Ajouter l'entrée de l'utilisateur à l'historique
        conversation_history.add_message("user", user_input)
        
        # Construire le prompt avec le contexte récent
        context_window = conversation_history.get_context_window()
        context_prompt = "\n".join([
            f"{'Assistant' if msg['role'] == 'system' else msg['role'].capitalize()}: {msg['content']}"
            for msg in context_window[:-1]  # Exclure le dernier message utilisateur
        ])
        
        # Générer la réponse avec le contexte
        response = chat.send_message(
            f"{context_prompt}\n\nUser: {user_input}",
            generation_config={"temperature": 0.7}
        )
        
        # Sauvegarder la réponse dans l'historique
        response_text = response.text if not gemini_api.is_mock else response.text
        conversation_history.add_message("assistant", response_text)
        
        return response_text
        
    except Exception as e:
        error_msg = str(e)
        print(f"Erreur lors de la génération de la réponse: {error_msg}")
        if "404" in error_msg:
            return "Le service n'est pas disponible pour le moment. Veuillez réessayer plus tard."
        return "Je suis désolé, j'ai rencontré une erreur. Pouvez-vous reformuler votre question ?"
