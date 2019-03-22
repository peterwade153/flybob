import os

from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

#load dotenv in the base root
app_root = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join('app_root', '.env')
load_dotenv(dotenv_path)



@app.route('/')
def home():
    return "Welcome to Fly bob, let us take you to your destination"