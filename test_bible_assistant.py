import unittest
from bible_chat import initialize_chat, get_bible_response, ConversationHistory, GeminiAPI
from unittest.mock import patch, MagicMock
import os
import warnings

class TestBibleAssistant(unittest.TestCase):
    """Tests unitaires pour l'assistant biblique."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        warnings.filterwarnings('ignore', category=ResourceWarning)
        self.chat = initialize_chat()
        self.conversation = ConversationHistory()

    def test_conversation_history_management(self):
        """Test complet de la gestion de l'historique des conversations."""
        # Test l'ajout de messages
        self.conversation.add_message("user", "Test message")
        self.assertEqual(len(self.conversation.messages), 1)
        self.assertEqual(self.conversation.messages[0]["content"], "Test message")

        # Test le filtrage des messages vides
        self.conversation.add_message("user", "   ")
        self.assertEqual(len(self.conversation.messages), 1)

        # Test la limite de l'historique
        for i in range(15):  # Dépasse max_history
            self.conversation.add_message("user", f"Message {i}")
        self.assertLessEqual(len(self.conversation.messages), 10)

        # Test la fenêtre de contexte
        context_window = self.conversation.get_context_window(3)
        self.assertLessEqual(len(context_window), 3)
        
        # Test clear
        self.conversation.clear()
        self.assertEqual(len(self.conversation.messages), 0)

    @patch('bible_chat.GeminiAPI')
    def test_chat_initialization_error(self, mock_api):
        """Test la gestion des erreurs lors de l'initialisation."""
        mock_api.side_effect = Exception("API Error")
        with self.assertRaises(Exception):
            GeminiAPI()

    def test_response_format_validation(self):
        """Test si les réponses respectent le format attendu."""
        test_questions = [
            "What does the Bible say about love?",
            "Tell me about the creation story",
            "What is the meaning of faith?",
        ]
        
        for question in test_questions:
            response = get_bible_response(question, self.chat)
            
            # Vérifie la présence de références bibliques
            self.assertTrue(
                any(char.isdigit() and ':' in text 
                    for text in response.split() 
                    for char in text),
                f"No biblical reference found in response to: {question}"
            )
            
            # Vérifie la longueur minimale
            self.assertTrue(
                len(response) > 100,
                f"Response too short for question: {question}"
            )
            
            # Vérifie la présence de contenu théologique
            theological_terms = ['God', 'Jesus', 'Christ', 'faith', 'love', 'Bible']
            self.assertTrue(
                any(term.lower() in response.lower() for term in theological_terms),
                f"No theological terms found in response to: {question}"
            )

    def test_error_handling_comprehensive(self):
        """Test approfondi de la gestion des erreurs."""
        test_cases = [
            ("", "Should handle empty input"),
            (None, "Should handle None input"),
            ("   ", "Should handle whitespace"),
            ("?" * 1000, "Should handle very long input"),
            ("¿§¶°", "Should handle special characters"),
            (123, "Should handle non-string input"),  # Nouveau cas
            ([], "Should handle list input"),  # Nouveau cas
        ]
        
        for input_text, message in test_cases:
            try:
                response = get_bible_response(input_text, self.chat)
                self.assertTrue(isinstance(response, str), message)
                self.assertTrue(len(response) > 0, message)
                self.assertTrue("error" in response.lower() or "sorry" in response.lower(), 
                              "Error responses should be apologetic")
            except Exception as e:
                self.fail(f"Failed to handle {input_text}: {str(e)}")

    def test_conversation_flow(self):
        """Test la cohérence du flux de conversation."""
        # Test d'une série de questions liées
        questions = [
            "Who is Jesus?",
            "What did he teach about love?",
            "Can you elaborate on that last point?",
        ]
        
        previous_response = None
        for question in questions:
            current_response = get_bible_response(question, self.chat)
            
            if previous_response:
                # Vérifie la cohérence contextuelle
                self.assertTrue(
                    any(word in current_response.lower() 
                        for word in ["also", "additionally", "furthermore", "moreover"]),
                    "Response should show awareness of conversation context"
                )
            
            previous_response = current_response

if __name__ == '__main__':
    unittest.main()
