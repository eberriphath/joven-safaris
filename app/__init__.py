from flask import Flask
from flask_cors import CORS
from app.config import config
from app.extensions import db, migrate , mail
from app.routes.bookings import bookings_bp
from app.routes.reviews import reviews_bp
from app.models.review import Review
from app.models.booking import Booking

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(config)

    CORS(app)

    app.register_blueprint(bookings_bp, url_prefix="/api")
    app.register_blueprint(reviews_bp, url_prefix="/api")

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from app.routes.home import home_bp
    app.register_blueprint(home_bp)

    return app    