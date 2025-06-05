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

# Required for Vercel
app.debug = False


def create_app():
    return app


def handler(event, context):
    """
    Fonction handler pour Vercel serverless
    Cette fonction adapte les requêtes Vercel pour Flask
    """
    if not event:
        return {"statusCode": 500, "body": "No event data received"}

    try:
        # Create a Flask request context
        with app.test_request_context(
            path=event.get("path", "/"),
            method=event.get("httpMethod", "GET"),
            headers=event.get("headers", {}),
            data=event.get("body", ""),
            environ_base={"SERVER_NAME": "vercel"},
        ):
            try:
                response = app.full_dispatch_request()
                return {
                    "statusCode": response.status_code,
                    "body": response.get_data(as_text=True),
                    "headers": dict(response.headers),
                }
            except Exception as e:
                app.logger.error(f"Error processing request: {str(e)}")
                return {
                    "statusCode": 500,
                    "body": str(e),
                    "headers": {"Content-Type": "application/json"},
                }
    except Exception as e:
        app.logger.error(f"Error setting up request context: {str(e)}")
        return {
            "statusCode": 500,
            "body": str(e),
            "headers": {"Content-Type": "application/json"},
        }
