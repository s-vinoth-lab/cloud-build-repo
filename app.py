from flask import Flask, request, jsonify
import os
from google.cloud import firestore

app = Flask(__name__)

# Initialize Firestore DB client
db = firestore.Client()

NOTES_COLLECTION = 'notes'

@app.route('/')
def hello_world():
    return 'Hello, World! This is the Notes App.'

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the Flask application."""
    return jsonify({"status": "healthy", "service": "notes-app"}), 200

@app.route('/notes', methods=['POST'])
def add_note():
    """Adds a new note to Firestore."""
    try:
        data = request.get_json()
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({"error": "Missing title or content"}), 400

        title = data['title']
        content = data['content']

        doc_ref = db.collection(NOTES_COLLECTION).document()
        doc_ref.set({
            'title': title,
            'content': content,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        return jsonify({"id": doc_ref.id, "message": "Note added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/notes', methods=['GET'])
def get_notes():
    """Retrieves all notes from Firestore."""
    try:
        notes = []
        # Order by timestamp to get most recent first, or as desired
        docs = db.collection(NOTES_COLLECTION).order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            note = doc.to_dict()
            note['id'] = doc.id
            notes.append(note)
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # When running locally, you might want to specify a port
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
