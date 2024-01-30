pip install flask flask-login flask-sqlalchemy werkzeug

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Use SQLite for a simple demo
app.config['SECRET_KEY'] = 'thisShouldBeSecret'  # Add your own secret key

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return 'Logged in successfully!'
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully!'

if __name__ == '__main__':
    app.run(debug=True)
