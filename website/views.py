from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import mysql.connector

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Empty Note! Please enter any character', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/update-note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def update_note(note_id):

    if request.method == 'POST':
        note_data = request.form.get('note_data')

        if len(note_data) < 1:
            flash('Empty Note! Please enter any character', category='error')
        else:
            
            note=Note.query.get_or_404(note_id)
            note.data = note_data
            db.session.add(note)
            db.session.commit()
            flash('Note updated!', category='success')
            return redirect(url_for('views.home'))
            

    return render_template("update.html", user=current_user, note_id=note_id)

