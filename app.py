from flask import Flask, render_template, request, redirect, url_for, session, flash
from database_service import db, File, bcrypt, User
import auth_service as auth
import upload_service as upl
from map_service import generate_plot
import secrets

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = secret_key


db.init_app(app)
bcrypt.init_app(app)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    return upl.upload_file()


@app.route('/plot', methods=['POST'])
def plot_graph():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    file_path = session.get('file_path')

    if request.method == 'POST' and file_path:
        generate_plot(file_path)
        return redirect(url_for('home'))

    return redirect(url_for('home'))


@app.route('/view_file/<int:file_id>')
def view_file(file_id):
    if 'user_id' in session:
        user_id = session['user_id']
        file = File.query.get(file_id)


        if file and file.user_id == user_id:

            file_path = file.file_path 
            generate_plot(file_path)

        return redirect(url_for('home'))

    return redirect(url_for('login'))

@app.route('/delete_file/<int:file_id>')
def delete_file(file_id):
    return upl.delete_file(file_id)


@app.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        user_files = File.query.filter_by(user_id=user_id).all()

        return render_template('home.html', user=user, user_files=user_files)
    
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    return auth.login()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return auth.register()


@app.route('/logout')
def logout():
    return auth.logout()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)