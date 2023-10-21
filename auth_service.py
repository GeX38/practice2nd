from flask import Flask, render_template, request, redirect, url_for, session
from database_service import User
from database_service import db, User, bcrypt
def login():
    error = None
    success_message = request.args.get('success_message')
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            error = "Invalid username or password. Please try again."

    return render_template('login.html', error=error, success_message=success_message)

def register():
    error = None
    success_message = None
    if request.method == 'POST':
        data = request.form
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            error = "Username is already registered. Please use a different username."
        else:
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            user = User(username=data['username'], password=hashed_password)
            db.session.add(user)
            db.session.commit()
            success_message = "Registration successful. You can now log in."

            return redirect(url_for('login', success_message=success_message))

    return render_template('register.html', error=error)

def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
