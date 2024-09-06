"""This module is the core of the project."""
from flask import Flask
from flask_cors import CORS


class CreateApp:
    """
    Initialize the core application
    """
    app = Flask(__name__, template_folder='../templates')
    app.debug = True

    def __init__(self):
        self.headers = None

    def create_app(self):
        CORS(self.app)

        with self.app.app_context():

           
            from app.project.contoller import mod_ppg

            self.app.register_blueprint(mod_ppg)

            return self.app
