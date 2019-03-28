import os
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from celery import Celery
from flask_mail import Mail
import cloudinary as Cloud

from .config import app_configuration
from app.models import db
from app.auth import auth_blueprint
from app.flights import flight_blueprint
from app.reservations import reservations_blueprint


app = Flask(__name__)

#load dotenv in the base root
app_root = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(app_root, '.env')

load_dotenv(dotenv_path)

app_environment = os.getenv('APP_SETTINGS')
app.config.from_object(app_configuration[app_environment])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')  # enter your email here
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') # enter your password here

#connecting sqlalchemy object to the app
db.init_app(app)

#cloudinary config
Cloud.config.update = ({
    'cloud_name':os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET')
})

#register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(flight_blueprint)
app.register_blueprint(reservations_blueprint)


#celery config
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

CELERYBEAT_SCHEDULE = {
        'run-every-1-minute': {
            'task': 'tasks.flight_reminder',
            'schedule': timedelta(seconds=60)
        },
    }

#mail config
mail = Mail(app)


@app.route('/')
def home():
    return "Welcome to Fly bob, let us take you to your destination"
