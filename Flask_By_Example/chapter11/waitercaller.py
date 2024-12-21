import datetime
from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

import os
import config
from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
from bitlyhelper import BitlyHelper
from user import User
from forms import RegistrationForm, LoginForm, CreateTableForm

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", config.SECRET_KEY)
login_manager = LoginManager(app)
login_manager.login_view = "home"

DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)
    return None


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user(form.loginemail.data)
        print (form.loginemail.data)
        print(stored_user)
        if stored_user:
            # Ensure salt and hashed are bytes
            salt = stored_user["salt"].encode() if isinstance(stored_user["salt"], str) else stored_user["salt"]
            hashed = stored_user["hashed"].encode() if isinstance(stored_user["hashed"], str) else stored_user["hashed"]
            print (PH.validate_password(form.loginpassword.data, salt, hashed))
            if PH.validate_password(form.loginpassword.data, salt, hashed):
                user = User(form.loginemail.data)
                login_user(user, remember=True)
                return redirect(url_for("account"))
        form.loginemail.errors.append("Invalid email or password.")

    return render_template("home.html", loginform=form, registrationform=RegistrationForm())


@app.route("/register", methods=["POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address is already registered.")
            return render_template("home.html", loginform=LoginForm(), registrationform=form)
        
        salt = PH.get_salt()  # get_salt() returns a string, so no need to decode
        # Concatenate password and salt, then hash
        hashed = PH.get_hash((form.password.data + salt).encode())  # Encode the concatenated string
        DB.add_user(form.email.data, salt, hashed)
        
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("home"))
    return render_template("home.html", loginform=LoginForm(), registrationform=form)




@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())


@app.route("/dashboard")
# @login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    for req in requests:
        deltaseconds = (now - req["time"]).seconds
        minutes, seconds = divmod(deltaseconds, 60)
        req["wait_minutes"] = f"{minutes}:{str(seconds).zfill(2)}"
    return render_template("dashboard.html", requests=requests)


@app.route("/dashboard/resolve")
# @login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    if request_id:
        DB.delete_request(request_id)
        flash("Request resolved.", "success")
    return redirect(url_for("dashboard"))


@app.route("/account")
# @login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", createtableform=CreateTableForm(), tables=tables)


@app.route("/account/createtable", methods=["POST"])
# @login_required
def account_createtable():
    form = CreateTableForm(request.form)
    if form.validate():
        tableid = DB.add_table(form.tablenumber.data, current_user.get_id())
        new_url = BH.shorten_url(config.base_url + f"newrequest/{tableid}")
        DB.update_table(tableid, new_url)
        flash("Table created successfully.", "success")
        return redirect(url_for("account"))
    flash("Failed to create table. Please try again.", "error")
    return render_template("account.html", createtableform=form, tables=DB.get_tables(current_user.get_id()))


@app.route("/account/deletetable")
# @login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    if tableid:
        DB.delete_table(tableid)
        flash("Table deleted successfully.", "success")
    return redirect(url_for("account"))


@app.route("/newrequest/<tid>")
def new_request(tid):
    if DB.add_request(tid, datetime.datetime.now()):
        flash("Your request has been logged, and a waiter will be with you shortly.", "success")
        return redirect(url_for("dashboard"))
    flash("A request is already pending for this table. Please be patient.", "warning")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
