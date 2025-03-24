import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('FLASK_SECRET_KEY')
    return app

# Create the app instance
app = create_app() 