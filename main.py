from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# URL of the Notes application
NOTES_APP_URL = os.environ.get('NOTES_APP_URL', 'http://localhost:8080')

@app.route('/')
def hello_gateway():
    return 'Hello, World! This is the API Gateway.'

@app.route('/gateway/health', methods=['GET'])
def gateway_health_check():
    """Health check endpoint for the API Gateway."""
    return jsonify({"status": "healthy", "service": "api-gateway"}), 200

@app.route('/gateway/notes-app-health', methods=['GET'])
def notes_app_health_check():
    """Fetches the health status of the Notes application."""
    try:
        response = requests.get(f"{NOTES_APP_URL}/health")
        response.raise_for_status() # Raise an exception for HTTP errors
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"status": "unhealthy", "service": "notes-app", "error": "Connection to notes app failed"}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "unhealthy", "service": "notes-app", "error": str(e)}), 500

@app.route('/gateway/notes', methods=['POST'])
def add_note_via_gateway():
    """Forwards a request to add a note to the Notes application."""
    try:
        data = request.get_json()
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{NOTES_APP_URL}/notes", json=data, headers=headers)
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), response.status_code if 'response' in locals() else 500

@app.route('/gateway/notes', methods=['GET'])
def get_notes_via_gateway():
    """Forwards a request to get notes from the Notes application."""
    try:
        response = requests.get(f"{NOTES_APP_URL}/notes")
        response.raise_for_status()
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), response.status_code if 'response' in locals() else 500

if __name__ == '__main__':
    # When running locally, the API Gateway will run on a different port than the notes app
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('GATEWAY_PORT', 8080)))
