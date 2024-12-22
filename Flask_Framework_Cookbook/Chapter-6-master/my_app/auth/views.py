import requests
from flask import request, render_template, flash, redirect, url_for, \
    session, Blueprint, g
from flask_login import current_user, login_user, logout_user, \
    login_required
from my_app import db, login_manager, oid, facebook, google, twitter
from my_app.auth.models import User, RegistrationForm, LoginForm, OpenIDForm

auth = Blueprint('auth', __name__)

GOOGLE_OAUTH2_USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/')
@auth.route('/home')
def home():
    return render_template('home.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        flash('Your are already logged in.', 'info')
        return redirect(url_for('auth.home'))

    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash(
                'This username has been already taken. Try another one.',
                'warning'
            )
            return render_template('register.html', form=form)
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered. Please login.', 'success')
        return redirect(url_for('auth.login'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('auth.home'))

    form = LoginForm(request.form)
    openid_form = OpenIDForm(request.form)

    if request.method == 'POST':
        if 'openid' in request.form:
            openid_form.validate()
            if openid_form.errors:
                flash(openid_form.errors, 'danger')
                return render_template('login.html', form=form, openid_form=openid_form)
            openid = request.form.get('openid')
            return oid.try_login(openid, ask_for=['email', 'nickname'])
        else:
            form.validate()
            if form.errors:
                flash(form.errors, 'danger')
                return render_template('login.html', form=form, openid_form=openid_form)

            username = request.form.get('username')
            password = request.form.get('password')
            existing_user = User.query.filter_by(username=username).first()

            if not (existing_user and existing_user.check_password(password)):
                flash('Invalid username or password. Please try again.', 'danger')
                return render_template('login.html', form=form)

        login_user(existing_user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('auth.home'))

    return render_template('login.html', form=form, openid_form=openid_form)


@oid.after_login
def after_login(resp):
    username = resp.nickname or resp.email
    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username, '')
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('auth.home'))


# Facebook OAuth
@auth.route('/facebook-login')
def facebook_login():
    return facebook.authorize_redirect(url_for('auth.facebook_callback', _external=True))


@auth.route('/facebook-login/callback')
def facebook_callback():
    token = facebook.authorize_access_token()
    user_info = facebook.get('me?fields=id,name,email').json()
    user = User.query.filter_by(username=user_info['email']).first()
    if not user:
        user = User(username=user_info['email'], password='')
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash(f"Welcome, {user_info['name']}!", 'success')
    return redirect(url_for('auth.home'))


# Google OAuth
@auth.route('/google-login')
def google_login():
    return google.authorize_redirect(url_for('auth.google_callback', _external=True))


@auth.route('/google-login/callback')
def google_callback():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    user = User.query.filter_by(username=user_info['email']).first()
    if not user:
        user = User(username=user_info['email'], password='')
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash(f"Welcome, {user_info['name']}!", 'success')
    return redirect(url_for('auth.home'))


# Twitter OAuth
@auth.route('/twitter-login')
def twitter_login():
    return twitter.authorize_redirect(url_for('auth.twitter_callback', _external=True))


@auth.route('/twitter-login/callback')
def twitter_callback():
    token = twitter.authorize_access_token()
    user_info = twitter.get('account/verify_credentials.json').json()
    user = User.query.filter_by(username=user_info['screen_name']).first()
    if not user:
        user = User(username=user_info['screen_name'], password='')
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash(f"Welcome @{user_info['screen_name']}!", 'success')
    return redirect(url_for('auth.home'))




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
