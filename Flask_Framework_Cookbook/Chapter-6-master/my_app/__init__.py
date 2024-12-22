from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'random_key_for_form'
app.secret_key = 'some_random_key'

# Initialize extensions
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

oid = OpenID(app, 'openid-store')

oauth = OAuth(app)

# OAuth Apps
facebook = oauth.register(
    'facebook',
    client_id='FACEBOOK_APP_ID',
    client_secret='FACEBOOK_APP_SECRET',
    api_base_url='https://graph.facebook.com/',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    client_kwargs={'scope': 'email'}
)

google = oauth.register(
    'google',
    client_id='1031819118511-7fjbknqo1i762i1st8h9uplgg3tk66m0.apps.googleusercontent.com',
    client_secret='GOOGLE_CLIENT_SECRET',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'token_endpoint_auth_method': 'client_secret_post'
    }
)

twitter = oauth.register(
    'twitter',
    client_id='Twitter_API_Key',
    client_secret='Twitter_API_Secret',
    request_token_url='https://api.twitter.com/oauth/request_token',
    api_base_url='https://api.twitter.com/1.1/',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate'
)

# Register Blueprints
from my_app.auth.views import auth
app.register_blueprint(auth)

# Create Database Tables
with app.app_context():
    db.create_all()
