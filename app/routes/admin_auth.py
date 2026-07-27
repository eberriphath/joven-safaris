from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from secrets import token_urlsafe
from datetime import datetime, timedelta
import jwt
from app.utils.auth import admin_required
from app.extensions import db
from app.utils.email import send_password_reset_email

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

    if not admin.is_active:
        return jsonify({
            "error": "This account has been disabled."
        }), 403

    token = jwt.encode(
        {
            "admin_id": admin.id,
            "email": admin.email,
            "role": admin.role,
            "exp": datetime.utcnow() + timedelta(hours=24),
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

    admin.reset_token = None
    admin.reset_token_expiry = None

    db.session.commit()

    return jsonify({
        "message": "Password changed successfully"
    }), 200


@admin_auth_bp.route("/admin/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    admin = Admin.query.filter_by(email=email).first()

    if not admin:
        return jsonify({
            "message": "If an account with that email exists, a password reset link has been sent."
        }), 200

    token = token_urlsafe(32)

    admin.reset_token = token
    admin.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)

    db.session.commit()

    send_password_reset_email(admin.email, token)

    return jsonify({
        "message": "If an account with that email exists, a password reset link has been sent."
    }), 200


@admin_auth_bp.route("/admin/reset-password/<token>", methods=["PUT"])
def reset_password(token):

    data = request.get_json()

    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not password or not confirm_password:
        return jsonify({
            "error": "Both password fields are required."
        }), 400

    if password != confirm_password:
        return jsonify({
            "error": "Passwords do not match."
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters."
        }), 400

    admin = Admin.query.filter_by(
        reset_token=token
    ).first()

    if not admin:
        return jsonify({
            "error": "Invalid reset link."
        }), 400

    if (
        admin.reset_token_expiry is None or
        admin.reset_token_expiry < datetime.utcnow()
    ):
        return jsonify({
            "error": "Reset link has expired."
        }), 400

    admin.password_hash = generate_password_hash(password)

    admin.reset_token = None
    admin.reset_token_expiry = None

    db.session.commit()

    return jsonify({
        "message": "Password has been reset successfully."
    }), 200