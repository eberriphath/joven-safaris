from flask import Flask
from flask_cors import CORS
from app.config import config
from app.extensions import db

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(config)

    CORS(app)

    db.init_app(app)

    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    return app    