import unittest
import os
from app import app
import json

class TestVoiceIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_loads(self):
        """Test if the homepage loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Assistant Biblique', response.data)

    def test_audio_processing_endpoint(self):
        """Test the audio processing endpoint with text input"""
        test_cases = [
            {
                "text": "What is the meaning of life according to the Bible?",
                "expected_status": 200
            },
            {
                "text": "Tell me about Jesus",
                "expected_status": 200
            },
            {
                "text": "",  # Empty input
                "expected_status": 400
            }
        ]

        for case in test_cases:
            response = self.app.post('/process_audio',
                                   data=json.dumps({"text": case["text"]}),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, case["expected_status"])
            
            if case["expected_status"] == 200:
                data = json.loads(response.data)
                self.assertIn('response', data)
                self.assertTrue(len(data['response']) > 0)

    def test_invalid_requests(self):
        """Test handling of invalid requests"""
        # Test missing text field
        response = self.app.post('/process_audio',
                               data=json.dumps({}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test invalid JSON
        response = self.app.post('/process_audio',
                               data='invalid json',
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Test wrong content type
        response = self.app.post('/process_audio',
                               data='{"text": "test"}',
                               content_type='text/plain')
        self.assertEqual(response.status_code, 415)

if __name__ == '__main__':
    unittest.main()
