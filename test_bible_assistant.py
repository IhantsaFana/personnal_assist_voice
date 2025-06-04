import unittest
from bible_chat import initialize_chat, get_bible_response, ConversationHistory
import os

class TestBibleAssistant(unittest.TestCase):
    def setUp(self):
        self.chat = initialize_chat()
        self.conversation = ConversationHistory()

    def test_conversation_history(self):
        """Test la gestion de l'historique des conversations"""
        # Test l'ajout de messages
        self.conversation.add_message("user", "Test message")
        self.assertEqual(len(self.conversation.messages), 1)
        self.assertEqual(self.conversation.messages[0]["content"], "Test message")

        # Test la limite de l'historique
        for i in range(15):  # Dépasse max_history
            self.conversation.add_message("user", f"Message {i}")
        self.assertLessEqual(len(self.conversation.messages), 10)

        # Test la fenêtre de contexte
        context_window = self.conversation.get_context_window(3)
        self.assertLessEqual(len(context_window), 3)

    def test_chat_initialization(self):
        """Test si le chat est correctement initialisé avec le contexte système"""
        self.assertIsNotNone(self.chat)

    def test_bible_response(self):
        """Test if the assistant provides biblical responses with references"""
        test_questions = [
            "What does the Bible say about love?",
            "Tell me about the creation story",
            "What is the meaning of faith?",
            "Explain the Lord's Prayer",
            "What are the Ten Commandments?",
            "Tell me about Jesus's resurrection"
        ]
        
        for question in test_questions:
            response = get_bible_response(question, self.chat)
            self.assertIsNotNone(response)
            # Check if response contains biblical references (e.g., Book chapter:verse)
            self.assertTrue(any(char.isdigit() and ':' in text 
                              for text in response.split() 
                              for char in text))
            # Check for minimum response length
            self.assertTrue(len(response) > 100, f"Response too short for question: {question}")

    def test_conversation_continuity(self):
        """Test la continuité de la conversation et la pertinence du contexte"""
        # Première question sur un sujet
        response1 = get_bible_response("Que dit la Bible sur l'amour ?", self.chat)
        self.assertIsNotNone(response1)
        self.assertTrue(len(response1) > 0)

        # Question de suivi liée au même sujet
        response2 = get_bible_response("Et qu'en est-il de l'amour fraternel ?", self.chat)
        self.assertIsNotNone(response2)
        self.assertTrue(len(response2) > 0)
        # La réponse devrait faire référence au contexte précédent
        self.assertTrue(any(word in response2.lower() for word in ["aussi", "également", "comme"]))

    def test_error_handling(self):
        """Test la gestion des erreurs avec des entrées invalides"""
        test_cases = [
            ("", "Response should not be empty"),
            (None, "Should handle None input"),
            ("   ", "Should handle whitespace"),
            ("?" * 1000, "Should handle very long input"),
            ("¿§¶°", "Should handle special characters")
        ]
        
        for input_text, message in test_cases:
            response = get_bible_response(input_text, self.chat)
            self.assertTrue(isinstance(response, str), message)
            self.assertNotEqual(response, "", message)
            self.assertTrue(len(response) > 0, message)

    def test_response_quality(self):
        """Test the quality and relevance of responses"""
        question = "What is salvation?"
        response = get_bible_response(question, self.chat)
        
        # Check for key theological terms
        theological_terms = ['salvation', 'grace', 'faith', 'Jesus', 'Christ', 'God']
        self.assertTrue(
            any(term.lower() in response.lower() for term in theological_terms),
            "Response should contain relevant theological terms"
        )
        
        # Check for Bible verse format (e.g., John 3:16)
        self.assertRegex(
            response,
            r'[A-Za-z]+\s*\d+:\d+',
            "Response should contain at least one Bible verse reference"
        )

if __name__ == '__main__':
    unittest.main()
