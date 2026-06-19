from flask import Flask
from flask_cors import CORS
from app.config import config
from app.extensions import db, migrate
from app.routes.bookings import bookings_bp

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(config)

    CORS(app)

    app.register_blueprint(bookings_bp, url_prefix="/api")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    return app    