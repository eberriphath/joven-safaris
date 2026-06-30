from datetime import datetime
from app.extensions import db

class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(30), default="admin")

    is_active = db.Column(db.Boolean, default=True)

    last_login = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)