import os

from flask import Flask
from dotenv import load_dotenv

from .config import app_configuration

app = Flask(__name__)

#load dotenv in the base root
app_root = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(app_root, '.env')

load_dotenv(dotenv_path)

app_environment = os.getenv('APP_SETTINGS')
app.config.from_object(app_configuration[app_environment])


@app.route('/')
def home():
    return "Welcome to Fly bob, let us take you to your destination"
