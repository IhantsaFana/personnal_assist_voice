from flask import Flask, request, Response, send_from_directory
import sys
import os
from pathlib import Path

# Add parent directory to PYTHONPATH
root_path = str(Path(__file__).parent.parent.absolute())
sys.path.append(root_path)

# Import the Flask app
from app import app

# Configure static and template folders
app.static_folder = os.path.join(root_path, "static")
app.template_folder = os.path.join(root_path, "templates")


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
