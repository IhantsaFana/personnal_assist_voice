import pytest
import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_gemini_response():
    return "[TEST] Voici une réponse de test qui inclut une référence biblique (Jean 3:16) et des termes théologiques comme la grâce, la foi et la rédemption."
