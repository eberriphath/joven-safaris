from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
import jwt
import datetime
from app.utils.auth import admin_required
from app.extensions import db

from app.models.admin import Admin

admin_auth_bp = Blueprint("admin_auth", __name__)


@admin_auth_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    admin = Admin.query.filter_by(email=email).first()

    if not admin:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(admin.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "admin_id": admin.id,
            "email": admin.email,
            "role": admin.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200

@admin_auth_bp.route("/admin/change-password", methods=["PUT"])
@admin_required
def change_password():

    admin = request.admin

    data = request.get_json()

    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if not current_password or not new_password or not confirm_password:
        return jsonify({
            "error": "All fields are required"
        }), 400

    if not check_password_hash(
        admin.password_hash,
        current_password
    ):
        return jsonify({
            "error": "Current password is incorrect"
        }), 400

    if new_password != confirm_password:
        return jsonify({
            "error": "New passwords do not match"
        }), 400

    if len(new_password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    admin.password_hash = generate_password_hash(
        new_password
    )

    db.session.commit()

    return jsonify({
        "message": "Password changed successfully"
    }), 200