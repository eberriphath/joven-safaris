from datetime import datetime
from app.extensions import db


class Package(db.Model):

    __tablename__ = "packages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    destination = db.Column(
        db.String(150),
        nullable=False
    )

    duration = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    image_url = db.Column(
        db.String(255),
        nullable=True
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )