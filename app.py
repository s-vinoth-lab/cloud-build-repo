import os
from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore

app = Flask(__name__)

# Initialize Firestore
db = firestore.Client()
notes_ref = db.collection('notes')

@app.route('/')
def index():
    # Get all notes from Firestore, ordered by creation time
    notes = notes_ref.order_by('created_at', direction=firestore.Query.DESCENDING).stream()
    notes_list = []
    for note in notes:
        note_dict = note.to_dict()
        note_dict['id'] = note.id
        notes_list.append(note_dict)
    return render_template('index.html', notes=notes_list)

@app.route('/add', methods=['POST'])
def add_note():
    content = request.form.get('content')
    if content:
        notes_ref.add({
            'content': content,
            'created_at': firestore.SERVER_TIMESTAMP
        })
    return redirect(url_for('index'))

@app.route('/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    notes_ref.document(note_id).delete()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
