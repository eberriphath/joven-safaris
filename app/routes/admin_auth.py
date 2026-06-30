from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
import jwt
import datetime

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