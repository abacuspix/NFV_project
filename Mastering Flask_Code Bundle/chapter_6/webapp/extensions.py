from flask import flash, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_openid import OpenID
from flask_login import LoginManager, current_user
from flask_principal import Principal, Permission, RoleNeed
from authlib.integrations.flask_client import OAuth

bcrypt = Bcrypt()
oid = OpenID()
oauth = OAuth()
principals = Principal()

# Define permissions
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"

# User loader callback
@login_manager.user_loader
def load_user(userid):
    from models import User
    return User.query.get(userid)

# Handle OpenID login
@oid.after_login
def create_or_login(resp):
    from models import db, User
    username = resp.fullname or resp.nickname or resp.email

    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    session['username'] = username
    return redirect(url_for('blog.home'))

# OAuth Configuration for Facebook
facebook = oauth.register(
    'facebook',
    client_id='YOUR_FACEBOOK_APP_ID',
    client_secret='YOUR_FACEBOOK_APP_SECRET',
    api_base_url='https://graph.facebook.com/',
    authorize_url='https://www.facebook.com/dialog/oauth',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    client_kwargs={'scope': 'email'},
)

# OAuth Configuration for Twitter
twitter = oauth.register(
    'twitter',
    client_id='YOUR_TWITTER_API_KEY',
    client_secret='YOUR_TWITTER_API_SECRET',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    api_base_url='https://api.twitter.com/1.1/',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)

# Token getter for Facebook
@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_oauth_token')

# Token getter for Twitter
@twitter.tokengetter
def get_twitter_oauth_token():
    return session.get('twitter_oauth_token')
