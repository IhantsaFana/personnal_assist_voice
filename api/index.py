from flask import Flask, request, Response
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
root_path = str(Path(__file__).parent.parent.absolute())
sys.path.append(root_path)

from app import app


def handler(request):
    """
    Fonction handler pour Vercel serverless
    Cette fonction adapte les requêtes Vercel pour Flask
    """
    with app.request_context(request):
        try:
            return app.full_dispatch_request()
        except Exception as e:
            app.logger.error(f"Error handling request: {e}")
            return Response(
                response='{"error": "Internal server error"}',
                status=500,
                mimetype="application/json",
            )
