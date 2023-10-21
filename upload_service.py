from flask import request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from database_service import db, File, User
from datetime import datetime
import os

ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'txt', 'h5'}



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_nonexistent_filename(directory, filename):
    name, ext = os.path.splitext(filename)
    i = 1
    while True:
        new_filename = f"{name}({i}){ext}"
        if not os.path.exists(os.path.join(directory, new_filename)):
            return new_filename
        i += 1


def upload_file():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    uploaded_file = request.files['file']

    if uploaded_file and allowed_file(uploaded_file.filename):
        user_id = session['user_id']
        username = User.query.get(user_id).username

        user_upload_dir = os.path.join('uploads', username)
        os.makedirs(user_upload_dir, exist_ok=True)

        filename = secure_filename(uploaded_file.filename)

        if os.path.exists(os.path.join(user_upload_dir, filename)):
            new_filename = get_nonexistent_filename(user_upload_dir, filename)
        else:
            new_filename = filename

        file_path = os.path.join(user_upload_dir, new_filename)
        uploaded_file.save(file_path)

        file_size = os.path.getsize(file_path)
        upload_date = datetime.now()

        new_file = File(user_id=user_id, filename=new_filename, file_size=file_size, upload_date=upload_date, file_path=file_path)
        db.session.add(new_file)
        db.session.commit()

        session['file_path'] = file_path

        flash('File uploaded successfully.', 'success')
    else:
        flash('Invalid file format. Allowed formats are: jpeg, jpg, png, txt', 'error')

    return redirect(url_for('home'))

def delete_file(file_id):
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        file = File.query.get(file_id)

        if file and file.user_id == user_id:
            file_path = os.path.join('uploads', user.username, file.filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)

            db.session.delete(file)
            db.session.commit()

            flash('File deleted successfully.', 'success')
        else:
            flash('You do not have permission to delete this file.', 'error')

    return redirect(url_for('home'))