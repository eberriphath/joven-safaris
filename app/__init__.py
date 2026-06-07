from flask import Flask
from flask_cors import CORS
from app.config import config

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(config)

    CORS(app)

    @app.route("/")
    def home():
        return {
            "message" : "Backend api running"
            }

    return app    