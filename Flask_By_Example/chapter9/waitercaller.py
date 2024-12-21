from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user

from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
from user import User
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Use an environment variable for the secret key
login_manager = LoginManager(app)
login_manager.login_view = 'home'

DB = DBHelper()
PH = PasswordHelper()


@login_manager.user_loader
def load_user(user_id):
    stored_user = DB.get_user(user_id)
    if stored_user:
        return User(user_id)
    return None


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return render_template("home.html", error="Invalid email or password.")


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return render_template("home.html", error="Passwords do not match.")
    if DB.get_user(email):
        return render_template("home.html", error="User already exists.")
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for('home'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/account")
@login_required
def account():
    return "You are logged in"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
