from flask import Blueprint, request, jsonify

from app.utils.auth import admin_required
from app.utils.cloudinary_upload import upload_image
import cloudinary.uploader


admin_upload_bp = Blueprint(
    "admin_upload",
    __name__
)


@admin_upload_bp.route(
    "/admin/upload-image",
    methods=["POST"]
)
@admin_required
def upload_image():

    if "image" not in request.files:
        return jsonify({
            "error": "No image provided"
        }), 400


    image = request.files["image"]


    try:

        result = cloudinary.uploader.upload(
            image
        )


        return jsonify({
            "image_url": result["secure_url"]
        }), 200


    except Exception as e:

       print("CLOUDINARY ERROR:", e)

       return jsonify({
        "error": str(e)
        }), 500